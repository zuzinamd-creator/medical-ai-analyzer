import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    api_key = os.getenv("AI_KEY")
    base_url = os.getenv("AI_URL")
    
    # Теперь этот список — часть объекта settings
    COMPETITORS_URLS = [
        "https://www.dealmed.ru/search/?q=%D1%81%D1%82%D0%B5%D1%82%D0%BE%D1%81%D0%BA%D0%BE%D0%BF%D1%8B",
        "https://www.sunmed.ru/search/?s=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&q=%D1%81%D1%82%D0%B5%D1%82%D0%BE%D1%81%D0%BA%D0%BE%D0%BF%D1%8B",
        "https://mteh1.ru/catalog/?q=%D1%81%D1%82%D0%B5%D1%82%D0%BE%D1%81%D0%BA%D0%BE%D0%BF%D1%8B&s=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8"
    ]

settings = Settings()