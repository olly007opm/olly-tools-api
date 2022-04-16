from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialise FastAPI
tags_metadata = [
        {
            "name": "convert",
            "description": "Convert data between different formats",
        },
        {
            "name": "generate",
            "description": "Generate data such as lorem ipsum text",
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
from tools import convert
from tools import generate
app.include_router(convert.router)
app.include_router(generate.router)


# App routes
@app.get("/hello/{name}", tags=["other"])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
