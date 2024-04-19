from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.constant import (
    ERROR_MESSAGE_EMPTY_EMAIL,
    ERROR_MESSAGE_CHAT_CREATE,
    ERROR_MESSAGE_CHAT_NOT_FOUND,
    ERROR_MESSAGE_GENERAL)
from config import logger
from schemas.chat_schema import ChatCreate
from models.chat import Chat

backlog_gen_ai_chat_logger = logger.get_logger()

def create_chat(email: str, db: Session) -> JSONResponse:
    """
    チャットセッションを作成する

    パラメータ:
    - email: ユーザーのメールアドレス (str)
    - db: データベースセッション (sqlalchemy.orm.Session)

    戻り値:
    - JSONResponse: 作成されたチャットセッションのID (int) 
    """
    backlog_gen_ai_chat_logger.info('#### Action: create_chat ####')
    try:
        if email is None:
            return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_EMPTY_EMAIL})

        chat = Chat(**ChatCreate(User=email).model_dump())
        with db.begin():
            db.add(chat)
            db.commit()
        backlog_gen_ai_chat_logger.info(f"Chat created successfully with id {chat.Id}, User: {chat.User}")

        return JSONResponse(status_code=200, content={"chat_id": chat.Id})

    except Exception as e:
        db.rollback()
        e_error_msg = ERROR_MESSAGE_CHAT_CREATE.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return JSONResponse(status_code=500, content={"error": e_error_msg})
    
def get_chat(chat_id: int, db: Session) -> Chat:
    """
    指定されたIDのチャットをデータベースから取得します。

    引数:
        chat_id (int): チャットID
        db (Session): SQLAlchemyデータベースセッション

    戻り値:
        Chat: チャット

    例外:
        Exception: チャットが存在しない場合
    """
    backlog_gen_ai_chat_logger.info('#### Action: get_chat ####')
    try:
        chat = db.query(Chat).filter(Chat.Id == chat_id).first()
        if chat is None:
            error_msg = ERROR_MESSAGE_CHAT_NOT_FOUND.format(id=chat_id)
            backlog_gen_ai_chat_logger.info(error_msg)
            raise Exception(error_msg)
        return chat
    except Exception as e:
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        raise Exception(e_error_msg)
