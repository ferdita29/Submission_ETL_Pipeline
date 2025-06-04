import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'submission5_ferdita', 'utils')))
from utils.extract import scrape_all_pages, fetch_page_data, extract_product_data

BASE_URL = "https://fashion-studio.dicoding.dev/"

class TestExtract(unittest.TestCase):

    @patch("utils.extract.requests.get")
    def test_fetch_page_data(self, mock_get):
        html = "<html><body><div class='collection-card'></div></body></html>"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        url = f"{BASE_URL}?page=1"
        result = fetch_page_data(url)
        self.assertIsNotNone(result)
        self.assertIn("collection-card", str(result))

    def test_extract_product_data(self):
        html = '''<div class='collection-card'>
                    <h3 class='product-title'>T-shirt 1</h3>
                    <span class='price'>$123.45</span>
                    <p>Rating: \u2b50 4.4 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Men</p>
                 </div>'''
        soup = BeautifulSoup(html, "html.parser")
        product_elem = soup.find("div", class_="collection-card")
        result = extract_product_data(product_elem)

        self.assertEqual(result["Title"], "T-shirt 1")
        self.assertEqual(result["Price"], "123.45")
        self.assertIn("4.4", result["Rating"])
        self.assertEqual(result["Colors"], "3")
        self.assertEqual(result["Size"], "M")
        self.assertEqual(result["Gender"], "Men")

    @patch("utils.extract.requests.get")
    def test_scrape_all_pages(self, mock_get):
        html = '''<html><body><div class='collection-card'>
                    <h3 class='product-title'>T-shirt 1</h3>
                    <span class='price'>$123.45</span>
                    <p>Rating: \u2b50 4.4 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Men</p>
                  </div></body></html>'''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        result = scrape_all_pages(start_page=1, end_page=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "T-shirt 1")

if __name__ == "__main__":
    unittest.main()
