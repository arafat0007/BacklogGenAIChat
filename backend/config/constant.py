from dotenv import load_dotenv
import os

load_dotenv()

# oauth2
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
AUTHORIZE_URL = "https://nulab-exam.backlog.jp/OAuth2AccessRequest.action"
TOKEN_URL = "https://nulab-exam.backlog.jp/api/v2/oauth2/token"
ACCESS_URL = "https://nulab-exam.backlog.jp/api/v2/users/myself"


# Database
DATABASE_URL = os.environ.get('DATABASE_URL')

# Openai
OPENAI_KEY = os.environ.get('OPENAI_KEY')
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
COMPLETION_MODEL_NAME = "gpt-4-0125-preview"
COMPLETION_MODEL_TEMPERATURE = 0.7
COMPLETION_MODEL_TOP_P = 0.95
COMPLETION_MODEL_FREQUENCY_PENALTY = 0
COMPLETION_MODEL_PRESENCE_PENALTY = 0
COMPLETION_MODEL_N = 1
TIKTOKEN_MODEL_NAME = 'gpt-3.5-turbo'

# Openai messages
ERR_MSG_OPEN_AI_API_ERROR = 'APIError: Issue on OpenAI side.'
ERR_MSG_OPEN_AI_TIMEOUT = 'Timeout: Request timed out.'
ERR_MSG_OPEN_AI_RATE_LIMIT_ERROR = 'RateLimitError: You have hit your assigned rate limit.'
ERR_MSG_OPEN_AI_API_CONNECTION_ERROR = 'APIConnectionError: Issue connecting to OpenAI services.'
ERR_MSG_OPEN_AI_OTHERS_ERROR = 'Open AI Error: Issue on OpenAI servers.'
ERR_MSG_CONTENT_FILTER = 'FINISH REASON: content_filter:: The content filtering detects specific categories of potentially harmful.'
ERR_MSG_TOKEN_LENGTH = 'FINISH REASON:: length: Incomplete model output due to limit of chat\'s length.'
ERR_MSG_CONTENT_NULL = 'FINISH REASON: null: Response of N-CHAT still in progress or incomplete.'
DISP_MSG_OPEN_AI_RETRY = 'Retry sending the message again after a brief wait.'
DISP_MSG_OPEN_AI_RATE_LIMIT = 'Pace your requests more slowly.'
DISP_MSG_OPEN_AI_API_CONNECTION_ERROR = 'Retry sending the message again after a brief wait and contact if the issue persists.'
DISP_MSG_OPEN_AI_OTHERS_ERROR = 'There was a connection issue with Azure Open AI. Retry sending the message again after a brief wait.'
DISP_MSG_TOKEN_LENGTH = 'Incomplete model output due to limit of chat\'s length.'
DISP_MSG_CONTENT_FILTER = 'The content filtering detects specific categories of potentially harmful.'
DISP_MSG_CONTENT_NULL = 'Response of N-CHAT still in progress or incomplete.'
DISP_MSG_LONG_INPUT = 'This message is too long. Retry sending a shorter message.'
DISP_MSG_OVER_CHAT_LIMIT = 'This chat is too long history. Plese create a new chat.'

# Openai Model Unit Cost
INPUT_UNIT_COST = 0.00001
OUTPUT_UNIT_COST = 0.00003

# logger
LOGGER_NAME = 'BacklogGenAIChat'
LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGER_PATH = './app_log/'
LOGGER_FILE = 'BacklogGenAIChat.log'
LOGGER_ROTATING_SUFFIX = '%Y-%m-%d'
LOGGER_ENCODING = 'UTF-8'
LOGGER_ROTATE_TIMING = 'MIDNIGHT'
LOGGER_3_MONTHS = 90

# embedding
EMBEDDING_FOLDER_NAME = 'embeddings'

