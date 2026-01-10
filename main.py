from fastapi import FastAPI, HTTPException
from services import openai_service
from parsing_service import parsing_service
from config import settings # Добавили импорт для доступа к URL конкурентов
import os
import json
import time

app = FastAPI(title="Medical Competitor AI Analyzer")

# --- ШАГ 4: Настройка папки истории ---
HISTORY_DIR = "history"
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

@app.get("/")
def read_root():
    return {
        "status": "online", 
        "message": "Медицинский ИИ-анализатор готов к работе",
        "capabilities": [
            "Manual Site Analysis", 
            "Batch Competitor Analysis (Config-based)", 
            "Text/Image Local Analysis"
        ]
    }

@app.post("/analyze-text")
def analyze_text(text: str):
    try:
        return openai_service.analyze_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-site")
def analyze_site(url: str):
    """
    РУЧНОЙ РЕЖИМ: Selenium делает скриншот любого введенного URL, 
    ИИ проводит аудит, результат сохраняется в историю.
    """
    try:
        screenshot_path = parsing_service.capture_screenshot(url)
        analysis = openai_service.analyze_image(screenshot_path)
        
        timestamp = int(time.time())
        history_file = os.path.join(HISTORY_DIR, f"analysis_{timestamp}.json")
        
        report_data = {
            "timestamp": timestamp,
            "url": url,
            "screenshot_path": screenshot_path,
            "analysis_result": analysis.model_dump()
        }
        
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=4)
        
        return {
            "status": "success",
            "history_saved_to": history_file,
            "url": url,
            "analysis_result": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при анализе сайта: {str(e)}")

@app.post("/analyze-all-competitors")
def analyze_all_competitors():
    """
    АВТОМАТИЧЕСКИЙ РЕЖИМ (Шаг 4): Анализирует список сайтов из config.py.
    """
    # Извлекаем список URL из config.py
    urls = getattr(settings, "COMPETITORS_URLS", [])
    
    if not urls:
        raise HTTPException(
            status_code=404, 
            detail="Список COMPETITORS_URLS в config.py пуст или не найден."
        )

    batch_results = []
    for url in urls:
        try:
            # Используем существующий метод для каждого сайта
            report = analyze_site(url)
            batch_results.append({
                "url": url, 
                "status": "success", 
                "file": report["history_saved_to"]
            })
        except Exception as e:
            batch_results.append({
                "url": url, 
                "status": "error", 
                "detail": str(e)
            })
            
    return {
        "message": f"Завершен массовый аудит. Обработано сайтов: {len(urls)}",
        "results": batch_results
    }

@app.post("/analyze-image")
def analyze_image(file_name: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "data", "images", file_name)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"Файл {file_name} не найден.")
    
    try:
        return openai_service.analyze_image(image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)