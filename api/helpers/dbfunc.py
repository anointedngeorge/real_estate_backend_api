


from api.models.users import BlackListedTokens


def createBlackListedTokens(token:str):
    return BlackListedTokens.objects.update_or_create(token=str(token))