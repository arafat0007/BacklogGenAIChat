from fastapi import APIRouter, Depends
from services import embedding_service
from config.session import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.session import get_db

router = APIRouter()

@router.get("/create_embedding")
async def create_embedding(db: Session = Depends(get_db)) -> JSONResponse:
    """データベースに新しいデータがある場合、埋め込みファイルを生成してファイルシステムに保存する

    この関数は、データベースに新しいデータがある場合、埋め込みファイルを生成してファイルシステムに保存します。

    パラメータ:
        db (sqlalchemy.orm.session.Session): データベースセッション

    戻り値:
        fastapi.responses.JSONResponse: 埋め込みファイルの生成に成功したかどうかを示すメッセージ
    """
    return embedding_service.create_embedding(db)
