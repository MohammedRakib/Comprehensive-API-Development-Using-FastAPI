from fastapi import Body, FastAPI
from pydantic_models import Post

app = FastAPI()

@app.get("/")
def root():
    return {"message": "WELCOME to the base routing link !!!"}

my_posts = [{"title": "POST-I", "body": "Blah 1", "rating": 7}, 
            {"title": "POST-II", "body": "Blah 2", "rating": 5}
            ]

@app.get("/posts")
def get_posts():
    return f"My posts are: {my_posts}"

@app.post("/posts")
def create_post(post: Post):
    # print(post.title)
    print(post) #pydantic model
    return {"message": post.dict()} #converts pydantic model to dict and returns
