from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.user.router import router as router_user

app = FastAPI()

app.include_router(router_user)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})