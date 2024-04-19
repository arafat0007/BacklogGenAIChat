import unittest
from unittest.mock import MagicMock
from pandas.errors import ParserError
import json
from services.data_store_service import upload_file
from config.constant import (
    ERROR_MESSAGE_NOT_EXCEL_FILE,
    SUCCESS_MESSAGE_FILE_UPLOAD,
    ERROR_MESSAGE_GENERAL,
    ERROR_MESSAGE_PANDAS_PARSER_FAIL
)

class TestDataStoreService(unittest.TestCase):
    """
    データストアサービスのテスト用のモックデータベースを作成する
    """
    def setUp(self):
        """
        テスト用のデータストアサービスのモックデータベースを作成する
        """
        self.mock_db = MagicMock()

    def test_upload_file_invalid_file_format(self):
        """
        アップロードされたファイルの形式が正しくない場合
        """
        file = MagicMock(filename="test.txt")
        response = upload_file(file, self.mock_db)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_NOT_EXCEL_FILE})

    def test_upload_file_successful_upload(self):
        """
        正常にファイルをアップロードできる場合のテスト

        テストの検証
        - アップロードに成功したことを示すレスポンスコード200が返却されること
        - アップロードに成功したことを示すメッセージがレスポンスボディに含まれていること
        """
        file = MagicMock(filename="test.xlsx")
        file.file = MagicMock()
        data_frame = MagicMock(iterrows=lambda: [(0, {"Keywords": "kw1", "Title": "Title1", "Source": "Source1", "Content": "Content1", "Category": "Cat1"})])
        with unittest.mock.patch("services.data_store_service.pd.read_excel", return_value=data_frame):
            response = upload_file(file, self.mock_db)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), {"message": SUCCESS_MESSAGE_FILE_UPLOAD})

    def test_upload_file_pandas_parser_error(self):
        """
        アップロードされたExcelファイルの形式が不正な場合

        テストの検証
        - アップロードに失敗したことを示すレスポンスコード400が返却されること
        - アップロードに失敗した理由を示すメッセージがレスポンスボディに含まれていること
        """
        file = MagicMock(filename="test.xlsx")
        file.file = MagicMock()
        with unittest.mock.patch("services.data_store_service.pd.read_excel", side_effect=ParserError("Error parsing Excel file")):
            response = upload_file(file, self.mock_db)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_PANDAS_PARSER_FAIL.format(reason="Error parsing Excel file")})

    def test_upload_file_general_error(self):
        """
        アップロードされたExcelファイルの形式が不正な場合（パーサーエラー以外のエラー）

        テストの検証
        - アップロードに失敗したことを示すレスポンスコード500が返却されること
        - アップロードに失敗した理由を示すメッセージがレスポンスボディに含まれていること
        """
        file = MagicMock(filename="test.xlsx")
        file.file = MagicMock()
        with unittest.mock.patch("services.data_store_service.pd.read_excel", side_effect=Exception("General error")):
            response = upload_file(file, self.mock_db)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.body), {"error": ERROR_MESSAGE_GENERAL.format(reason="General error")})

if __name__ == '__main__':
    unittest.main()
