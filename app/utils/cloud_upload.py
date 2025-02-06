from fastapi import HTTPException
from google.cloud import storage
from fastapi import UploadFile
import uuid
from app.config.settings import settings



async def upload_to_cloud(file: UploadFile) -> str:
    try:
        file_size = 0
        chunks = []
        # chunk_size = 8192 #ye 8kb he
        chunk_size = 524288 #and ye 512kb

        MAX_FILE_SIZE_MB = settings.MAX_FILE_SIZE_MB
        MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
        while chunk := await file.read(chunk_size):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE_MB}MB"
                )
            chunks.append(chunk)

        file_content = b''.join(chunks)
        
        client = storage.Client.from_service_account_json(settings.GCD_CREDENTIALS_JSON_PATH)
        bucket = client.bucket(settings.GCS_BUCKET_NAME)
        extension = file.filename.split('.')[-1].lower()
        blob_name = f"products/{uuid.uuid4()}.{extension}"
        blob = bucket.blob(blob_name)
        
        blob.upload_from_string(
            file_content,
            content_type=file.content_type
        )
        
        return blob.public_url
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

