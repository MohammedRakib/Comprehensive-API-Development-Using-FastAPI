from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app import oauth2
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), 
              current_user: models.UserDB = Depends(oauth2.get_current_user)):
    
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # query = """SELECT * FROM posts"""
    # cursor.execute(query)
    # posts = cursor.fetchall()
    
    posts = db.query(models.PostDB).all()
    
    return posts

@router.get("/latestpost", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db), 
                    current_user: models.UserDB = Depends(oauth2.get_current_user)):
    ## SQL Query without ORM (SQLAlchemy). No need Session for SQL Queries!
    # query = (
    #     "SELECT * FROM posts "
    #     "ORDER BY created_at DESC LIMIT 1"
    #     )
    # print(query)
    # cursor.execute(query)
    # latest_post = cursor.fetchone()
    latest_post = db.query(models.PostDB).all()[-1]
    
    return latest_post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, 
             db: Session = Depends(get_db), 
             current_user: models.UserDB = Depends(oauth2.get_current_user)): 
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

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: models.UserDB = Depends(oauth2.get_current_user)):
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
    
    post = db.query(models.PostDB).filter(models.PostDB.id == new_post.id)
    
    return post.first() 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: models.UserDB = Depends(oauth2.get_current_user)):
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

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, input_post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: models.UserDB = Depends(oauth2.get_current_user)):    
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
    
    return post.first()
