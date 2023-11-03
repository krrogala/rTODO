from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


@app.get("/hello/")
def hello_world():
    return "Hello world"
