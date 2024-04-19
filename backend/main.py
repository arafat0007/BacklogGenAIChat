from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.data_store_router import router as data_store_router
from routers.embedding_router import router as embedding_router
from routers.user_query_router import router as user_query_router
from routers.chat_router import router as chat_router
from routers.message_router import router as message_router
from routers.feedback_router import router as feedback_router
from routers.login_router import router as login_router
from config.session import get_engine
from sqlalchemy.ext.declarative import declarative_base
from config.logger import init_logger

# ログの設定
init_logger()

# FastAPI インスタンスの作成
app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routesの追加
app.include_router(data_store_router)
app.include_router(embedding_router)
app.include_router(user_query_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(feedback_router)
app.include_router(login_router)

# データベーステーブルの作成
Base = declarative_base()
Base.metadata.create_all(bind=get_engine())