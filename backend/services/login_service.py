from config.constant import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    ERROR_MESSAGE_GENERAL,
    AUTHORIZE_URL,
    TOKEN_URL,
    ACCESS_URL,
    ERROR_INVALID_ACCESS_TOKEN,
    ERROR_EXPIRED_ACCESS_TOKEN)
from config import logger
from starlette.responses import RedirectResponse
from urllib.parse import urlencode
import httpx

backlog_gen_ai_chat_logger = logger.get_logger()

def login() -> RedirectResponse:
    """
    Backlog へのログインページへのリダイレクト処理。

    Backlog へのログインページへリダイレクトする処理を行います。

    Returns:
        RedirectResponse: Backlog ログインページへのリダイレクトレスポンス。
    """
    backlog_gen_ai_chat_logger.info('#### Action: login ####')
    try:  
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
        }

        url = AUTHORIZE_URL + "?" + urlencode(params)
        return RedirectResponse(url)

    except Exception as e:
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return RedirectResponse(url="http://localhost:3000/oauth_error")

async def authorize(code: str) -> RedirectResponse:
    """
    Backlog へのアクセストークンの発行処理。

    認可コードからアクセストークンを取得し、ユーザーのメールアドレスを取得します。

    Args:
        code (str): 認可コード

    Returns:
        RedirectResponse: ユーザーのメールアドレスをリダイレクトパラメータに含むリダイレクトレスポンス。
    """
    backlog_gen_ai_chat_logger.info('#### Action: authorize ####')
    backlog_gen_ai_chat_logger.info(f"code: {code}")

    try:  
        params = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # アクセストークンの取得
        async with httpx.AsyncClient() as client:
            response = await client.post(url=TOKEN_URL, data=params, headers=headers)

            if response.status_code == 200:
                reposense_json = response.json()
                access_token = reposense_json["access_token"]
                token_type = reposense_json["token_type"]
                expires_in = reposense_json["expires_in"]
                refresh_token = reposense_json["refresh_token"]
                backlog_gen_ai_chat_logger.info(f"access_token: {access_token}, token_type: {token_type}, expires_in: {expires_in}, refresh_token: {refresh_token}")
            else:
                e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(reposense_json.error_description))
                backlog_gen_ai_chat_logger.info(e_error_msg)
                raise Exception(e_error_msg)

        # ユーザーのメールアドレスの取得
        async with httpx.AsyncClient() as client:
            headers.update({'Authorization': f'{token_type} {access_token}'})
            response = await client.get(ACCESS_URL, headers=headers)

            if response.status_code == 200:
                reposense_json = response.json()
                backlog_gen_ai_chat_logger.info(f"reposense_json: {reposense_json}")
                email = reposense_json['mailAddress']
                return RedirectResponse(url=f"http://localhost:3000?email={email}")
            else:
                error_description = reposense_json.error_description
                if error_description == ERROR_INVALID_ACCESS_TOKEN:
                    backlog_gen_ai_chat_logger.info(ERROR_INVALID_ACCESS_TOKEN)
                    raise Exception(ERROR_MESSAGE_GENERAL.format(reason=ERROR_INVALID_ACCESS_TOKEN))
                elif error_description == ERROR_EXPIRED_ACCESS_TOKEN:
                    backlog_gen_ai_chat_logger.info(ERROR_EXPIRED_ACCESS_TOKEN)
                    raise Exception(ERROR_MESSAGE_GENERAL.format(reason=ERROR_EXPIRED_ACCESS_TOKEN))
                else:
                    e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(error_description))
                    backlog_gen_ai_chat_logger.info(e_error_msg)
                    raise Exception(e_error_msg)

    except Exception as e:
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return RedirectResponse(url="http://localhost:3000/oauth_error")
