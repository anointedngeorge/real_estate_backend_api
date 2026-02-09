from datetime import datetime, timedelta, timezone
import jwt
import uuid

from api.helpers.dbfunc import createBlackListedTokens
from api.models.users import  BlackListedTokens

APP = "api"
MAX_ACCESS_TOKEN_AGE = timedelta(minutes=15)
CLOCK_SKEW = timedelta(seconds=30)

def generate_access_token(user, secret_key, algorithm="HS256"):
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "type": "bearer",
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "aud": "auth",
        "jti": jti,
        "iss": APP,
    }

    return jwt.encode(payload, secret_key, algorithm=algorithm)


def generate_refresh_token(user, secret_key, algorithm="HS256"):
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())  # unique token ID

    payload = {
        "sub": str(user.id),
        "type": "refresh",
        "jti": jti,
        "iat": now,
        "exp": now + timedelta(days=14),
        "aud": "auth",
        "iss": APP,
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return token, jti




def is_token_revoked(jti):
    result = BlackListedTokens.objects.filter(jti=jti).first()
    return result is not None



def decode_jwt_token(
    token: str,
    secret_key: str,
    algorithms=["HS256"],
):
    """
    Decodes and validates a JWT with strict max-age enforcement.
    """
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=algorithms,
            audience="auth",
            issuer=APP,
            options={
                "require": ["exp", "iat", "sub",'jti'],
            },
        )

        now = datetime.now(timezone.utc)

        # ---- STRICT iat VALIDATION ----
        iat = payload.get("iat")
        if not isinstance(iat, (int, float, datetime)):
            raise jwt.InvalidTokenError("Invalid iat claim")

        # PyJWT may return iat as int (timestamp)
        if isinstance(iat, (int, float)):
            iat = datetime.fromtimestamp(iat, tz=timezone.utc)

        # Reject tokens issued in the future
        if iat > now + CLOCK_SKEW:
            raise jwt.InvalidTokenError("Token issued in the future")

        # Enforce max token age
        token_age = now - iat
        if token_age > MAX_ACCESS_TOKEN_AGE:
            raise jwt.ExpiredSignatureError("Token exceeds max age")

        # ---- OPTIONAL REVOCATION CHECK ----
        jti = payload.get("jti", None)
        
        if jti and is_token_revoked(jti):
            raise jwt.InvalidTokenError("Token revoked")

        return payload

    except jwt.ExpiredSignatureError as e:
        print("Token expired:")
        createBlackListedTokens(token=token)
        return None

    except jwt.InvalidTokenError as e:
        print("Token invalid:", e)
        return None