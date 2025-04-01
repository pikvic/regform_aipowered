from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .config import settings
from .routers import auth, form

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="session"
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(form.router)

@app.get("/")
async def root(request: Request):
    if "user_data" in request.session:
        return templates.TemplateResponse("form.html", {"request": request})
    return templates.TemplateResponse("login.html", {"request": request})