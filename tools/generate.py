#  olly-tools-api | generate.py
#  Last modified: 24/04/2022, 12:30
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

from typing import Optional
from fastapi import APIRouter, Response, Request, Form
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/generate",
    tags=["generate"],
)


@router.get("/lorem", summary="Generate lorem ipsum text")
def lorem_sentences(response: Response, sentences: Optional[int] = None, paragraphs: Optional[int] = None):
    import lorem
    if sentences:
        text = ""
        for i in range(sentences):
            text += lorem.sentence()
            text += " " if i < sentences - 1 else ""
        return {"result": text}
    elif paragraphs:
        text = ""
        for i in range(paragraphs):
            text += lorem.paragraph()
            text += "\n" if i < paragraphs - 1 else ""
        return {"result": text}
    else:
        response.status_code = 400
        return {"error": "No sentences or paragraphs specified"}


# noinspection PyShadowingBuiltins
@router.get("/random", summary="Generate a random number")
def random_number(response: Response, min: int = 0, max: int = 100):
    import random
    try:
        return {"result": random.randint(min, max)}
    except ValueError:
        response.status_code = 400
        return {"error": "Minimum value must be less than maximum value"}


@router.post("/qr", summary="Generate a qr code", responses={200: {"content": {"image/png": {}}}}, response_class=Response)
def qr_code(data: str = Form(...)):
    import qrcode
    from io import BytesIO
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, 'PNG')
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


@router.get("/password", summary="Generate a password")
def password(length: int = 8, upper: bool = True,
             lower: bool = True, digits: bool = True, symbols: bool = True, other: bool = False):
    import random
    upper_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_chars = "abcdefghijklmnopqrstuvwxyz"
    digits_chars = "0123456789"
    symbols_chars = "!@#$%"
    other_chars = "^&*()_+-=[]{}|;':,./<>?"
    chars = ""
    if upper:
        chars += upper_chars
    if lower:
        chars += lower_chars
    if digits:
        chars += digits_chars
    if symbols:
        chars += symbols_chars
    if other:
        chars += other_chars

    password = ""
    for i in range(length):
        password += random.choice(chars)
    return {"result": password}


@router.get("/hex-secret", summary="Generate a hex secret")
def hex_secret(length: int = 256):
    import random
    chars = "0123456789abcdef"

    secret = ""
    for i in range(length):
        secret += random.choice(chars)
    return {"result": secret}


@router.get("/big-text", summary="Generate giant text")
def big_text(response: Response, text: str, output_format: str = "plain"):
    text = text.upper()
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?#()/+-=\"., "
    if any(char not in valid_chars for char in text):
        response.status_code = 400
        return {"error": "Invalid characters in text"}

    big_chars = [
        " █████ |██████ | ██████|██████ |███████|███████| ██████ |██   ██|██|     ██|██   ██|██     |███    ███|███    ██| ██████ |██████ | ██████ |██████ |███████|████████|██    ██|██    ██|██     ██|██   ██|██    ██|███████| █████ |  ███  |██████ |██████ |  ██ ██|███████| █████ |███████| █████ | █████ |██| █████ |   ██  ██ |████|████|    ██|      |     |      |██ ██|  |  |    ".split("|"),
        "██   ██|██   ██|██     |██   ██|██     |██     |██      |██   ██|██|     ██|██  ██ |██     |████  ████|████   ██|██    ██|██   ██|██    ██|██   ██|██     |   ██   |██    ██|██    ██|██     ██| ██ ██ | ██  ██ |   ███ |██   ██| ████  |     ██|     ██| ██  ██|██     |██     |     ██|██   ██|██   ██|██|██   ██|██████████|██  |  ██|   ██ |  ██  |     |██████| █  █|  |  |    ".split("|"),
        "███████|██████ |██     |██   ██|█████  |█████  |██   ███|███████|██|     ██|█████  |██     |██ ████ ██|██ ██  ██|██    ██|██████ |██    ██|██████ |███████|   ██   |██    ██|██    ██|██  █  ██|  ███  |  ████  |  ███  |██   ██|██ ██  |  ███  | █████ |██   ██|██████ |██████ |    ██ | █████ | ██████|██|   ███ |  ██  ██  |██  |  ██|  ██  |██████|█████|      |     |  |  |    ".split("|"),
        "██   ██|██   ██|██     |██   ██|██     |██     |██    ██|██   ██|██|██   ██|██  ██ |██     |██  ██  ██|██  ██ ██|██    ██|██     |██ ▄▄ ██|██   ██|     ██|   ██   |██    ██| ██  ██ |██ ███ ██| ██ ██ |   ██   | ███   |██   ██|   ██  |██     |     ██|███████|     ██|██   ██|   ██  |██   ██|     ██|  |       |██████████|██  |  ██| ██   |  ██  |     |██████|     |  |██|    ".split("|"),
        "██   ██|██████ | ██████|██████ |███████|██     | ██████ |██   ██|██| █████ |██   ██|███████|██      ██|██   ████| ██████ |██     | ██████ |██   ██|███████|   ██   | ██████ |  ████  | ███ ███ |██   ██|   ██   |███████| █████ |███████|███████|██████ |     ██|██████ | █████ |  ██   | █████ | █████ |██|   ██  | ██  ██   |████|████|██    |      |     |      |     |██| █|    ".split("|"),
    ]
    output = ["", "", "", "", ""]
    if output_format == "css":
        output = ["/* ", "/* ", "/* ", "/* ", "/* "]

    for char in text:
        for i in range(5):
            output[i] += big_chars[i][valid_chars.index(char)] + " "

    result = ""
    for line in output:
        result += line[:-1]
        if output_format == "css":
            result += " */"
        result += "\n"
    result = result[:-1]

    return {"result": result}
