from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth
import mysql.connector
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = mysql.connector.connect(user='root',
                                    password='1633',
                                    host='localhost',
                                    port=3307,
                                    database='fastapi')
        
        cursor = conn.cursor(dictionary=True)
        print("\n Database Connection Successful !!! \n")
        break

    except Exception as e:
        print(f"\n Database Connection FAILED due to: {e} \n")
        time.sleep(2)
        print("\n Retrying ... \n")
        
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "WELCOME to the base routing link !!!"}
