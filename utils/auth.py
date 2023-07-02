
def authenticate(jwtToken):
    """
    This function is used to authenticate the user by checking the JWT token
    """
    status = False
    user = {
        'id': '1234567890',
        'walletAddress': '0x1234567890'
    }
    return status, user