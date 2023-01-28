from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
def get_posts():
    return {"message": "Wow!I have many posts!!!"}

@app.post("/createposts")
def create_post(body: dict = Body(...)):
    return {"message": body}