# return messages
ERROR_MESSAGE_NOT_EXCEL_FILE = "Only Excel files are allowed."
ERROR_MESSAGE_GENERAL = "An error occurred. {reason}"
ERROR_MESSAGE_PANDAS_PARSER_FAIL = "Pandas parser error. {reason}"
ERROR_MESSAGE_ZERO_CHUNKS = "Chunk size can not be zero."
ERROR_MESSAGE_DATABASE_EXCEPTION = "Database exception occurred. {reason}"
ERROR_MESSAGE_FAISS_EMBEDDING_SAVE_EXCEPTION = "Error on saving embedding file using FAISS. {reason}"
ERROR_MESSAGE_FAISS_VECTORSTORE_LOAD_EXCEPTION = "Error on loading vectorstore using FAISS. {reason}"
ERROR_MESSAGE_EMPTY_QUERY = "Query can not be empty."
ERROR_MESSAGE_EMPTY_CHATID = "Chat ID can not be empty."
ERROR_MESSAGE_CHAT_NOT_FOUND = "Chat with id {id} not found."
ERROR_MESSAGE_EMPTY_RATING = "Rating must be in range between 1 and 10."
ERROR_MESSAGE_EMPTY_EMAIL = "Email can not be empty."
ERROR_MESSAGE_CHAT_CREATE = "Chat creation failed. {reason}"
ERROR_INVALID_ACCESS_TOKEN = "The access token is invalid"
ERROR_EXPIRED_ACCESS_TOKEN = "The access token expired"
SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDING = "No new data for embedding."
SUCCESS_MESSAGE_FILE_UPLOAD = "File uploaded successfully."
SUCCESS_MESSAGE_EMBEDDING_FILES_CREATION = "Embedding files are successfully created."

# log messages
LOG_MESSAGE_EMBEDDING_FOLDER_EXIST = "Embedding folder path exists."
LOG_MESSAGE_EMBEDDING_FOLDER_CREATED = "Embedding folder created."

# message type
USER_MESSAGE_TYPE = 'user'
ASSISTANT_MESSAGE_TYPE = 'assistant'

# vector store
NO_OF_SIMILAR_DOCUMENTS = 32

# langdetect supported languages
CODES_TO_CHAT_LANGUAGE = {
    'af': 'AFRIKAANS',
    'ar': 'ARABIC',
    'bg': 'BULGARIAN',
    'bn': 'BENGALI',
    'ca': 'CATALAN',
    'cs': 'CZECH',
    'cy': 'WELSH',
    'da': 'DANISH',
    'de': 'GERMAN',
    'el': 'GREEK',
    'en': 'ENGLISH',
    'es': 'SPANISH',
    'et': 'ESTONIAN',
    'fa': 'PERSIAN',
    'fi': 'FINNISH',
    'fr': 'FRENCH',
    'gu': 'GUJARATI',
    'he': 'HEBREW',
    'hi': 'HINDI',
    'hr': 'CROATIAN',
    'hu': 'HUNGARIAN',
    'id': 'INDONESIAN',
    'it': 'ITALIAN',
    'ja': 'JAPANESE',
    'kn': 'KANNADA',
    'ko': 'KOREAN',
    'lt': 'LITHUANIAN',
    'lv': 'LATVIAN',
    'mk': 'MACEDONIAN',
    'ml': 'MALAYALAM',
    'mr': 'MARATHI',
    'ne': 'NEPALI',
    'nl': 'DUTCH',
    'no': 'NORWEGIAN',
    'pa': 'PUNJABI',
    'pl': 'POLISH',
    'pt': 'PORTUGUESE',
    'ro': 'ROMANIAN',
    'ru': 'RUSSIAN',
    'sk': 'SLOVAK',
    'sl': 'SLOVENIAN',
    'so': 'SOMALI',
    'sq': 'ALBANIAN',
    'sv': 'SWEDISH',
    'sw': 'SWAHILI',
    'ta': 'TAMIL',
    'te': 'TELUGU',
    'th': 'THAI',
    'tl': 'FILIPINO',
    'tr': 'TURKISH',
    'uk': 'UKRAINIAN',
    'ur': 'URDU',
    'vi': 'VIETNAMESE',
    'zh-cn': 'CHINESE (SIMPLIFIED)',
    'zh-tw': 'CHINESE (TRADITIONAL)',
}
DEFAULT_CHAT_LANGUAGE = 'JAPANESE'
