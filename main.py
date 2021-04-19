import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from api.endpoints import auth, user, rooms, bookings, payments
from configs.base_config import settings


# Create metadata for tags
# The order of each tag metadata dictionary also defines the order shown in the docs UI.
tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication/Authorization routes",
    },
    {
        "name": "users",
        "description": "Normal user operations",
    },
    {
        "name": "rooms",
        "description": "Room and room type operations",
    },
    {
        "name": "bookings",
        "description": "Bookings operations", 
    },
        {
        "name": "payments",
        "description": "Payments operations", 
    }
]

app = FastAPI(
        title="Horesy API", 
        description="API to manage authentication, hotel bookings, checkins and payments", 
        version="0.1.0", 
        openapi_tags=tags_metadata, 
        openapi_url="/api/v1/openapi.json"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_tortoise(
    app,
    # db_url="sqlite://db.sqlite3",
    db_url=settings.DATABASE_URI,
    modules={'models':['models']},
    generate_schemas=True,
    add_exception_handlers=True
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(payments.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, workers=4)