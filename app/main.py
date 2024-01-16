#from random import randrange
#from typing import Optional, List
from fastapi import FastAPI#, Response, status, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware

import psycopg
#from sqlalchemy.orm import Session
from . import models#, schemas, utils
from .database import engine#, get_db
from .routers import post, user, auth, vote
from .config import settings

# next line is not needed since alembic will create the tables
# video 11:13:51
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize conn as a global variable
# conn = None

# @app.on_event("startup")
# async def startup_event():
#     global conn
#     conn = psycopg.connect("dbname='fastapi' user='postgres' host='localhost' password='Tool1992' port='5432'")
#     print('DB connection was ok')
        
#accessing files post.py and router.py
app.include_router(post.router)
app.include_router(user.router)       
app.include_router(auth.router)       
app.include_router(vote.router)    


@app.get("/")
async def root():
    return {"message": "Hello Welcome"}

