from fastapi import FastAPI, File, UploadFile
import shutil
import os
from fastapi.responses import HTMLResponse

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload</title>
    </head>
    <body>
        <h2>Upload File</h2>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
        <h2><a href="/files/">Upload More Files</a></h2>
    </body>
    </html>
    """
@app.post("/upload/")
async def upload_file(file: UploadFile =
            File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "message": "correct"}
@app.get("/files/", response_class=HTMLResponse)
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    files_list = "".join(f"<li>{file}</li>" for file in files)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uploaded Files</title>
    </head>
    <body>
        <h2>Uploaded Files</h2>
        <ul>
            {files_list}
        </ul>
        <h2><a href="/">Upload More Files</a></h2>
    </body>
    </html>
    """
    