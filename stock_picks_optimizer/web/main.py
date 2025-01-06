from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kink import di

app = FastAPI()
templates = Jinja2Templates(directory=di["app_web_templates_path"])


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.jinja")
