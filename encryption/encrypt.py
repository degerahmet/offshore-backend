from utils.secret_manager import get_secret
import rsa

def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)

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
    
    public_key = body.get('walletAddress', None)
    if public_key is None:
        return {
            'statusCode': 400,
            'body': 'No wallet address provided'
        }

    private_key = get_secret().get('SECRET_KEY', None)
    if private_key is None:
        return {
            'statusCode': 500,
            'body': 'No private key found'
        }
    
    base64_message = body.get('base64Message', None)
    if base64_message is None:
        return {
            'statusCode': 400,
            'body': 'No base64 message provided'
        }
    
    encrpytedMessage = encrypt(base64_message, public_key)
    signature = sign(base64_message, private_key)
    return {
        'statusCode': 200,
        'body': {
            'encryptedMessage': encrpytedMessage,
            'signature': signature
        }
    }