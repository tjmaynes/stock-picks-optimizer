import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kink import di

from stock_picks_optimizer.core.domain.models import StockGroup
from stock_picks_optimizer.core.use_cases import (
    OptimizeStockGroupsUseCase,
    FetchAllStockGroupsUseCase,
    AddStockGroupUseCase,
)
from stock_picks_optimizer.web.models import AddStockGroup

app = FastAPI()
templates = Jinja2Templates(directory=di["app_web_templates_path"])

app.mount("/static", StaticFiles(directory=di["app_web_static_path"]), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.j2")


@app.get("/new", response_class=HTMLResponse)
async def new(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="new.j2")


@app.get("/groups", response_class=HTMLResponse)
async def groups(request: Request) -> HTMLResponse:
    stock_groups = di[FetchAllStockGroupsUseCase].invoke()
    optimized_stock_groups = di[OptimizeStockGroupsUseCase].invoke(stock_groups)
    return templates.TemplateResponse(
        request=request,
        name="partials/show_groups.j2",
        context={"stock_groups": optimized_stock_groups},
    )


@app.get("/groups/add", response_class=HTMLResponse)
async def add_group(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="new.j2")


@app.get("/partials/groups/pick/add", response_class=HTMLResponse)
async def add_pick(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="partials/add_pick_section.j2"
    )


@app.get("/partials/groups/pick/remove", response_class=HTMLResponse)
async def remove_pick(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="partials/add_pick_section.j2"
    )


@app.get("/partials/groups/cancel_add", response_class=HTMLResponse)
async def cancel_add(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="partials/show_group_form.j2"
    )


@app.post("/groups/add")
async def post_add_group(stock_group: AddStockGroup) -> StockGroup:
    return di[AddStockGroupUseCase].invoke(
        stock_group.name, stock_group.budget, stock_group.picks
    )


def run(port: int = 8000, reload: bool = False) -> None:
    uvicorn.run(
        "stock_picks_optimizer.web.main:app", host="0.0.0.0", port=port, reload=reload
    )


if __name__ == "__main__":
    run()
