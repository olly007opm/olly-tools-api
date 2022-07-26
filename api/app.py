#  olly-tools-api | app.py
#  Last modified: 26/07/2022, 18:00
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialise FastAPI
tags_metadata = [
        {
            "name": "convert",
            "description": "Convert data between different formats",
        },
        {
            "name": "find",
            "description": "Find values",
        },
        {
            "name": "game",
            "description": "Games",
        },
        {
            "name": "generate",
            "description": "Generate data such as lorem ipsum text",
        },
        {
            "name": "track",
            "description": "Tracking",
        },
        {
            "name": "url",
            "description": "Url shortening and expanding",
        },
        {
            "name": "auth",
            "description": "User authentication",
        },
        {
            "name": "other",
            "description": "Other api endpoints that cannot be categorised",
        },
    ]

app = FastAPI(
    title="Olly Tools API",
    version="1.0.0",
    description="A simple API with various tools",
    contact={
        "name": "Olly",
        "url": "https://olly.ml",
        "email": "olly@olly.ml",
    },
    openapi_tags=tags_metadata,
    docs_url="/",
    redoc_url=None
)

# Initialise CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import all routes
from api.tools import convert
from api.tools import find
from api.tools import game
from api.tools import generate
from api.tools import track
from api.tools import url
import api.auth_routes as auth_routes

app.include_router(convert.router)
app.include_router(find.router)
app.include_router(game.router)
app.include_router(generate.router)
app.include_router(track.router)
app.include_router(url.router)
app.include_router(auth_routes.router)


# App routes
@app.get("/hello/{name}", tags=["other"])
def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/planned", tags=["other"])
def planned():
    """
    Planned features
    - Find Pi and e to the nth digit
    - Unit converter
      - Temperature (C, F and K)
      - Volume
      - Mass
    - Reverse text
    - Check if palindrome (reads the same forwards as backwards like "racecar")
    - Vigenere / Vernam / Ceasar Ciphers (encode and decode)
    - Base 64 encode and decode
    - Weather
    - Whois lookup
    - Noughts and crosses game
    - Battleship game
    """
    return {"message": "This API is currently under development"}
