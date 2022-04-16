from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialise FastAPI
app = FastAPI(docs_url="/docs", redoc_url=None)

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
@app.get("/", tags=["other"])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}", tags=["other"])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Customise OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    tags_metadata = [
        {
            "name": "other",
            "description": "Other api endpoints that cannot be categorised",
        },
        {
            "name": "convert",
            "description": "Convert data between different formats",
        },
        {
            "name": "generate",
            "description": "Generate data such as lorem ipsum text",
        }
    ]
    openapi_schema = get_openapi(
        title="Olly Tools API",
        version="1.0.0",
        description="A simple API with various tools",
        routes=app.routes,
        tags=tags_metadata,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
