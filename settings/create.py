import json
from utils.auth import authenticate

def handler(event, context):
    body = event.get('body', None)

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

    # Get user information from the request body
    if body:
        username = body.get('username', None)
        email = body.get('email', None)
        profilePicture = body.get('profilePicture', None)
        name = body.get('name', None)
        phone = body.get('phone', None)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request!')
        }
    
    """
    TODO:
    1- Check if the username is already taken
    2- Check if the email is already taken
    3- Check if the phone is already taken
    4- Create a user settings object in the MongoDB database with the given information
    """

    return {
        'statusCode': 201,
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
