from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.constant import (
    ERROR_MESSAGE_EMPTY_CHATID,
    ERROR_MESSAGE_EMPTY_RATING,
    ERROR_MESSAGE_GENERAL)
from config import logger
from schemas.feedback_schema import FeedbackCreate
from models.feedback import Feedback

backlog_gen_ai_chat_logger = logger.get_logger()

def create_feedback(chat_id: int, content: str, rating: int, db: Session) -> JSONResponse:
    """
    新規のフィードバックをデータベースに登録する

    パラメータ:
    - chat_id: フィードバックが属するチャットのID (int)
    - content: フィードバックの内容 (str)
    - rating: フィードバックの評価値 (1-10) (int)
    - db: データベースセッション (sqlalchemy.orm.Session)

    戻り値:
    - JSONResponse: 作成されたフィードバックのID (int) 
    """
    backlog_gen_ai_chat_logger.info('#### Action: create_feedback ####')
    try:
        # 入力を検証する
        if chat_id is None:
            return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_EMPTY_CHATID})
        if rating <= 0 or rating > 10:
            return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_EMPTY_RATING})

        # フィードバックを作成する
        feedback = Feedback(**FeedbackCreate(ChatId=chat_id, Content=content, Rating=rating).model_dump())

        # データベースにフィードバックを登録する
        with db.begin():
            db.add(feedback)
            db.commit()
        backlog_gen_ai_chat_logger.info(f"Feedback created successfully with id {feedback.Id}, ChatId: {feedback.ChatId}, Content: {feedback.Content}, Rating: {feedback.Rating}")

        return JSONResponse(status_code=200, content={"feedback_id": feedback.Id})

    except Exception as e:
        db.rollback()
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return JSONResponse(status_code=500, content={"error": e_error_msg})
