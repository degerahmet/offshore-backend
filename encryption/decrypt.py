import time
from utils.secret_manager import get_secret
import rsa
import jwt
from utils.auth import authenticate



def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False

def sign(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-256')

def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-256'
    except:
        return False
    
def handler(event, context):
    body = event.get('body', None)
    if body is None:
        return {
            'statusCode': 400,
            'body': 'No body provided'
        }
    encrpytedMessage = body.get('encryptedMessage', None)
    signature = body.get('signature', None)
    if encrpytedMessage is None or signature is None:
        return {
            'statusCode': 400,
            'body': 'Missing required parameters'
        }
    public_key = body.get('walletAddress', None)
    if public_key is None:
        return {
            'statusCode': 400,
            'body': 'No wallet address provided'
        }
    
    private_key = get_secret().get('SECRET_KEY', None)
    JWT_SECRET = get_secret().get('JWT_SECRET', None)
    
    decryptedMessage = decrypt(encrpytedMessage, private_key)
    verified = verify(decryptedMessage, signature, public_key)
    if verified:
        #TODO 1.Create a new JWT token for the user
        #TODO 2.Save the JWT token in the database
        #TODO 3.Return the JWT token to the user
        
        # Creating JWT token
        encoded_jwt = jwt.encode({
            'walletAddress': public_key,
            'message': decryptedMessage,
            'exp': int(time.time()) + 60*60*24*7
        }, JWT_SECRET, algorithm="HS256")
        status, user = authenticate(encoded_jwt)
        if not status:
            return {
                'statusCode': 401,
                'body': 'Invalid JWT token'
            }
        return {
            'statusCode': 200,
            'body': {
                'jwtToken': encoded_jwt,
                'user': user,
                'message': 'Successfully authenticated',
            }
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Signature not verified'
        }

    