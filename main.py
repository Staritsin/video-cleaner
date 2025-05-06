from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import subprocess

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "🚀 Server is up and running!"}


UPLOAD_DIR = "/tmp/uploads"
OUTPUT_PATH = "/tmp/output_cut.mp4"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/clean")
async def clean_video(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    command = [
        "auto-editor",
        input_path,
        "--silent-speed", "99999",
        "--video-speed", "1",
        "--frame-rate", "30",
        "-o", OUTPUT_PATH
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Ошибка обработки видео")

    if not os.path.exists(OUTPUT_PATH):
        raise HTTPException(status_code=500, detail="Выходной файл не создан")

    return FileResponse(OUTPUT_PATH, media_type="video/mp4", filename="output_cut.mp4")
