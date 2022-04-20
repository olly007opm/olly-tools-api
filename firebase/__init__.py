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
        "type": os.environ.get("FIREBASE_CERT_TYPE"),
        "project_id": os.environ.get("FIREBASE_CERT_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_CERT_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_CERT_PRIVATE_KEY"),
        "client_email": os.environ.get("FIREBASE_CERT_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CERT_CLIENT_ID"),
        "auth_uri": os.environ.get("FIREBASE_CERT_AUTH_URI"),
        "token_uri": os.environ.get("FIREBASE_CERT_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("FIREBASE_CERT_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("FIREBASE_CERT_CLIENT_X509_CERT_URL")
    })

    firebase_admin.initialize_app(cred, {
        "apiKey": os.environ.get("FIREBASE_APIKEY"),
        "authDomain": os.environ.get("FIREBASE_AUTHDOMAIN"),
        "projectId": os.environ.get("FIREBASE_PROJECTID"),
        "storageBucket": os.environ.get("FIREBASE_STORAGEBUCKET"),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGINGSENDERID"),
        "appId": os.environ.get("FIREBASE_APPID"),
        "measurementId": os.environ.get("FIREBASE_MEASUREMENTID")
    })

    return firestore.client()


def get_database():
    global db
    # If db is not initialised, initialise it
    if not db:
        db = initialise_firestore()
    return db
