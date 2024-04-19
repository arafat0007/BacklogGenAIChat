from fastapi.responses import JSONResponse
from models.data_store import Datastore
from sqlalchemy.orm import Session
from config.constant import (
    ERROR_MESSAGE_GENERAL, 
    SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDING,
    OPENAI_KEY,
    EMBEDDING_MODEL_NAME,
    ERROR_MESSAGE_ZERO_CHUNKS,
    ERROR_MESSAGE_DATABASE_EXCEPTION,
    ERROR_MESSAGE_FAISS_EMBEDDING_SAVE_EXCEPTION,
    SUCCESS_MESSAGE_EMBEDDING_FILES_CREATION)
from config import logger
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from exceptions.general_exception import CustomGeneralException
from exceptions.database_exception import CustomDatabaseException
from utils.utils import get_embeddings_folder_path, get_random_uuid_name, get_embedding_model

backlog_gen_ai_chat_logger = logger.get_logger()

def create_embedding(db: Session) -> JSONResponse:
    """
    データストア内の新しいデータに対して、埋め込みを生成します。

    引数:
        db {Session} -- SQLAlchemyデータベースセッション

    戻り値:
        JSONResponse -- 成功または失敗を示すメッセージを含むJSONレスポンス
    """
    try:
        with db.begin():
            backlog_gen_ai_chat_logger.info('#### Action: create_embedding ####')

            # data storeから新規データを取得する。Embedding済みのデータは除外する
            data_store = db.query(Datastore).filter(Datastore.IsUserForEmbedding == False).order_by(Datastore.Id.desc()).all()

            # 新規データがない場合、成功メッセージを返す
            if not data_store:
                backlog_gen_ai_chat_logger.info(SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDING)
                return JSONResponse(status_code=200, content={"message": SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDING})

            # 新規データからDocumentリストを作成する
            document_list = []
            for data in data_store:
                content = data.Title + "\n" + data.Content
                document_list.append(Document(page_content=content, metadata={"Source": data.Source, "Title": data.Title, "Keywords": data.Keywords, "Category": data.Category}))

            # Documentをチャンクに分割する
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=256, chunk_overlap=32)
            document_chunks = text_splitter.split_documents(document_list)

            # チャンクが存在しない場合、エラーメッセージを返す
            chunks_length = len(document_chunks)
            if (chunks_length == 0):
                backlog_gen_ai_chat_logger.info(ERROR_MESSAGE_ZERO_CHUNKS)
                return JSONResponse(status_code=400, content={"error": ERROR_MESSAGE_ZERO_CHUNKS})

            # Embeddingフォルダのパスを取得する
            embeddings_folder_path = get_embeddings_folder_path()

            # OpenAI Embeddingモデルを作成する
            embedding_model = get_embedding_model()

            # Embeddingを作成する
            counter = 0
            temp_chunks = []

            # チャンク数が16を超える場合、16個ずつEmbeddingを作成する
            if (chunks_length > 16):
                for chunk in document_chunks:
                    temp_chunks.append(chunk)
                    counter += 1

                    if (counter == 16):
                        create_embeddings(temp_chunks, embedding_model, embeddings_folder_path)
                        counter = 0
                        temp_chunks.clear()

                # 最後のチャンクが残っている場合、Embeddingを作成する
                if (len(temp_chunks) > 0):
                    create_embeddings(temp_chunks, embedding_model, embeddings_folder_path)
                    temp_chunks.clear()

            # チャンク数が16未満の場合、すべてのチャンクのEmbeddingを作成する
            else:
                create_embeddings(temp_chunks, embedding_model, embeddings_folder_path)

            # data storeを更新して、新規データのEmbedding済みフラグをTrueにする
            bulk_update_data_store(db, data_store)

        return JSONResponse(status_code=200, content={"message": SUCCESS_MESSAGE_EMBEDDING_FILES_CREATION})

    except CustomDatabaseException as cde:
        db.rollback()
        e_error_msg = ERROR_MESSAGE_DATABASE_EXCEPTION.format(reason=str(cde))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return JSONResponse(status_code=500, content={"error": e_error_msg})

    except CustomGeneralException as cge:
        db.rollback()
        return JSONResponse(status_code=500, content={"error": cge.message})

    except Exception as e:
        db.rollback()
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        return JSONResponse(status_code=500, content={"error": e_error_msg})

def create_embeddings(chunks, embedding_model, embeddings_folder_path):
    """
    埋め込みを作成します。

    Arguments:
        chunks {List[Document]} -- ドキュメントのリスト
        embedding_model {OpenAIEmbeddings} -- 埋め込みモデル
        embeddings_folder_path {str} -- 埋め込みフォルダのパス

    Raises:
        CustomGeneralException: FAISSに関する例外が発生した場合に発生します
    """
    try:
        # ベクトルストアを作成します
        vector_store = FAISS.from_documents(chunks, embedding_model)
        # ランダムなUUIDを取得します
        index_name = get_random_uuid_name()
        # ローカルにベクトルストアを保存します
        vector_store.save_local(folder_path=embeddings_folder_path, index_name=index_name)
    except Exception as e:
        # FAISSに関する例外が発生した場合、CustomGeneralExceptionを発生させます
        raise CustomGeneralException(ERROR_MESSAGE_FAISS_EMBEDDING_SAVE_EXCEPTION.format(reason=str(e)))

def bulk_update_data_store(db: Session, data_store):
    """
    データストアを一括更新します。

    Arguments:
        db {Session} -- SQLAlchemyデータベースセッション
        data_store {List[Datastore]} -- 更新するデータのリスト

    Raises:
        CustomDatabaseException: データベースに関する例外が発生した場合に発生します
    """
    try:
        # データストアを一括更新します
        for data in data_store:
            data.IsUserForEmbedding = True
        db.bulk_save_objects(data_store)
        # トランザクションをコミットします
        db.commit()
    except Exception as e:
        # データベースに関する例外が発生した場合、CustomDatabaseExceptionを発生させます
        raise CustomDatabaseException()
