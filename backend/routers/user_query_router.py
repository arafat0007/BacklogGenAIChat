from fastapi import APIRouter, Depends, Response, Request
from fastapi.responses import StreamingResponse
from services import user_query_service
from config.session import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.session import get_db

router = APIRouter()

@router.post("/query")
async def get_query_answer(
    request: Request, response: Response, db: Session = Depends(get_db)
) -> JSONResponse:
    """ユーザーのクエリに対するJSONレスポンスのストリームを返す

    この関数は、ユーザーのクエリに対するJSONレスポンスのストリームを返すFastAPIエンドポイントです。
    この関数はまず、リクエストとデータベースセッションから必要な情報を抽出します。次に、ユーザークエリサービスを使用してJSONレスポンスのストリームを生成します。
    最後に、生成されたストリームをyieldして返し、応答のcontent-typeをtext/event-streamに設定します。

    引数:
        request (fastapi.Request): HTTPリクエストオブジェクト
        response (fastapi.Response): HTTPレスポンスオブジェクト
        db (sqlalchemy.orm.session.Session): データベースセッション

    戻り値:
        fastapi.responses.JSONResponse: ユーザークエリサービスからのJSONレスポンスのストリーム
    """
    def generate():
        """ユーザークエリサービスからJSONレスポンスのストリームを生成する

        この関数はユーザークエリサービスを使用してJSONレスポンスのストリームを生成します。
        この関数はまず、リクエストとデータベースセッションから必要な情報を抽出します。次に、ユーザークエリサービスを使用してJSONレスポンスを生成します。
        最後に、生成されたJSONレスポンスをyieldして返します。

        Yields:
            str: ユーザークエリサービスからのJSONレスポンス
        """
        for json_response in user_query_service.get_query_answer(chat_id, email, query, db):
            yield json_response.body.decode("utf-8")

    data = await request.json()
    chat_id = data.get('chat_id')
    query = data.get('query')
    email = data.get('email')
    response.headers['content-type'] = 'text/event-stream'
    return StreamingResponse(generate())



