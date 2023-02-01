from pyexpat import model
from turtle import title
from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from .models import Post, PostDB
from .database import engine, get_db
from . import models
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
        
        
@app.get("/")
def root():
    return {"message": "WELCOME to the base routing link !!!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.PostDB).all()
    # return {"status": "Success"}
    return {"status": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # query = """SELECT * FROM posts"""
    # cursor.execute(query)
    # posts = cursor.fetchall()
    
    posts = db.query(models.PostDB).all()
    
    return {"data":posts}

@app.get("/posts/latestpost")
def get_latest_post(db: Session = Depends(get_db)):
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # query = (
    #     "SELECT * FROM posts "
    #     "ORDER BY created_at DESC LIMIT 1"
    #     )
    # print(query)
    # cursor.execute(query)
    # latest_post = cursor.fetchone()
    latest_post = db.query(models.PostDB).all()[-1]
    
    return {"latest_post": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)): 
    ## Type hinting of id very important! This enables FastAPI to convert the id in path operation
    ## from string to int. This type hinting also handles errors nicely if user enters string instead
    ## of numbers in the path parameter "id"
    
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # query = (
    #     "SELECT * FROM posts "
    #     "WHERE id = %s"
    #     )
    # cursor.execute(query, [id])
    # post = cursor.fetchone()
    
    post = db.query(models.PostDB).filter(models.PostDB.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with the id: {id}")

    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # print(post) #pydantic model (fields can be accessed like post.title etc..)
    # print(post.dict()) #converts pydantic model to dict and returns
    
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # query = (
    #     "INSERT INTO posts "
    #     "(title, content, published) "
    #     "VALUES (%s, %s, %s)"
    # )
    # cursor.execute(query, [post.title, post.content, post.published])
    # post_id = cursor.lastrowid
    # conn.commit()
    
    # new_post = models.PostDB(title=post.title, content=post.content, published=post.published)
    ## Shortcut for the above code. Automatically unpacks post.dict() and assigns the values of the keys to 
    ## the repsective parameters of the PostDB function
    ## Details: https://www.geeksforgeeks.org/packing-and-unpacking-arguments-in-python/
    new_post = models.PostDB(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"message": f"New Post Sucessfully Created With ID: {new_post.id}"} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # select_query = """SELECT * FROM posts WHERE id = %s"""
    # cursor.execute(select_query, [id])
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"No post found with id: {id}")
    # query = (
    #     "DELETE FROM posts "
    #     "WHERE id = %s"
    # )
    # cursor.execute(query, [id])
    # conn.commit()
    
    post = db.query(models.PostDB).filter(models.PostDB.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    # the below return statement will not return the message as in FastAPI 204 status code implies
    # that you shouldn't return anything as you're removing sth. So we can return the Response instead
    # return {"message": f"Successfully removed post with id: {post['id']}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, input_post: Post, db: Session = Depends(get_db)):    
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # select_query = """SELECT * FROM posts WHERE id = %s"""
    # cursor.execute(select_query, [id])
    # db_post = cursor.fetchone()
    # if not db_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"No post found with id: {id}")
    # query = (
    #     "UPDATE posts "
    #     "SET title = %s, content = %s "
    #     "WHERE id = %s"
    # )    
    # cursor.execute(query, [input_post.title, input_post.content, id])
    # conn.commit()
    
    post = db.query(models.PostDB).filter(models.PostDB.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")
    
    post.update(input_post.dict(), synchronize_session=False)
    db.commit()
    
    return {"updated_post": post.first()}

    
    