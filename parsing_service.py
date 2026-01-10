import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ParsingService:
    def __init__(self):
        self.screenshots_dir = "screenshots"
        # Создаем папку для скриншотов, если её нет
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def capture_screenshot(self, url: str) -> str:
        """Автоматически открывает сайт и делает скриншот"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск без окна браузера
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Настройка драйвера
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(url)
            # Ждем немного, чтобы элементы и изображения успели прогрузиться
            time.sleep(5) 
            
            # Генерируем уникальное имя файла
            filename = f"screenshot_{int(time.time())}.jpg"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # Делаем скриншот
            driver.save_screenshot(filepath)
            return filepath
        finally:
            driver.quit()

parsing_service = ParsingService()