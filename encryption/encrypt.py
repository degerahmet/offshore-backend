from utils.secret_manager import get_secret
from Crypto.Cipher import AES
import base64

def encrypt(message, key):
    cipher = AES.new(key.encode('utf8'), AES.MODE_CTR)
    ciphertext = cipher.encrypt(message.encode('ascii'))
    nonce = cipher.nonce
    return {
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'nonce': base64.b64encode(nonce).decode('utf-8')
    }

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
    
    encrpytedMessage = encrypt(base64_message, private_key)
    return {
        'statusCode': 200,
        'body': {
            'ciphertext': encrpytedMessage['ciphertext'],
            'nonce': encrpytedMessage['nonce']
        }
    }