from fastapi import APIRouter, Depends, Request
from services import feedback_service
from config.session import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.session import get_db

router = APIRouter()

@router.post("/create_feedback")
async def create_feedback(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """チャットのフィードバックを作成する

    この関数は、チャットのフィードバックを作成します。

    パラメータ:
        request (fastapi.Request): HTTPリクエストオブジェクト
        db (sqlalchemy.orm.session.Session): データベースセッション

    戻り値:
        fastapi.responses.JSONResponse: フィードバック作成に成功したかどうかを示すメッセージ
    """
    data = await request.json()
    chat_id = data.get('chat_id')
    rating = data.get('rating')
    content = data.get('content')
    return feedback_service.create_feedback(chat_id, content, rating, db)


