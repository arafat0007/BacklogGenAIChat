class CustomGeneralException(Exception):
    """
    オプションのメッセージでクラスを初期化します。

    パラメータ：
        message (str): 例外が発生した場合に表示されるメッセージ。

    戻り値：
        None
    """
    def __init__(self, message="Exception occurred."):
        self.message = message
        super().__init__(self.message)
