import datetime
from http import HTTPStatus

from fastapi import FastAPI
from pydantic.v1 import BaseModel
from starlette.responses import Response, HTMLResponse, PlainTextResponse
from starlette.requests import Request

app = FastAPI()

@app.get("/ping", response_model=PlainTextResponse)
def ping_pong():
    return PlainTextResponse(content="pong", status_code=200)
@app.get("/home", response_model=HTMLResponse)
def welcome_home():
    with open("welcome_home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

@app.exception_handler(404)
def error(request: Request):
    return HTMLResponse(content="404 NOT FOUND")

class PostDetails(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

posts_memorized: list[PostDetails]
@app.post("/posts", status_code=201)
def create_post(new_posts: list[PostDetails]):
    posts_memorized.extend(new_posts)

@app.get("/posts")
def list_of_posts():
    return Response(content=posts_memorized, status_code=200)

