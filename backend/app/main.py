from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router

app = FastAPI(
    title="Github Repo Search API",
    description="Search for repos on Github",
    version="0.1.0",
    contact={
        "name": "Chitru Shrestha",
        "email": "schitru@gmail.com",
    },
)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
