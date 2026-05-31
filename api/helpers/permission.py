import yaml
from django.conf import settings


    
with open(settings.BASE_DIR / "api/data/roles.yml") as f:
     ROLE_CONFIG = yaml.safe_load(f)

def get_role_permissions(role: str):
    return ROLE_CONFIG["roles"].get(str(role).lower(), [])