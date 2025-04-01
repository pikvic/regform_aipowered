from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from ..database import SessionLocal, engine
from ..models import User
from ..config import settings

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/form", response_class=HTMLResponse)
async def form_page(request: Request):
    if "user_data" not in request.session:
        return RedirectResponse("/")
    return templates.TemplateResponse("form.html", {"request": request})

@router.post("/submit")
async def submit_form(
    request: Request,
    telegram: str = Form(...),
    vk: str = Form(...),
    db: Session = Depends(get_db)
):
    user_data = request.session.get("user_data")
    if not user_data:
        return RedirectResponse("/")
    
    user = User(
        fio=user_data["fio"],
        email=user_data["email"],
        telegram=telegram,
        vk=vk
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    request.session.pop("user_data")
    request.session["user_id"] = user.id
    
    return RedirectResponse("/success", status_code=303)

@router.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    return templates.TemplateResponse("success.html", {
        "request": request,
        "user_id": user_id
    })