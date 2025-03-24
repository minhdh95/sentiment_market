from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from vnstock import Vnstock
import time

class VnIndexScraper:
    def get_vnindex(self, start_date, end_date):
        stock = Vnstock().stock(symbol='VNINDEX', source='VCI')
        df = stock.quote.history(start=start_date, end=end_date)
        return df


class ScrapeFireant:
    def __init__(self, url="https://fireant.vn/cong-dong/pho-bien", headless=True):
        """Khởi tạo ScrapeFireant với URL và tùy chọn headless"""
        self.url = url
        self.headless = headless
        self.driver = None

    def setup_driver(self):
        """Thiết lập WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")  # Chạy ở chế độ không giao diện
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Khởi tạo WebDriver (không cần chỉ định đường dẫn nếu chromedriver đã trong PATH)
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self):
        """Thực hiện scrape và trả về danh sách các text"""
        try:
            # Thiết lập driver
            self.setup_driver()

            # Truy cập trang web
            self.driver.get(self.url)

            # Chờ trang tải ban đầu
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "overflow-x-hidden"))
            )

            # Cuộn trang để tải thêm nội dung (nếu có infinite scroll)
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Chờ nội dung tải thêm
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:  # Nếu không còn nội dung mới
                    break
                last_height = new_height

            # Nhấp vào tất cả các nút "Thêm" (nếu có)
            while True:
                try:
                    more_buttons = self.driver.find_elements(By.XPATH, "//a[text()='Thêm']")
                    if not more_buttons:
                        break
                    for button in more_buttons:
                        self.driver.execute_script("arguments[0].click();", button)  # Nhấp bằng JavaScript
                        time.sleep(1)  # Chờ nội dung mở rộng
                except:
                    break

            # Lấy toàn bộ nguồn trang sau khi tải hết nội dung động
            page_source = self.driver.page_source

            # Phân tích HTML bằng BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            target_divs = soup.find_all('div', class_='overflow-x-hidden leading-7')

            # Danh sách để lưu trữ các text
            results = []

            # Lặp qua từng div và lấy nội dung
            for div in target_divs:
                # Lấy toàn bộ text, loại bỏ khoảng trắng thừa
                full_text = div.get_text(separator=" ", strip=True)
                results.append(full_text)

            return results

        finally:
            # Đóng trình duyệt nếu driver đã được khởi tạo
            if self.driver:
                self.driver.quit()
