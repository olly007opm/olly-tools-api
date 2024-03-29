#  olly-tools-api | auth_routes.py
#  Last modified: 26/07/2022, 17:58
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

from fastapi import APIRouter, Depends, Security, Response, Request
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
import os
import bcrypt

# Initialise firestore database
from api.firebase import get_database
db = get_database()

# Initialise login manager and router
auth = LoginManager(os.environ.get("AUTH_SECRET"), '/auth/login')
router = APIRouter(prefix="/auth", tags=["auth"])


# Login a user
@router.post('/login')
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password + os.environ.get("AUTH_PEPPER")
    uid = get_user_id(email)

    user = query_user(uid)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['hash']):
        access_token = auth.create_access_token(
            data={'sub': user['id']},
            scopes=user['scopes']
        )
        print(f"User {email} logged in with scopes {user['scopes']}")
        return {'access_token': access_token}
    else:
        response.status_code = 400
        return {'error': 'invalid credentials'}


# Create a new user in the db
@router.post('/register')
def register(response: Response, request: Request, data: OAuth2PasswordRequestForm = Depends()):
    origin = request.headers.get('origin')
    if os.environ.get("AUTH_ORIGIN") == '*' or origin != os.environ.get("AUTH_ORIGIN"):
        response.status_code = 400
        return {'error': 'invalid origin'}
    else:
        email = data.username
        password = data.password + os.environ.get("AUTH_PEPPER")
        print(f"Registering user {email}")
        if get_user_id(email):
            response.status_code = 400
            return {'error': 'user already exists'}

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = db.collection('users').document()
        user.set({
            'email': email,
            'hash': hashed,
            'scopes': []
        })

        uid = get_user_id(email)
        access_token = auth.create_access_token(
            data={'sub': uid}
        )
        return {'access_token': access_token}


# Protected route, requires valid access token and returns user object
@router.get('/get_user')
def get_user(user=Depends(auth)):
    user.pop('hash')
    return {'user': user}


# Protected route, requires scope 1
@router.get('/scope1')
def scope1(user=Security(auth, scopes=["scope1"])):
    return {'success': True}


# Protected route, requires scope 2
@router.get('/scope2')
def scope2(user=Security(auth, scopes=["scope2"])):
    return {'success': True}


# Test request origin
@router.post('/test-origin')
def test_origin(response: Response, request: Request):
    origin = request.headers.get('origin')
    if origin != os.environ.get("AUTH_ORIGIN"):
        response.status_code = 400
        return {'invalid_origin': origin}
    else:
        return {'valid_origin': origin}


# Get a user id from the db using an email address
def get_user_id(user_email: str):
    user = db.collection('users').where('email', '==', user_email).get()
    if user:
        return user[0].id
    else:
        return None


# Get a user from the db using a user id
@auth.user_loader()
def query_user(user_id: str):
    user = db.collection('users').document(user_id).get()
    try:
        user_data = user.to_dict()
        user_data['id'] = user_id
        try:
            user_data['scopes']
        except KeyError:
            user_data['scopes'] = []
        return user_data
    except TypeError:
        return None
