import openai
from config.constant import (
    OPENAI_KEY,
    COMPLETION_MODEL_NAME,
    COMPLETION_MODEL_TEMPERATURE,
    COMPLETION_MODEL_TOP_P,
    COMPLETION_MODEL_FREQUENCY_PENALTY,
    COMPLETION_MODEL_PRESENCE_PENALTY,
    COMPLETION_MODEL_N,
    TIKTOKEN_MODEL_NAME,
    ERR_MSG_OPEN_AI_API_ERROR,
    ERR_MSG_OPEN_AI_TIMEOUT,
    ERR_MSG_OPEN_AI_RATE_LIMIT_ERROR,
    ERR_MSG_OPEN_AI_API_CONNECTION_ERROR,
    ERR_MSG_OPEN_AI_OTHERS_ERROR,
    ERR_MSG_CONTENT_FILTER,
    ERR_MSG_TOKEN_LENGTH,
    ERR_MSG_CONTENT_NULL,
    DISP_MSG_OPEN_AI_RETRY,
    DISP_MSG_OPEN_AI_RATE_LIMIT,
    DISP_MSG_OPEN_AI_API_CONNECTION_ERROR,
    DISP_MSG_OPEN_AI_OTHERS_ERROR,
    DISP_MSG_TOKEN_LENGTH,
    DISP_MSG_CONTENT_FILTER,
    DISP_MSG_CONTENT_NULL)
import tiktoken
from config import logger
import time
from openai import OpenAI

backlog_gen_ai_chat_logger = logger.get_logger()

def call_completion_api_stream(message_list):
    """
     OpenAIのコンプリートAPIを呼び出す。
     このメソッドはstream=Trueを使って処理を高速化し、メモリ使用量を下げる。
 
     Parameters:
         message_list (list): OpenAI APIに送信するメッセージのリスト
 
     Yields:
         dict: レスポンステキスト、プロンプトトークン数、コンプリーショントークン数、総トークン数、レスポンスタイム、has_errorフィールドを含む辞書
     """
    result = {
        'response_text' : '',
        'prompt_tokens' : 0,
        'completion_tokens' : 0,
        'total_tokens' : 0,
        'response_time' : 0,
        'has_error' : False
    }

    start_time = time.time()
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0

    client = OpenAI(api_key=OPENAI_KEY)

    try:
        response = client.chat.completions.create(
            model = COMPLETION_MODEL_NAME,
            messages = message_list,
            temperature = COMPLETION_MODEL_TEMPERATURE,
            top_p = COMPLETION_MODEL_TOP_P,
            frequency_penalty = COMPLETION_MODEL_FREQUENCY_PENALTY,
            presence_penalty = COMPLETION_MODEL_PRESENCE_PENALTY,
            n = COMPLETION_MODEL_N,
            stream = True
        )

        response_text = ''
        for chunk in response:
            if chunk:
                content = chunk.choices[0].delta.content
                if content:
                    response_text += content
                    result['response_text'] = content
                    yield result
                else:
                    result['response_text'] = ''
                    yield result

        prompt_tokens = get_token_count(get_message_list_as_string(message_list))
        completion_tokens = get_token_count(response_text)
        total_tokens = prompt_tokens + completion_tokens
        
        finish_reason = get_finish_reason(chunk)

        if(finish_reason == 'stop'):
            result['prompt_tokens'] = prompt_tokens
            result['completion_tokens'] = completion_tokens
            result['total_tokens'] = total_tokens
        elif(finish_reason == 'length'):
            err_msg = ' ' + DISP_MSG_TOKEN_LENGTH
            set_error_info(result, ERR_MSG_TOKEN_LENGTH, err_msg)
        elif(finish_reason == 'content_filter'):
            err_msg = ' ' + DISP_MSG_CONTENT_FILTER
            set_error_info(result, ERR_MSG_CONTENT_FILTER, err_msg)
        elif(finish_reason == 'null'):
            err_msg = ' ' + DISP_MSG_CONTENT_NULL
            set_error_info(result, ERR_MSG_CONTENT_NULL, err_msg)
        
    except openai.APIError as e:
        set_error_info(result,  ERR_MSG_OPEN_AI_API_ERROR, "APIError : " + DISP_MSG_OPEN_AI_RETRY, e)
    except openai.Timeout as e:
        set_error_info(result,  ERR_MSG_OPEN_AI_TIMEOUT, "Timeout : " + DISP_MSG_OPEN_AI_RETRY, e)
    except openai.RateLimitError as e:
        set_error_info(result,  ERR_MSG_OPEN_AI_RATE_LIMIT_ERROR, "RateLimitError : " + DISP_MSG_OPEN_AI_RATE_LIMIT, e)
    except openai.APIConnectionError as e:
        set_error_info(result,  ERR_MSG_OPEN_AI_API_CONNECTION_ERROR, "APIConnectionError : " + DISP_MSG_OPEN_AI_API_CONNECTION_ERROR, e)
    except openai.InvalidRequestError as e:
        set_error_info(result,  ERR_MSG_OPEN_AI_OTHERS_ERROR, "InvalidRequestError : " + DISP_MSG_OPEN_AI_OTHERS_ERROR, e) 
    except Exception as e:
        set_error_info(result,  ERR_MSG_OPEN_AI_OTHERS_ERROR, "Exception : " + DISP_MSG_OPEN_AI_OTHERS_ERROR, e)
    finally:
        result['prompt_tokens'] = prompt_tokens
        result['completion_tokens'] = completion_tokens
        result['total_tokens'] = total_tokens
        end_time = time.time()
        response_time = end_time - start_time
        result['response_time'] = response_time
        yield result

