

from api.models.realtors import Realtors, Referrals


class ReferralService:

    @staticmethod
    def confirm_referral_code(referral_code):
        sponsor_realtor = Realtors.objects.filter(
            referral_code=referral_code
        ).first()

        if not sponsor_realtor:
            raise ValueError("Invalid referral code")

        sponsor_node, _ = Referrals.objects.get_or_create(
            realtor=sponsor_realtor,
            defaults={"sponsor": None}
        )
        return sponsor_node
