from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from config import settings

app = FastAPI(title="Noctis Admin API")


class LoginRequest(BaseModel):
    api_key: str


def verify_token(authorization: str = Header(default="")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@app.post("/api/login")
async def login(req: LoginRequest):
    payload = {"sub": "admin", "exp": datetime.now(timezone.utc) + timedelta(hours=12)}
    return {"token": jwt.encode(payload, settings.jwt_secret, algorithm="HS256")}


@app.get("/api/chat/{chat_id}/stats")
async def chat_stats(chat_id: int, _: dict = Depends(verify_token)):
    return {"chat_id": chat_id, "messages": 0, "active_users": 0}


@app.get("/api/chat/{chat_id}/activity")
async def chat_activity(chat_id: int, _: dict = Depends(verify_token)):
    return {"chat_id": chat_id, "heatmap": []}


@app.get("/api/chat/{chat_id}/members")
async def chat_members(chat_id: int, page: int = 1, limit: int = 50, _: dict = Depends(verify_token)):
    return {"chat_id": chat_id, "page": page, "limit": limit, "members": []}


@app.post("/api/chat/{chat_id}/trigger")
async def create_trigger(chat_id: int, payload: dict, _: dict = Depends(verify_token)):
    return {"chat_id": chat_id, "trigger": payload, "status": "created"}


@app.get("/api/cas/check/{user_id}")
async def cas_check(user_id: int):
    return {"user_id": user_id, "is_spammer": False}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
