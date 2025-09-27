from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

# Create your tests here.
class MovieBookingTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge()  # or webdriver.Edge() / Firefox()
        self.driver.maximize_window()
        self.driver.get("https://online-movie-ticket-booking-website-production.up.railway.app/")  # Change to your site address
    """
    def test_login_valid(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Đăng nhập").click()
        driver.find_element(By.NAME, "username").send_keys("kientrung")
        driver.find_element(By.NAME, "password").send_keys("Kien8013")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Đăng xuất", driver.page_source)  # Expect login success

    def test_login_invalid(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Đăng nhập").click()
        driver.find_element(By.NAME, "username").send_keys("kientrung")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Sai tên đăng nhập hoặc mật khẩu", driver.page_source)
    

    def test_search_movie(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Phim").click()
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Avengers")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        self.assertIn("Avengers", driver.page_source)
    """
    def test_booking_seat(self):
        driver = self.driver

        driver.find_element(By.LINK_TEXT, "Đăng nhập").click()
        driver.find_element(By.NAME, "username").send_keys("kientrung")
        driver.find_element(By.NAME, "password").send_keys("Kien8013")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        driver.find_element(By.LINK_TEXT, "Mua vé").click()
        driver.find_element(By.LINK_TEXT, "Chọn ghế & Đặt vé").click()
        # Find all available green seats
        available_seats = driver.find_elements(By.CSS_SELECTOR, "input.seat-checkbox:not([disabled])")

        # Pick the first available seat
        if available_seats:
            available_seats[0].click()
        else:
            self.fail("No available seats to book")
        
        driver.find_element(By.NAME, "Email").send_keys("hiepkien2k4@gmail.com")
        driver.find_element(By.NAME, "Số điện thoại").send_keys("1234567890")
        driver.find_element(By.LINK_TEXT, "Xác nhận ghế").click()
        time.sleep(2)

        # Verify booking success
        self.assertIn("Đặt vé thành công", driver.page_source)



    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
