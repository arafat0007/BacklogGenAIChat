from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.constant import (
    ERROR_MESSAGE_EMPTY_CHATID,
    ERROR_MESSAGE_GENERAL,
    ERROR_MESSAGE_EMPTY_EMAIL)
from config import logger
from models.message import Message
from services.chat_service import get_chat

backlog_gen_ai_chat_logger = logger.get_logger()

def get_messages(chat_id: int, email: str, db: Session) -> JSONResponse:
    """
    チャットのメッセージを取得する

    Args:
        chat_id (int): チャットID
        db (Session): データベースセッション
        email (str): メールアドレス

    Returns:
        JSONResponse: メッセージのリスト
    """
    backlog_gen_ai_chat_logger.info('#### Action: get_messages ####')
    try:
        # 入力を検証する
        if chat_id is None:
            return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_EMPTY_CHATID})
        
        if email is None:
            return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_EMPTY_EMAIL})

        # データベースからチャットを取得する
        chat = get_chat(chat_id, db)
        
        # データベースからメッセージを取得する
        messages = db.query(Message).filter(Message.ChatId == chat_id and chat.User == email).all()

        # メッセージをJSON形式に変換する
        messages_json = []
        for msg in messages:
            messages_json.append(
                {
                    "Id": msg.Id,
                    "ChatId": msg.ChatId,
                    "Type": msg.Type,
                    "Content": msg.Content,
                    "Created": msg.CreateDate
                }
            )

        # JSONレスポンスを返す
        return JSONResponse(status_code=200, content={"messages": messages_json})

    except Exception as e:
        db.rollback()
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return JSONResponse(status_code=500, content={"error": e_error_msg})

