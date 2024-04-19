from fastapi import APIRouter, Depends, Request
from services import chat_service
from config.session import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.session import get_db

router = APIRouter()

@router.post("/create_chat")
async def create_chat(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """新しいチャットを作成する

    この関数は、新しいチャットを作成します。

    パラメータ:
        request (fastapi.Request): HTTPリクエストオブジェクト
        db (sqlalchemy.orm.session.Session): データベースセッション

    戻り値:
        fastapi.responses.JSONResponse: チャット作成に成功したかどうかを示すメッセージ
    """
    data = await request.json()
    email = data.get('email')
    return chat_service.create_chat(email, db)


