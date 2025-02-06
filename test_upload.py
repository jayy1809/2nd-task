from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from app.config.settings import settings  # Assuming you have settings configured properly
from app.utils.cloud_upload import upload_to_cloud  # Import the function to upload to GCS

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        file_url = await upload_to_cloud(file)
        return JSONResponse(content={"url": file_url}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
