import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from services.chat_service import create_chat
from config.constant import ERROR_MESSAGE_EMPTY_EMAIL, ERROR_MESSAGE_CHAT_CREATE, ERROR_MESSAGE_CHAT_NOT_FOUND
import json
from models.chat import Chat
from services.chat_service import get_chat

class TestCreateChat(unittest.TestCase):
    """create_chat関数のテストクラス

    チャットセッションを作成するcreate_chat関数のテストを行う
    """

    def setUp(self):
        """テスト実行前の処理

        mockでデータベースセッションをモックする
        """
        self.db_session = MagicMock(spec=Session)

    def test_create_chat_success(self):
        """成功した場合のテスト

        チャットセッションが正しく作成されることを確認する
        """
        db = MagicMock()
        email = "test@example.com"
        chat_id = 1
        chat = Chat(Id=chat_id, User=email)
        db.add.return_value = None
        db.commit.return_value = None
        response = create_chat(email, db)
        self.assertEqual(response.status_code, 200)

    def test_create_chat_empty_email(self):
        """メールアドレスが空の場合のテスト

        メールアドレスが空の場合、400を返すことを確認する
        """
        email = None
        response = create_chat(email, self.db_session)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_EMPTY_EMAIL})

    def test_create_chat_exception(self):
        """例外が発生した場合のテスト

        例外が発生した場合、500を返すことを確認する
        """
        email = "test@example.com"
        self.db_session.begin.side_effect = Exception("Database error")
        response = create_chat(email, self.db_session)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_CHAT_CREATE.format(reason="Database error")})

    def test_get_chat_success(self):
        """チャット取得成功時のテスト

        指定されたチャットIDのチャットが正しく取得できることを確認する
        """
        chat_id = 1
        chat = Chat(Id=chat_id, User="test@example.com")
        # 指定されたチャットIDのチャットを取得する
        self.db_session.query().filter().first.return_value = chat
        returned_chat = get_chat(chat_id, self.db_session)
        # 取得したチャットが正しいチャットであることを確認する
        self.assertEqual(returned_chat, chat)
        self.assertEqual(returned_chat, chat)

    def test_get_chat_failure(self):
        """
        チャット取得失敗時のテスト

        存在しないチャットIDを指定してチャットを取得した場合、例外が発生することを確認する

        """
        chat_id = 1
        # 指定されたチャットIDのチャットが存在しない場合、例外が発生することを想定する
        self.db_session.query().filter().first.return_value = None
        with self.assertRaises(Exception) as context:
            get_chat(chat_id, self.db_session)
        # 発生した例外が、存在しないチャットのエラーメッセージを含んでいることを確認する
        self.assertIn(ERROR_MESSAGE_CHAT_NOT_FOUND.format(id=chat_id), str(context.exception))

if __name__ == '__main__':
    unittest.main()
