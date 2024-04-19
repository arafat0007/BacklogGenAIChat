import unittest
from unittest.mock import MagicMock
from config.constant import ERROR_MESSAGE_EMPTY_QUERY, ERROR_MESSAGE_EMPTY_EMAIL, ERROR_MESSAGE_EMPTY_CHATID
from services.user_query_service import get_query_answer
from models.message import Message
from sqlalchemy.orm import Session
import json

class TestGetQueryAnswer(unittest.TestCase):

    def setUp(self):
        """テスト実行前の設定を行います。

        MagicMockを使用してdb_sessionをモック化します。
        """
        self.db_session = MagicMock(Session)

    def test_query_is_none(self):
        """ユーザーがクエリを入力しなかった場合、Empty query error というエラーメッセージが返されることを確認します。

        Args:
            self (TestGetQueryAnswer): 本クラスのインスタンス

        Returns:
            None: 何も返さない
        """
        db = self.db_session
        gen = get_query_answer(None, 'test@example.com', None, db)
        response = next(gen)
        json_result = json.loads(response.body)
        self.assertEqual(json_result['status'], 'answer')
        self.assertEqual(json_result['error'], ERROR_MESSAGE_EMPTY_QUERY)

    def test_email_is_none(self):
        """ユーザーがメールアドレスを入力しなかった場合、
        Empty email error というエラーメッセージが返されることを確認します。

        Args:
            self (TestGetQueryAnswer): 本クラスのインスタンス

        Returns:
            None: 何も返さない
        """
        db = self.db_session
        gen = get_query_answer(123, None, 'test query', db)
        response = next(gen)
        json_result = json.loads(response.body)
        self.assertEqual(json_result['status'], 'answer')
        self.assertEqual(json_result['error'], ERROR_MESSAGE_EMPTY_EMAIL)


    def test_chat_id_is_none(self):
        """ユーザーがチャットIDを入力しなかった場合、
        Empty chat id error というエラーメッセージが返されることを確認します。

        Args:
            self (TestGetQueryAnswer): 本クラスのインスタンス

        Returns:
            None: 何も返さない
        """
        db = self.db_session
        gen = get_query_answer(None, 'test@example.com', 'test query', db)
        response = next(gen)
        json_result = json.loads(response.body)
        self.assertEqual(json_result['status'], 'answer')
        self.assertEqual(json_result['error'], ERROR_MESSAGE_EMPTY_CHATID)

if __name__ == '__main__':
    unittest.main()
