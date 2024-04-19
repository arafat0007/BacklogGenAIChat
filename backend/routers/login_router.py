from fastapi import APIRouter, Query
from services import login_service
from starlette.responses import RedirectResponse

router = APIRouter()

@router.get("/login")
async def login() -> RedirectResponse:
    """Backlog へのログインページへのリダイレクト処理。

    Backlog へのログインページへリダイレクトする処理を行います。

    Returns:
        RedirectResponse: Backlog ログインページへのリダイレクトレスポンス。
    """
    return login_service.login()


@router.get("/oauth_code")
async def authorize(code: str = Query(...)) -> RedirectResponse:
    """Backlog の認証コードを受け取り、アクセストークンを取得する処理。

    Backlog の認証コードを受け取り、アクセストークンを取得する処理を行います。
    取得したアクセストークンをセッションに保存します。

    Args:
        code (str): Backlog から受け取る認証コード

    Returns:
        RedirectResponse: トップページへのリダイレクトレスポンス。
    """
    return await login_service.authorize(code)





