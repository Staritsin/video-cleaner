from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "/tmp/uploads"
OUTPUT_PATH = "/tmp/output_cut.mp4"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "🚀 Server is up and running"}

@app.post("/clean")
async def clean_video(file: UploadFile = File(...)):
    try:
        input_path = os.path.join(UPLOAD_DIR, file.filename)

        # Сохраняем файл
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print("✅ Файл сохранён:", input_path)

        # Заглушка: просто копируем как будто обработали
        shutil.copy(input_path, OUTPUT_PATH)

        print("✅ Обработка завершена. Возврат файла:", OUTPUT_PATH)
        return FileResponse(OUTPUT_PATH, media_type="video/mp4", filename="result.mp4")

    except Exception as e:
        print("❌ Ошибка обработки:", str(e))
        return JSONResponse(status_code=500, content={"detail": f"Ошибка обработки: {str(e)}"})
