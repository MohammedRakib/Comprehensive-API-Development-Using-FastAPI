from fastapi import Body, FastAPI, status, HTTPException, Response
from starlette.status import HTTP_100_CONTINUE
from app.models import Post
from random import randrange
import mysql.connector
import time

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
        
my_posts = [{"id": 1, "title": "POST-I", "body": "Blah 1", "rating": 7}, 
            {"id": 2, "title": "POST-II", "body": "Blah 2", "rating": 5},
            ]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post 
        
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get("/")
def root():
    return {"message": "WELCOME to the base routing link !!!"}

@app.get("/posts")
def get_posts():
    query = """SELECT * FROM posts"""
    cursor.execute(query)
    posts = cursor.fetchall()
    return {"data":posts}

@app.get("/posts/latestpost")
def get_latest_post():
    query = (
        "SELECT * FROM posts "
        "ORDER BY created_at DESC LIMIT 1"
        )
    print(query)
    cursor.execute(query)
    latest_post = cursor.fetchone()
    return {"latest_post": latest_post}

@app.get("/posts/{id}")
def get_post(id: int): 
    #Type hinting of id very important! This enables FastAPI to convert the id in path operation
    #from string to int. This type hinting also handles errors nicely if user enters string instead
    # of numbers in the path parameter "id"
    query = (
        "SELECT * FROM posts "
        "WHERE id = %s"
        )
    cursor.execute(query, [id])
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with the id: {id}")

    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # print(post) #pydantic model (fields can be accessed like post.title etc..)
    # print(post.dict()) #converts pydantic model to dict and returns
    query = (
        "INSERT INTO posts "
        "(title, content, published) "
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(query, [post.title, post.content, post.published])
    post_id = cursor.lastrowid
    conn.commit()
    
    return {"message": f"New Post Sucessfully Created With ID: {post_id}"} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    select_query = """SELECT * FROM posts WHERE id = %s"""
    cursor.execute(select_query, [id])
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")
    query = (
        "DELETE FROM posts "
        "WHERE id = %s"
    )
    cursor.execute(query, [id])
    conn.commit()
    
    # the below return statement will not return the message as in FastAPI 204 status code implies
    # that you shouldn't return anything as you're removing sth. So we can return the Response instead
    # return {"message": f"Successfully removed post with id: {post['id']}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, input_post: Post):    
    select_query = """SELECT * FROM posts WHERE id = %s"""
    cursor.execute(select_query, [id])
    db_post = cursor.fetchone()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")
    query = (
        "UPDATE posts "
        "SET title = %s, content = %s "
        "WHERE id = %s"
    )    
    cursor.execute(query, [input_post.title, input_post.content, id])
    conn.commit()
    
    return {"updated_post": input_post}

    
    