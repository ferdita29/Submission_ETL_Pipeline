import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_data(self):
        """Test untuk memastikan data diubah dengan benar"""
        raw_data = [
            {"Title": "T-shirt", "Price": "$100", "Rating": "4.5", "Colors": "3"},
            {"Title": "Jeans", "Price": "$50", "Rating": "3.9", "Colors": "2"}
        ]
        
        transformed_data = transform_data(raw_data)
        
        self.assertEqual(len(transformed_data), 2)
        self.assertEqual(transformed_data["Price"].iloc[0], 100 * 16000)  # Check exchange rate conversion
        self.assertEqual(transformed_data["Rating"].iloc[0], 4.5)
        self.assertEqual(transformed_data["Colors"].iloc[0], 3)
        self.assertFalse(transformed_data.empty)

    def test_empty_data(self):
        """Test jika data kosong"""
        raw_data = []
        transformed_data = transform_data(raw_data)
        
        self.assertTrue(transformed_data.empty)

    def test_invalid_data(self):
        """Test jika ada data yang tidak valid"""
        raw_data = [
            {"Title": "T-shirt", "Price": "Price Unavailable", "Rating": "Invalid Rating", "Colors": "Unknown"}
        ]
        
        transformed_data = transform_data(raw_data)
        
        self.assertTrue(transformed_data.empty)

if __name__ == "__main__":
    unittest.main()
