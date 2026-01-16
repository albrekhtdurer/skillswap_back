from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.user import router as user_router
from api.login import router as auth_router
from api.city import router as city_router
from api.category import router as category_router
from api.users import router as users_router

app = FastAPI()
app.include_router(user_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(city_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

origins = [
    "*",  # wildcard
    "http://localhost:5173",  # Example frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def home():
    return {"Greet": "Привет! Это супер-сервер команды 42_5"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Skillswap_42_5",
        version="1.0.0",
        summary="OpenAPI схема для бэкэнда проекта Skillswap",
        routes=app.routes
    )
    app.openapi_schema=openapi_schema
    return app.openapi_schema

app.openapi=custom_openapi