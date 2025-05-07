from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import subprocess

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

        # Сохраняем загруженный файл
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print("✅ Файл получен:", input_path)

        # Удаляем выходной файл, если был
        if os.path.exists(OUTPUT_PATH):
            os.remove(OUTPUT_PATH)

        # Запускаем auto-editor
        result = subprocess.run(
            ["auto-editor", input_path, "--output_file", OUTPUT_PATH],
            capture_output=True,
            text=True
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            raise Exception("Auto-editor failed")

        # Проверка наличия файла
        if not os.path.exists(OUTPUT_PATH):
            raise Exception("Файл не создан")

        print("✅ Обработка завершена")
        return FileResponse(OUTPUT_PATH, media_type="video/mp4", filename="cleaned.mp4")

    except Exception as e:
        print("❌ Ошибка:", str(e))
        return JSONResponse(status_code=500, content={"detail": f"Ошибка: {str(e)}"})
