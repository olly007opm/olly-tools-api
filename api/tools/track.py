#  olly-tools-api | track.py
#  Last modified: 26/07/2022, 18:51
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

import datetime

from fastapi import APIRouter, Security, Request, Response, Form
from fastapi.responses import FileResponse

from api.auth_routes import auth
# Get the database
from api.firebase import get_database

db = get_database()

router = APIRouter(
    prefix="/track",
    tags=["track"],
)


# Go to a tracking pixel
@router.get("/test")
def test(request: Request, response: Response):
    headers = {"Cache-Control": "no-cache, no-store, must-revalidate, max-age=0"}
    return FileResponse("api/other/empty.png", headers=headers)


# Go to a tracking pixel
@router.get("/pixel/{code}")
def track(request: Request, response: Response, code: str):
    data = get_pixel_data(code)
    headers = {"Cache-Control": "no-cache, no-store, must-revalidate, max-age=0"}
    if data and data['active']:
        print(request.headers)
        tracking_data = {
            'timestamp': datetime.datetime.now(),
            'ip': request.client.host,
            'mobile': request.headers.get("sec-ch-ua-mobile"),
            'platform': request.headers.get("sec-ch-ua-platform"),
            'user-agent': request.headers.get("user-agent"),
            'language': request.headers.get("accept-language"),
        }
        add_tracking_data(code, tracking_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    else:
        response.status_code = 404
    return FileResponse("api/other/empty.png", headers=headers)


# Create a tracking pixel
@router.post('/create', summary="Create a tracking pixel")
def create_pixel(code: str = None, user=Security(auth, scopes=["tracking_create"]), note: str = None):
    if not code:
        code = generate_code()

    tracking_doc = db.collection('tracking').document()
    tracking_doc.set({
        'code': code,
        'user': user['id'],
        'created': datetime.datetime.now(),
        'tracking_data': [],
        'active': True,
        'note': note
    })
    return {"tracking_pixel": f"https://tools-api.olly.ml/track/pixel/{code}"}


# Generate a random code for the tracking pixel
def generate_code():
    import random
    chars = "0123456789abcdef"

    path = ""
    for i in range(16):
        path += random.choice(chars)
    return path


def add_tracking_data(code, data):
    pixel_data = get_pixel_data(code)
    if not pixel_data:
        return False
    else:
        all_data = pixel_data['tracking_data']
        all_data.append(data)
        db.collection('tracking').document(pixel_data['id']).update({'tracking_data': all_data})


# Get tracking pixel data by code
def get_pixel_data(code: str):
    data = db.collection('tracking').where('code', '==', code).get()
    if data:
        data_id = data[0].id
        data = data[0].to_dict()
        data['id'] = data_id
        return data
    else:
        return None
