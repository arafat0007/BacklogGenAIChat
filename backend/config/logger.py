import logging
from logging.handlers import TimedRotatingFileHandler
from config.constant import LOGGER_NAME, LOGGER_FORMAT, LOGGER_PATH, LOGGER_FILE, LOGGER_ROTATING_SUFFIX, LOGGER_ENCODING, LOGGER_ROTATE_TIMING, LOGGER_3_MONTHS

def init_logger() -> logging.Logger:
    """
    StreamHandlerとTimedRotatingFileHandlerを設定したロガーを生成する。

    ロガーには、標準出力にログを出力するStreamHandlerと、
    ファイルにログを保存するTimedRotatingFileHandlerが設定される。

    生成されたロガーはINFOレベルでロギングを行う。

    Returns:
        logging.Logger: StreamHandlerとTimedRotatingFileHandlerを設定したロガー
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOGGER_FORMAT)

    # 標準出力にログを出力するStreamHandlerを設定
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    # ファイルにログを保存するTimedRotatingFileHandlerを設定
    rotating_file_handler = TimedRotatingFileHandler(
        filename=LOGGER_PATH + LOGGER_FILE,
        when=LOGGER_ROTATE_TIMING,
        backupCount=LOGGER_3_MONTHS,
        encoding=LOGGER_ENCODING)

    # ローテーションされたファイル名の拡張子を設定
    rotating_file_handler.suffix = LOGGER_ROTATING_SUFFIX

    # ローテーションされたファイルのログフォーマットを設定
    rotating_file_handler.setFormatter(formatter)

    # ローテーションされたファイルのログレベルを設定
    rotating_file_handler.setLevel(logging.INFO)

    # ロガーにハンドラを追加
    logger.addHandler(rotating_file_handler)

    return logger

def get_logger() -> logging.Logger:
    """
    ロガーを取得する。

    Returns:
        logging.Logger: ロガー
    """
    return logging.getLogger(LOGGER_NAME)
