from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
from logger import logger
import requests
load_dotenv()
AZURE_BLOB_STORAGE_CONNECTION_STRING=os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STRING")
AZURE_BLOB_STORAGE_ACCOUNT_KEY=os.getenv("AZURE_BLOB_STORAGE_ACCOUNT_KEY")
class AzureBlobStorageService:
    azure_request_headers={"x-ms-blob-type": "BlockBlob"}
    def __init__(self, container_name):
        self.container_name=container_name
        self.blob_service_client=None

    def init_blob_service_client(self):
        if not self.blob_service_client:
            self.blob_service_client=BlobServiceClient.from_connection_string(AZURE_BLOB_STORAGE_CONNECTION_STRING)

    def generate_sas_url(self, blob_name:str):
        self.init_blob_service_client()
        sas_token=generate_blob_sas(
        account_name=self.blob_service_client.account_name,
        container_name=self.container_name,
        blob_name=blob_name,
        account_key=AZURE_BLOB_STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(write=True),
        expiry=datetime.now(timezone.utc)+ timedelta(hours=1)
        )
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
    
    def upload_image(self, image_file_name:str, image_bytes:bytes):
        try:
            sas_url=self.generate_sas_url(blob_name=image_file_name)
            response=requests.put(sas_url, data=image_bytes, headers=self.azure_request_headers)
            response.raise_for_status()
            logger.info("Successfully uploaded {image_file_name} to Azure Blob Storage")
        except Exception as e:
            logger.error(f"Error uploading image to Azure Blob Storage: {e}")
            


