#  olly-tools-api | __init__.py
#  Last modified: 24/04/2022, 12:38
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

import os
import firebase_admin
from firebase_admin import credentials, firestore

# Load enviroment variables
from dotenv import load_dotenv
load_dotenv()

db = None


# Initialise Firestore
def initialise_firestore():
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "olly-tools",
        "private_key_id": os.environ.get("FIREBASE_CERT_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_CERT_PRIVATE_KEY"),
        "client_email": os.environ.get("FIREBASE_CERT_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CERT_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("FIREBASE_CERT_CLIENT_X509_CERT_URL")
    })

    firebase_admin.initialize_app(cred, {
        "apiKey": os.environ.get("FIREBASE_APIKEY"),
        "authDomain": os.environ.get("FIREBASE_AUTHDOMAIN"),
        "projectId": "olly-tools",
        "storageBucket": os.environ.get("FIREBASE_STORAGEBUCKET"),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGINGSENDERID"),
        "appId": os.environ.get("FIREBASE_APPID"),
    })

    return firestore.client()


def get_database():
    global db
    # If db is not initialised, initialise it
    if not db:
        db = initialise_firestore()
    return db