def get_token_count(string):
    """
    この関数は文字列を受け取り、その文字列に含まれるトークン数を返します。
    TikTok AIモデルのエンコーディングを取得するencoding_for_model関数を使用し、
    そのエンコーディングのencode関数を使用して、入力文字列からトークンを取得します。

    Args:
        string (str): トークン数を数える文字列

    Returns:
        int: 入力文字列に含まれるトークン数

    Raises:
        Exception: encoding_for_modelまたはencodeでエラーが発生した場合
    """
    try:
        encoding = tiktoken.encoding_for_model(TIKTOKEN_MODEL_NAME)
        tokens = encoding.encode(string)
        return len(tokens)
    except Exception as e:
        backlog_gen_ai_chat_logger.info(str(e))
        raise Exception(str(e))
    
def get_message_list_as_string(message_list):
    """
    この関数はメッセージのリストを受け取り、そのメッセージを1つの文字列にして返します。

    各メッセージは "{role} : {content}" の形式です。

    Args:
        message_list (list[dict]): メッセージのリスト。各メッセージはroleとcontentの2つのキーを持つ辞書型です。

    Returns:
        str: すべてのメッセージを "{role} : {content}" の形式で連結した文字列。
    """
    message_string = ''
    for message in message_list:
        role = message['role']
        content = message['content']
        message_string = f"{message_string} \n {role} : {content}"
    return message_string

def get_finish_reason(chunk):
    """
    最初の選択肢のfinish_reasonを取得します。

    Args:
        chunk (CompletionChunk): finish_reasonを取得するチャンク。

    Returns:
        str: 最初の選択肢のfinish_reason。

    Raises:
        Exception: チャンクに選択肢がない場合、または最初の選択肢のfinish_reasonを取得する際に問題が発生した場合。
    """
    try:
        return chunk.choices[0].finish_reason
    except Exception as e:
        backlog_gen_ai_chat_logger.info(str(e))
        raise Exception(str(e))


    
def set_error_info(result, err_msg, disp_msg, exception = None):
    """
     エラー情報をresultに設定します。
 
     パラメータ:
         result (dict): 更新対象のresult
         エラーメッセージ (str): エラーメッセージ
         表示メッセージ (str): 表示メッセージ
         例外 (Exception): 例外が発生した場合
 
     戻り値:
         dict: エラー情報が設定された更新済みのresult
     """
    backlog_gen_ai_chat_logger.info(type(err_msg), type(disp_msg), type(exception))
    backlog_gen_ai_chat_logger.info(err_msg)
    if(exception is not None):
        backlog_gen_ai_chat_logger.info(exception)
    result['response_text'] = disp_msg
    result['has_error'] = True
