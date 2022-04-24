#  olly-tools-api | url.py
#  Last modified: 21/04/2022, 18:50
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

import datetime
from fastapi import APIRouter, Depends, Security, Response, Form
from fastapi.responses import RedirectResponse
from auth_routes import auth

# Get the database
from firebase import get_database
db = get_database()

router = APIRouter(tags=["url"])


# Go to a shortened url
@router.get("/go/{path}", tags=["url"])
def redirect(response: Response, path: str):
    url = get_url_data(path)
    if url and url['active'] and (url['limit'] == -1 or url['uses'] < url['limit']):
        if url['limit'] != -1:
            db.collection('urls').document(url['id']).update({'uses': url['uses'] + 1})
        return RedirectResponse(url['url'])
    else:
        response.status_code = 404
        return {"error": "Url not found"}


# Expand a shortened url
@router.get("/url/get/{path}", summary="Expand a shortened url")
def url(response: Response, path: str):
    url = get_url_data(path)
    if url and url['active'] and (url['limit'] == -1 or url['uses'] < url['limit']):
        if url['limit'] != -1:
            db.collection('urls').document(url['id']).update({'uses': url['uses'] + 1})
        return {"url": url['url']}
    else:
        response.status_code = 404
        return {"error": "Url not found"}


# Get data about a shortened url
@router.get("/url/get_data/{path}", summary="Get data about a shortened url")
def url(response: Response, path: str, user=Depends(auth)):
    url = get_url_data(path)
    if url:
        if url['user'] == user['id'] or "url_get_data" in user['scopes']:
            return {"data": url}
        else:
            response.status_code = 403
            return {"error": "You don't have permission to get data about this url"}
    else:
        response.status_code = 404
        return {"error": "Url not found"}


# Shorten a url
@router.post('/url/shorten', summary="Shorten a url")
def get_user(response: Response, url: str, user=Security(auth, scopes=["url_shorten"]),
             path: str = Form(None), limit: int = Form(None)):
    reserved_paths = ["shorten", "get", "delete", "update"]
    if path in reserved_paths:
        response.status_code = 400
        return {"error": "Path is reserved"}

    if get_url_data(path):
        response.status_code = 400
        return {"error": "Path is already taken"}

    else:
        if not path:
            path = generate_path()
        url_doc = db.collection('urls').document()
        url_doc.set({
            'path': path,
            'url': url,
            'user': user['id'],
            'created': datetime.datetime.now(),
            'uses': 0,
            'active': True,
            'limit': limit if limit else -1
        })
        return {"shortened_url": f"https://tools-api.olly.ml/go/{path}"}


# Update a shortened url
@router.put('/url/update/{path}', summary="Update a shortened url")
def update(response: Response, path: str, user=Depends(auth),
           active: bool = Form(None), limit: int = Form(None), new_url: str = Form(None), new_path: str = Form(None)):
    url = get_url_data(path)
    if url:
        if url['user'] == user['id'] or "url_update" in user['scopes']:
            updates = {}
            if not (active is None):
                db.collection('urls').document(url['id']).update({'active': active})
                updates['active'] = active
            if limit:
                db.collection('urls').document(url['id']).update({'limit': limit})
                updates['limit'] = limit
            if new_url:
                db.collection('urls').document(url['id']).update({'url': new_url})
                updates['url'] = new_url
            if new_path:
                if get_url_data(new_path):
                    response.status_code = 400
                    return {"error": "Path is already taken"}
                else:
                    db.collection('urls').document(url['id']).update({'path': new_path})
                    updates['path'] = new_path

            return {"success": True, "updates": updates}
        else:
            response.status_code = 403
            return {"error": "You don't have permission to update this url"}
    else:
        response.status_code = 404
        return {"error": "Url not found"}


# Delete a shortened url
@router.delete("/url/delete/{path}", summary="Delete a shortened url")
def delete_url(response: Response, path: str, user=Depends(auth)):
    url = get_url_data(path)
    if url:
        if url['user'] == user['id'] or "url_delete" in user['scopes']:
            db.collection('urls').document(url['id']).delete()
            return {"deleted": True}
        else:
            response.status_code = 403
            return {"error": "You don't have permission to delete this url"}
    else:
        response.status_code = 404
        return {"error": "Url not found"}


# Generate a random path if none is provided
def generate_path():
    import random
    chars = "0123456789abcdef"

    path = ""
    for i in range(6):
        path += random.choice(chars)
    return path


# Get url data by path
def get_url_data(path: str):
    url = db.collection('urls').where('path', '==', path).get()
    if url:
        url_id = url[0].id
        url = url[0].to_dict()
        url['id'] = url_id
        return url
    else:
        return None
