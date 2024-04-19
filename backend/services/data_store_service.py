from fastapi import UploadFile
from fastapi.responses import JSONResponse
from models.data_store import Datastore
from schemas.data_store_schema import DatastoreCreate
from sqlalchemy.orm import Session
import pandas as pd
from pandas.errors import ParserError
from config.constant import (
    ERROR_MESSAGE_NOT_EXCEL_FILE, 
    SUCCESS_MESSAGE_FILE_UPLOAD, 
    ERROR_MESSAGE_GENERAL, 
    ERROR_MESSAGE_PANDAS_PARSER_FAIL)
from config import logger


backlog_gen_ai_chat_logger = logger.get_logger()

def upload_file(file: UploadFile, db: Session) -> JSONResponse:
    """
    Excelファイルをデータベースに保存する

    Parameters:
    - file: アップロードされたExcelファイル (fastapi.UploadFile)
    - db: データベースセッション (sqlalchemy.orm.Session)

    Returns:
    - JSONResponse: 合格または不合格のメッセージ (fastapi.responses.JSONResponse)
    """

    backlog_gen_ai_chat_logger.info('#### Action: upload_file ####')

    if not file.filename.endswith(".xlsx"):
        backlog_gen_ai_chat_logger.info(ERROR_MESSAGE_NOT_EXCEL_FILE)
        return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_NOT_EXCEL_FILE})

    try:
        # Excelファイルを読み込み、DataFrameに変換
        data_frame = pd.read_excel(file.file)

        # 保存用のオブジェクトリストを生成
        items = [
            Datastore(**DatastoreCreate(
                Keywords=row["Keywords"],
                Title=row["Title"],
                Source=row["Source"],
                Content=row["Content"],
                Category=row["Category"],
                IsUserForEmbedding=False
            ).model_dump()) for index, row in data_frame.iterrows()
        ]

        with db.begin():
            # データベースに保存
            db.bulk_save_objects(items)
            db.commit()

        backlog_gen_ai_chat_logger.info(SUCCESS_MESSAGE_FILE_UPLOAD)
        return JSONResponse(status_code=200, content={"message": SUCCESS_MESSAGE_FILE_UPLOAD})
    except ParserError as pe:
        # パーサーエラー
        db.rollback()
        pe_error_msg = ERROR_MESSAGE_PANDAS_PARSER_FAIL.format(reason=str(pe))
        backlog_gen_ai_chat_logger.info(pe_error_msg)
        return JSONResponse(status_code=400, content={"error": pe_error_msg})
    except Exception as e:
        # 一般エラー
        db.rollback()
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return JSONResponse(status_code=500, content={"error": e_error_msg})

