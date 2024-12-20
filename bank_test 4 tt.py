# מוחמד טאטור
# 314933854
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class TestSpatialCommunityAI(unittest.TestCase):
    def setUp(self):
        # Initialize the browser
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000")  # The URL of the webpage

    def test_page_title(self):
        """Test: Check if the page title is correct"""
        title = self.driver.title
        self.assertEqual(title, "The Spatial Community", "Page title is incorrect")
        print("AI Test 1: Page title is correct")

    def test_main_heading(self):
        """Test: Check if the main heading is displayed correctly"""
        main_heading = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(main_heading, "The Spatial Community", "Main heading is not displayed correctly")
        print("AI Test 2: Main heading is displayed correctly")

    def test_sub_heading(self):
        """Test: Check if the subheading is displayed correctly"""
        sub_heading = self.driver.find_element(By.TAG_NAME, "h2").text
        self.assertIn("Welcome to The Spatial Community", sub_heading, "Subheading is incorrect")
        print("AI Test 3: Subheading is displayed correctly")

    def test_navigation_links(self):
        """Test: Verify if all navigation links are displayed"""
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav ul li a")
        self.assertEqual(len(nav_links), 3, "The number of navigation links is incorrect")
        expected_links = ["ABOUT", "EVENTS", "JOIN"]
        for i, link in enumerate(nav_links):
            self.assertEqual(link.text, expected_links[i], f"Link '{link.text}' does not match the expected text")
        print("AI Test 4: All navigation links are displayed correctly")

    def test_event_list(self):
        """Test: Verify if the list of events is displayed"""
        events = self.driver.find_elements(By.TAG_NAME, "li")
        self.assertGreaterEqual(len(events), 2, "Not all events are displayed")
        print("AI Test 5: The list of events is displayed correctly")

    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
