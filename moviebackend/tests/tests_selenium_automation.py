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
    
    def test_booking_seat(self):
        driver = self.driver

        # Login first
        driver.find_element(By.LINK_TEXT, "Đăng nhập").click()
        driver.find_element(By.NAME, "username").send_keys("kientrung")
        driver.find_element(By.NAME, "password").send_keys("Kien8013")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # Go to booking
        driver.find_element(By.LINK_TEXT, "Mua vé").click()
        driver.find_element(By.LINK_TEXT, "Chọn ghế & Đặt vé").click()
        time.sleep(4)

        seat_number = "42"
        seat = driver.find_element(By.CSS_SELECTOR, f"div.seat[data-seat-number='{seat_number}']")
        seat.click()
        time.sleep(2)

        # Confirm booking
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # Verify booking success
        self.assertIn("Đặt vé thành công", driver.page_source)

    def test_booking_history(self):
        driver = self.driver

        # Login first
        driver.find_element(By.LINK_TEXT, "Đăng nhập").click()
        driver.find_element(By.NAME, "username").send_keys("kientrung")
        driver.find_element(By.NAME, "password").send_keys("Kien8013")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Thành viên").click()

        driver.find_element(By.LINK_TEXT, "LỊCH SỬ GIAO DỊCH").click()
        time.sleep(2)
        self.assertIn("Booking", driver.page_source)


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()