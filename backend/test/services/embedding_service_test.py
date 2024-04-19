import unittest
from unittest.mock import MagicMock, patch
from services.embedding_service import create_embedding
from config.constant import SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDING, ERROR_MESSAGE_DATABASE_EXCEPTION
from sqlalchemy.orm import Session
import json
from exceptions.general_exception import CustomGeneralException
from exceptions.database_exception import CustomDatabaseException

class TestCreateEmbedding(unittest.TestCase):
    """テストクラスです。embedding_service.create_embedding関数のテストを行います。"""

    @patch('fastapi.responses.JSONResponse')
    def test_no_data_in_data_store(self, mock_json_response):
        """データストアにデータがない場合のテストです。
        SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDINGを返すことを確認します。
        """
        db_session = MagicMock(Session)
        db_session.query().filter().order_by().all.return_value = []
        response = create_embedding(db_session)
        msg = json.loads(response.body.decode("utf-8")).get("message")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(msg, SUCCESS_MESSAGE_NO_NEW_DATA_FOR_EMBEDDING)

    def test_create_embedding_database_exception(self):
        """データベースで例外が発生した場合のテストです。
        500を返すことを確認します。
        """
        db_session = MagicMock(Session)
        db_session.query().filter().order_by().all.side_effect = CustomDatabaseException('Database error')
        response = create_embedding(db_session)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.body), {'error': ERROR_MESSAGE_DATABASE_EXCEPTION.format(reason='Database error')})

    def test_create_embedding_general_exception(self):
        """一般例外が発生した場合のテストです。
        500を返すことを確認します。
        """
        db_session = MagicMock(Session)
        db_session.query().filter().order_by().all.side_effect = CustomGeneralException('Custom error')
        response = create_embedding(db_session)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.body), {'error': 'Custom error'})

if __name__ == '__main__':
    unittest.main()