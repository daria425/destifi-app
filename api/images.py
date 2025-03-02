from fastapi import APIRouter, Depends,UploadFile, File
from fastapi.responses import JSONResponse
from azure_blob_storage_service import AzureBlobStorageService
from db_service import UserDatabaseService
import time, re
router=APIRouter(prefix='/images')

@router.post('/upload')
async def upload_image(uid:str, image_file:UploadFile=File(...),user_db_service:UserDatabaseService=Depends()):
    container_name=uid.lower()
    azure_blob_storage_service=AzureBlobStorageService(container_name)
    azure_blob_storage_service.init_clients()
    encoded_image=image_file.file.read()
    timestamp=time.time()
    image_file_name=f"{int(timestamp)}-{image_file.filename}"
    content_type=image_file.content_type
    # image_file_name=re.sub(r'[^a-z0-9_-]', '', image_file_name)
    uploaded_image_urls=azure_blob_storage_service.upload_image_to_storage(image_file_name, encoded_image, content_type)
    if uploaded_image_urls:
        image_metadata={"image_name":image_file_name, "uploaded_at":timestamp, "storage_url":uploaded_image_urls["storage_url"], "content_type":content_type}
        update={"$push":{"stored_images": image_metadata}}
        await user_db_service.update_user(uid, update)
        return {
        "message":"Successfully uploaded image",
        "data":{"sas_url":uploaded_image_urls["sas_url"]}
        }
    return JSONResponse({
       "message": "An error occurred uploading image", 
       "data": None
    }, status_code=500)







