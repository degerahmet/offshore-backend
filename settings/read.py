import json
from utils.auth import authenticate


def handler(event, context):

    # Get the JWT token from the request headers
    jwtToken = event.get('Authorization', None)
    if not jwtToken:
        return {
            'statusCode': 401,
            'body': json.dumps('Unauthorized!')
        }
    
    # Call the authentication middleware to get the user id and wallet address
    status, user = authenticate(jwtToken)
    if not status:
        return {
            'statusCode': 403,
            'body': json.dumps('Forbidden!')
        }
    
    userId = user.get('id', None)
    walletAddress = user.get('walletAddress', None)

    # Get the user settings object from the MongoDB database
    userSettings = None

    username = userSettings.get('username', None)
    email = userSettings.get('email', None)
    profilePicture = userSettings.get('profilePicture', None)
    name = userSettings.get('name', None)
    phone = userSettings.get('phone', None)

    return {
        'statusCode': 200,
        'body': {
            'user':{
                'id': userId,
                'walletAddress': walletAddress,
            },
            'username': username,
            'email': email,
            'profilePicture': profilePicture,
            'name': name,
            'phone': phone
        }
    }
