from fastapi import Body, FastAPI, status, HTTPException, Response
from starlette.status import HTTP_100_CONTINUE
from app.models import Post
from random import randrange

app = FastAPI()

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
    return {"data": my_posts}

@app.get("/posts/latestpost")
def get_latest_post():
    return {"latest_post": my_posts[-1]}

@app.get("/posts/{id}")
def get_post(id: int): 
    #Type hinting of id very important! This enables FastAPI to convert the id in path operation
    #from string to int. This type hinting also handles errors nicely if user enters string instead
    # of numbers in the path parameter "id"
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with the id: {id}")

    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # print(post) #pydantic model (fields can be accessed like post.title etc..)
    # print(post.dict()) #converts pydantic model to dict and returns
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"message": post_dict} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")
        
    my_posts.pop(index)
    # the below return statement will not return the message as in FastAPI 204 status code implies
    # that you shouldn't return anything as you're removing sth. So we can return the Response instead
    # return {"message": f"Successfully removed post with id: {id}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id: {id}")
    
    updated_post = post.dict()
    updated_post['id'] = id
    my_posts[index] = updated_post
    
    return {"updated_post": updated_post}

    
    