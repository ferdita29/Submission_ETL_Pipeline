import unittest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from utils.load import save_to_csv, save_to_postgresql, save_to_google_sheets
import sys
import os

# Menambahkan direktori 'utils' ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'submission5_ferdita', 'utils')))


class TestLoad(unittest.TestCase):

    @patch("utils.load.pd.DataFrame.to_csv")
    def test_save_to_csv(self, mock_to_csv):
        """Test untuk memastikan data disimpan ke CSV"""
        df = pd.DataFrame({'Title': ['T-shirt'], 'Price': [123.45]})
        save_to_csv(df, 'test_products.csv')
        
        mock_to_csv.assert_called_once_with('test_products.csv', index=False)
        
    @patch("utils.load.psycopg2.connect")
    def test_save_to_postgresql(self, mock_connect):
        """Test untuk memastikan data disimpan ke PostgreSQL"""
        df = pd.DataFrame({'Title': ['T-shirt'], 'Price': [123.45]})
        db_config = {"host": "localhost", "database": "test_db", "user": "user", "password": "password"}
        save_to_postgresql(df, db_config, "test_table")
        
        mock_connect.assert_called_once_with(**db_config)

    @patch("utils.load.build")
    def test_save_to_google_sheets(self, mock_build):
        """Test untuk memastikan data disimpan ke Google Sheets"""
        df = pd.DataFrame({'Title': ['T-shirt'], 'Price': [123.45]})
        save_to_google_sheets(df, 'spreadsheet_id', 'Sheet1!A1')
        
        mock_build.assert_called_once()

if __name__ == "__main__":
    unittest.main()

