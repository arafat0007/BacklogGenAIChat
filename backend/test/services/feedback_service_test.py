import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from services.feedback_service import create_feedback
import json
from config.constant import ERROR_MESSAGE_EMPTY_CHATID, ERROR_MESSAGE_EMPTY_RATING, ERROR_MESSAGE_GENERAL

class TestCreateFeedback(unittest.TestCase):

    def test_valid_input(self):
        """
        有効なフィードバックの作成と、200ステータスコードの返却をテストします。
        """
        db = MagicMock(Session)  # データベースセッションをMockします。
        response = create_feedback(1, "Great chat!", 8, db)  # フィードバックを作成します。
        self.assertEqual(response.status_code, 200)  # ステータスコードが200であることをアサートします。
    
    def test_invalid_chat_id(self):
        """
        無効なチャットID（None）のフィードバックの作成テスト

        テストの検証
        - アップロードに失敗したことを示すレスポンスコード400が返却されること
        - アップロードに失敗した理由を示すメッセージがレスポンスボディに含まれていること
        """
        db = MagicMock(Session)  # データベースセッションをMockします。
        response = create_feedback(None, "Great chat!", 8, db) # フィードバックを作成します。
        self.assertEqual(response.status_code, 400) # ステータスコードが400であることをアサートします。
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_EMPTY_CHATID})
    
    def test_invalid_rating(self):
        """
        無効な評価値（11）のフィードバックの作成テスト

        テストの検証
        - アップロードに失敗したことを示すレスポンスコード400が返却されること
        - アップロードに失敗した理由を示すメッセージがレスポンスボディに含まれていること
        """
        db = MagicMock(Session)  # データベースセッションをMockします。
        response = create_feedback(1, "Great chat!", 11, db) # フィードバックを作成します。
        self.assertEqual(response.status_code, 400) # ステータスコードが400であることをアサートします。
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_EMPTY_RATING})

    def test_database_exception(self):
        """
        データベースに接続できない場合、例外が発生することをテストします。
        テストの検証
        - アップロードに失敗したことを示すレスポンスコード500が返却されること
        - アップロードに失敗した理由を示すメッセージがレスポンスボディに含まれていること
        """
        db = MagicMock(Session)  # データベースセッションをMockします。
        db.commit.side_effect = Exception("Database connection failed")
        response = create_feedback(1, "Great chat!", 8, db) # フィードバックを作成します。
        self.assertEqual(response.status_code, 500) # ステータスコードが500であることをアサートします。
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_GENERAL.format(reason="Database connection failed")})

if __name__ == '__main__':
    unittest.main()