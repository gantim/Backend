from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Подключение статических файлов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение шаблонов Jinja2
templates = Jinja2Templates(directory="templates")

# Главная страница
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})