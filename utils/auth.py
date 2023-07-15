import jwt
import time
from utils.secret_manager import get_secret

def authenticate(jwtToken):
    """
    This function is used to authenticate the user by checking the JWT token
    """
    if jwtToken:
        # TODO: 1 . Find the jwtToken in the database and check if it is valid
        JWT_SECRET = get_secret().get('JWT_SECRET', None)
        decodedJWT = jwt.decode(jwtToken, JWT_SECRET, algorithms=["HS256"])
        if decodedJWT:
            exp = decodedJWT.get('exp', None)
            if exp and exp > int(time.time()):
                return True, decodedJWT
    return False, None