import unittest
from scraper import scrape_category_data

class TestScraper(unittest.TestCase):
    def test_scrape_category_data(self):
        # Test case 1: Valid category with articles
        category_name = "machine learning"
        results = scrape_category_data(category_name)
        self.assertTrue(len(results) > 0)

        # Test case 2: Valid category with no articles
        category_name = "nonexistent category"
        results = scrape_category_data(category_name)
        self.assertEqual(len(results), 0)

        # Test case 3: Empty category
        category_name = ""
        results = scrape_category_data(category_name)
        self.assertEqual(len(results), 0)

        # Test case 4: Category with special characters
        category_name = "!@#$%^&*()"
        results = scrape_category_data(category_name)
        self.assertEqual(len(results), 0)

        # Test case 5: Category with multiple words
        category_name = "data science"
        results = scrape_category_data(category_name)
        self.assertTrue(len(results) > 0)

if __name__ == '__main__':
    unittest.main()