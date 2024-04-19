from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import constant
from typing import Iterator
from sqlalchemy.orm import Session
import sqlalchemy

SQLALCHEMY_DATABASE_URL = constant.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Iterator[Session]:
    """
    データベースセッションを取得する

    この機能はパラメータを受け取りません

    Yields:
        db (sqlalchemy.orm.session.Session): データベースセッション

    Returns:
        なし
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        db.close()

def get_engine() -> sqlalchemy.engine.Engine:
    """
    データベース接続に使用するエンジンオブジェクトを返す機能

    この機能はパラメータを受け取りません。

    返り値:
        engine (sqlalchemy.engine.Engine): エンジンオブジェクト
    """
    return engine
