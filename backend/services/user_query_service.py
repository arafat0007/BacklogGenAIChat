from fastapi.responses import JSONResponse
from models.message import Message
from models.message_log import MessageLog
from sqlalchemy.orm import Session
from config.constant import (
    ERROR_MESSAGE_GENERAL,
    ERROR_MESSAGE_FAISS_VECTORSTORE_LOAD_EXCEPTION,
    ERROR_MESSAGE_EMPTY_QUERY,
    NO_OF_SIMILAR_DOCUMENTS,
    ERROR_MESSAGE_EMPTY_CHATID,
    CODES_TO_CHAT_LANGUAGE,
    DEFAULT_CHAT_LANGUAGE,
    USER_MESSAGE_TYPE,
    ASSISTANT_MESSAGE_TYPE,
    COMPLETION_MODEL_NAME,
    ERROR_MESSAGE_EMPTY_EMAIL)
from config import logger
import os
from langchain_community.vectorstores import FAISS
from exceptions.general_exception import CustomGeneralException
from utils.utils import get_embeddings_folder_path, get_embedding_model, get_total_costs
from config.prompt import get_chat_prompt, SYSTEM_PROMPT
from langdetect import detect
from services.openai_service import call_completion_api_stream
from services.chat_service import get_chat

backlog_gen_ai_chat_logger = logger.get_logger()

def get_query_answer(chat_id: int, email: str, query: str, db: Session): 
    """
    この関数はモデルからクエリに対する回答を取得するために使用されます。
    この関数は以下の処理を行います。
    1. queryとchat_idとメールの全てがNoneでないかをチェック
    2. 両方がNoneでない場合はベクトルストアを取得し、クエリに対する類似度の高いドキュメントを検索する
    3. 指定されたchat_idのメッセージをデータベースから取得する
    4. クエリから言語を検出する
    5. システムプロンプト、メッセージのリスト、クエリのコンテンツを含むメッセージのリストを作成する
    6. 作成したメッセージリストをopenai completion apiを呼び出す
    7. レスポンスをパースし、ユーザーメッセージとアシスタントメッセージをデータベースに追加する
    8. メッセージログを作成しデータベースに追加する
 
    Parameters:
        chat_id (int): クエリが出されたチャットのID
        query (str): ユーザーが出したクエリ
        db (Session): データベースのセッション
 
    Returns:
         JSONResponse: 回答またはエラーメッセージを含むJSONレスポンスを返す
    """
    try:
        backlog_gen_ai_chat_logger.info('#### Action: get_query_answer ####')
        if query is None:
            yield JSONResponse(status_code=400, content={'status' : 'answer','error': ERROR_MESSAGE_EMPTY_QUERY})

        if email is None:
            yield JSONResponse(status_code=400, content={'status' : 'answer','error': ERROR_MESSAGE_EMPTY_EMAIL})
        
        elif chat_id is None:
            yield JSONResponse(status_code=400, content={'status' : 'answer','error': ERROR_MESSAGE_EMPTY_CHATID})

        else:
            with db.begin():
                vector_store = get_vector_store()
                yield JSONResponse(status_code=200, content={'status' : 'processing','message': 'Searching for relevant data'})
                similarity_search_result = vector_store.similarity_search(query=query, k=NO_OF_SIMILAR_DOCUMENTS)

                # データベースからチャットを取得する
                chat = get_chat(chat_id, db)
                # データベースからメッセージを取得する
                messages = db.query(Message).filter(Message.ChatId == chat_id and chat.User == email).all()

                code = detect(query)
                if(code in CODES_TO_CHAT_LANGUAGE):
                    language = CODES_TO_CHAT_LANGUAGE[code]
                else:
                    language = DEFAULT_CHAT_LANGUAGE

                message_list = []
                message_list.append({'role':'system', 'content':SYSTEM_PROMPT})

                for message in messages:
                    message_list.append({'role':message.Type, 'content':message.Content})

                query_content = get_chat_prompt(language=language, context=similarity_search_result, query=query)
                message_list.append({'role':'user', 'content':query_content})

                backlog_gen_ai_chat_logger.info(f"message_list: {message_list}")

                response_content = ''
                yield JSONResponse(status_code=200, content={'status' : 'processing','message': 'Create a response'})
                for result in call_completion_api_stream(message_list):
                    response_text = result['response_text']
                    response_content += response_text
                    prompt_tokens = result['prompt_tokens']
                    completion_tokens = result['completion_tokens']
                    total_tokens = result['total_tokens']
                    response_time = result['response_time']
                    has_error = result['has_error']
                    if(response_text != ''):
                        yield JSONResponse(status_code=200, content={'status' : 'answer','message': response_text})

                total_cost = get_total_costs(prompt_tokens, completion_tokens)
                backlog_gen_ai_chat_logger.info(f"response: {response_content}")
                backlog_gen_ai_chat_logger.info(f"Query Log: prompt_tokens:{prompt_tokens}, completion_tokens:{completion_tokens}, total_tokens:{total_tokens}, total_cost:{total_cost}, response_time:{response_time}, has_error:{has_error}")

                user_message = Message(ChatId=chat_id, Type=USER_MESSAGE_TYPE, Content=query)
                assistant_message = Message(ChatId=chat_id, Type=ASSISTANT_MESSAGE_TYPE, Content=response_content)
                db.add_all([user_message, assistant_message])
                db.flush()
                message_log = MessageLog(MessageId=user_message.Id, Model=COMPLETION_MODEL_NAME, PromptTokens=prompt_tokens, CompletionTokens=completion_tokens, TotalTokens=total_tokens, TotalCost=total_cost, ResponseTime=response_time, HasError=has_error)
                db.add(message_log)
                db.commit()

    except CustomGeneralException as cge:
        db.rollback()
        yield JSONResponse(status_code=200, content={'status' : 'answer','message': cge.message})
    
    except Exception as e:
        db.rollback()
        e_error_msg = ERROR_MESSAGE_GENERAL.format(reason=str(e))
        backlog_gen_ai_chat_logger.info(e_error_msg)
        yield JSONResponse(status_code=200, content={'status' : 'answer','message': e_error_msg})
    
def get_vector_store():
    """
    エンコーディングフォルダからベクトルストアを読み込みます。

    この関数は、エンコーディングフォルダにあるインデックスファイルをすべて読み込み、1つのベクトルストアにマージします。

    読み込まれたベクトルストアを返します。

    Args:
        なし

    Returns:
        FAISS.VectorStore: マージされたベクトルストア

    Raises:
        CustomGeneralException: ベクトルストアの読み込み時にエラーが発生した場合に発生
    """
    try:
        embeddings_folder_path = get_embeddings_folder_path()
        file_names = next(os.walk(embeddings_folder_path))[2]
        file_names_without_extension = [os.path.splitext(file_name)[0] for file_name in file_names]
        file_names_without_duplicates = list(set(file_names_without_extension))

        for index in range(len(file_names_without_duplicates)):
            file_name = file_names_without_duplicates[index]
            temp_vector_store = FAISS.load_local(folder_path=embeddings_folder_path, index_name=file_name, embeddings=get_embedding_model(), allow_dangerous_deserialization=True)
            if(index == 0):
                vector_store = temp_vector_store
            else:
                vector_store.merge_from(temp_vector_store)

        return vector_store

    except Exception as e:
        raise CustomGeneralException(ERROR_MESSAGE_FAISS_VECTORSTORE_LOAD_EXCEPTION.format(reason=str(e)))
