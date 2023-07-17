import time
from utils.secret_manager import get_secret
import json
import jwt
from utils.auth import authenticate
from Crypto.Cipher import AES
import base64

def decrypt(ciphertext, key, nonce):
    ciphertext = base64.b64decode(ciphertext)
    nonce = base64.b64decode(nonce)
    decrypt_cipher = AES.new(key.encode('utf8'), AES.MODE_CTR, nonce=nonce)
    try:
        return decrypt_cipher.decrypt(ciphertext).decode('ascii')
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
    nonce = body.get('nonce', None)
    if encrpytedMessage is None or nonce is None:
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
    
    decryptedMessage = decrypt(encrpytedMessage, private_key, nonce)
    if decryptedMessage:
        decryptedMessage = base64.b64decode(decryptedMessage)
        #TODO 1.Create a new JWT token for the user
        #TODO 2.Save the JWT token in the database
        #TODO 3.Return the JWT token to the user
        
        # Creating JWT token
        json_data = str({
            'walletAddress': public_key,
            'message': decryptedMessage,
            'exp': int(time.time()) + 60*60*24*7
        })
        
        # convert string to json
        json_data = json.dumps(json_data)
        print(json_data)
        encoded_jwt = jwt.encode(json_data, JWT_SECRET, algorithm="HS256")
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
            'body': 'Encrypted message is not verified'
        }

    