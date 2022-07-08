from fastapi import FastAPI
from routes.index import user
from flask_sqlalchemy import SQLAlchemy
app = FastAPI()

app.include_router(user)