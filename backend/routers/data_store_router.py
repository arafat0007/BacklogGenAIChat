from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from config.session import get_db
from services import data_store_service
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Excelファイルをアップロードし、データベースに保存する

    パラメータ:
    - file (UploadFile): アップロードされたExcelファイル
    - db (sqlalchemy.orm.session.Session): データベースセッション

    戻り値:
    - JSONResponse: アップロードの成否を示すメッセージ
    """

    return data_store_service.upload_file(file, db)
