from fastapi import APIRouter, Depends, Request
from services import message_service
from config.session import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.session import get_db

router = APIRouter()

@router.post("/get_messages")
async def get_messages(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """この関数は、指定されたチャットIDとメールアドレスに対応するメッセージを取得します。

    パラメータ:
        request (fastapi.Request): HTTPリクエストオブジェクト
        db (sqlalchemy.orm.session.Session): データベースセッション

    戻り値:
        fastapi.responses.JSONResponse: メッセージのJSON形式のリスト
    """
    chat_id = int(request.form["chat_id"])
    email = int(request.form["email"])

    # データベースからメッセージを取得
    messages = message_service.get_messages(chat_id, email, db)

    # JSON形式で返す
    return messages

