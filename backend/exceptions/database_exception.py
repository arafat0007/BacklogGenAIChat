class CustomDatabaseException(Exception):
    """
    カスタムデータベース例外クラスです。

    Attributes:
        message (str): 例外メッセージです。
    """
    def __init__(self, message="Database exception occurred."):
        self.message = message
        super().__init__(self.message)