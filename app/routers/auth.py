from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode

from ..config import settings

router = APIRouter()

YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"

@router.get("/auth")
async def auth_yandex():
    params = {
        "response_type": "code",
        "client_id": settings.yandex_client_id,
        "redirect_uri": "http://localhost:8000/callback"
    }
    return RedirectResponse(YANDEX_AUTH_URL + "?" + urlencode(params))

@router.get("/callback")
async def callback(code: str, request: Request):
    # Exchange code for token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.yandex_client_id,
        "client_secret": settings.yandex_client_secret
    }
    
    response = requests.post(YANDEX_TOKEN_URL, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid code")
    
    access_token = response.json()["access_token"]
    
    # Get user info
    user_info = requests.get(
        YANDEX_USER_INFO_URL,
        params={"format": "json"},
        headers={"Authorization": f"OAuth {access_token}"}
    ).json()
    
    request.session["user_data"] = {
        "fio": user_info.get("real_name"),
        "email": user_info.get("default_email")
    }
    
    return RedirectResponse("/form")