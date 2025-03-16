from fastapi import APIRouter, Depends, UploadFile, File 
from fastapi.responses import JSONResponse
from app.services.azure_blob_storage_service import AzureBlobStorageService
from app.db.db_service import UserDatabaseService
from app.core.agents.travel_agent import Travel_Agent
from app.core.assistants.travel_image_assistant import TravelImageAnalyzer
from app.schemas.user_message import UserMessage
from app.core.create_itinerary import create_itinerary_from_image
import time
router=APIRouter(prefix="/chat")

@router.post("")
def run_chat(user_message:UserMessage, travel_agent:Travel_Agent=Depends()):
    response=travel_agent.respond_to_user(user_message.message)
    return {
        "message": "Message run completed successfully", 
        "data":{
            "message":response
        }
    }

@router.post('/itinerary/create')
async def create_itinerary(uid:str, image_file:UploadFile=File(...),user_db_service:UserDatabaseService=Depends(), travel_image_analyzer:TravelImageAnalyzer=Depends(), travel_agent:Travel_Agent=Depends()):
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
        itinerary_data=create_itinerary_from_image(travel_image_analyzer=travel_image_analyzer, travel_agent=travel_agent, image_data_url=uploaded_image_urls["sas_url"])
        update={"$push":{"threads":{
            "thread_id":itinerary_data["thread_id"],
            "created_at":itinerary_data["timestamp"], 
            "image":image_metadata
        }}}
        await user_db_service.update_user(uid, update)
        return {
        "message":"Successfully created itinerary",
        "data":{
            "message":itinerary_data["message"],
            "thread_id":itinerary_data["thread_id"],
        }
        }
    return JSONResponse({
       "message": "An error occurred creating itinerary", 
       "data": None
    }, status_code=500)

