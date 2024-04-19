import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from services.message_service import get_messages
import json
from models.message import Message
from config.constant import ERROR_MESSAGE_EMPTY_CHATID, ERROR_MESSAGE_EMPTY_EMAIL

class TestGetMessages(unittest.TestCase):
    """get_messages関数のテストクラスです。

    get_messages関数が正しく動作するかをテストします。
    """

    def setUp(self):
        """テスト実行前の設定を行います。

        MagicMockを使用してdb_sessionをモック化します。
        """
        self.db_session = MagicMock(Session)

    def test_get_messages_valid_input(self):
        """入力が正しい場合のget_messages関数のテストです。

        chat_id, email, db_sessionを引数にget_messages関数を呼び出し、
        レスポンスのステータスコード、メッセージの内容が正しいか確認します。
        """
        chat_id = 1
        email = "test@example.com"
        chat = MagicMock()
        chat.User = email
        self.db_session.query().filter().first.return_value = chat
        message = Message(Id=1, ChatId=chat_id, Type="user", Content="Test message")
        self.db_session.query().filter().all.return_value = [message]
        response = get_messages(chat_id, email, self.db_session)
        response_message = json.loads(response.body)['messages'][0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message['Id'], 1)
        self.assertEqual(response_message['ChatId'], 1)
        self.assertEqual(response_message['Type'], "user")
        self.assertEqual(response_message['Content'], "Test message")

    def test_get_messages_empty_chat_id(self):
        """chat_idが空の場合のget_messages関数のテストです。

        chat_id, email, db_sessionを引数にget_messages関数を呼び出し、
        レスポンスのステータスコード、エラーメッセージが正しいか確認します。
        """
        response = get_messages(None, "test@example.com", self.db_session)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_EMPTY_CHATID})

    def test_get_messages_empty_email(self):
        """emailが空の場合のget_messages関数のテストです。

        chat_id, email, db_sessionを引数にget_messages関数を呼び出し、
        レスポンスのステータスコード、エラーメッセージが正しいか確認します。
        """
        response = get_messages(1, None, self.db_session)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_EMPTY_EMAIL})
        
    def test_get_messages_exception_handling(self):
        """例外発生時のget_messages関数のテストです。

        db_session.query.side_effectを使用して例外を発生させ、
        レスポンスのステータスコードが500であることを確認します。
        """
        self.db_session.query.side_effect = Exception("Test Exception")
        response = get_messages(1, "test@example.com", self.db_session)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
