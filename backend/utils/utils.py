from config import logger
from config.constant import (
    LOG_MESSAGE_EMBEDDING_FOLDER_EXIST,
    LOG_MESSAGE_EMBEDDING_FOLDER_CREATED,
    EMBEDDING_FOLDER_NAME,
    EMBEDDING_MODEL_NAME,
    OPENAI_KEY,
    INPUT_UNIT_COST,
    OUTPUT_UNIT_COST)
import os
import uuid
from langchain_openai import OpenAIEmbeddings

backlog_gen_ai_chat_logger = logger.get_logger()

def get_embeddings_folder_path() -> str:
    """
    エンベディングフォルダのパスを取得します。

    Returns:
        str -- エンベディングフォルダのパス
    """
    # 現在のスクリプトのパスを取得
    current_script_path = os.path.realpath(__file__)
    # サービスディレクトリのパスを取得
    utils_directory = os.path.dirname(current_script_path)
    # バックエンドディレクトリのパスを取得
    backend_directory = os.path.dirname(utils_directory)
    # エンベディングフォルダのパスを作成
    embedding_folder_path = os.path.join(backend_directory, EMBEDDING_FOLDER_NAME)

    # エンベディングフォルダが存在するかどうかを確認し、ログを記録します
    if os.path.isdir(embedding_folder_path):
        backlog_gen_ai_chat_logger.info(LOG_MESSAGE_EMBEDDING_FOLDER_EXIST)
    else:
        # エンベディングフォルダが存在しない場合、作成してログを記録します
        os.mkdir(embedding_folder_path)
        backlog_gen_ai_chat_logger.info(LOG_MESSAGE_EMBEDDING_FOLDER_CREATED)

    return embedding_folder_path

def get_random_uuid_name():
    """
    ランダムなUUIDを生成して、ハイフンを削除した文字列を返します。

    Returns:
        str -- ハイフンが削除されたランダムなUUIDの文字列
    """
    return str(uuid.uuid4()).replace('-', '')

def get_embedding_model() -> OpenAIEmbeddings:
    """
    OpenAI Embedding modelを生成して返します。

    Returns:
        OpenAIEmbeddings -- OpenAI Embedding model
    """
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,  # OpenAIのモデル名
        openai_api_key=OPENAI_KEY,  # OpenAIのAPIキー
    )

def get_total_costs(prompt_tokens: int, completion_tokens: int) -> float:
    """
    完了タスクの合計コストを計算します。

    パラメータ:
        prompt_tokens (int): 入力トークン数
        completion_tokens (int): 出力トークン数

    戻り値:
        float: 完了タスクの合計コスト
    """
    if(prompt_tokens != None and completion_tokens != None):
        return INPUT_UNIT_COST * prompt_tokens + OUTPUT_UNIT_COST * completion_tokens
    else:
        return 0
