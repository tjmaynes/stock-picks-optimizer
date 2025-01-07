import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kink import di

app = FastAPI()
templates = Jinja2Templates(directory=di["app_web_templates_path"])

app.mount("/static", StaticFiles(directory=di["app_web_static_path"]), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.jinja")


@app.get("/add-group", response_class=HTMLResponse)
def add_group(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="add-group.jinja")


def run(port: int = 8000, reload: bool = False) -> None:
    uvicorn.run(
        "stock_picks_optimizer.web.main:app", host="0.0.0.0", port=port, reload=reload
    )


if __name__ == "__main__":
    run()
