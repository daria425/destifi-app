from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
from app.utils.logger import logger
from urllib.parse import urlparse
import requests
load_dotenv()
AZURE_BLOB_STORAGE_CONNECTION_STRING=os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STRING")
AZURE_BLOB_STORAGE_ACCOUNT_KEY=os.getenv("AZURE_BLOB_STORAGE_ACCOUNT_KEY")
class AzureBlobStorageService:
    azure_request_headers={"x-ms-blob-type": "BlockBlob"}
    def __init__(self, container_name):
        self.container_name=container_name
        self.blob_service_client=None
        self.container_client=None

    def init_clients(self):
        """Initializes the Azure Blob Storage client and creates the container if it doesn't exist."""
        if not self.blob_service_client:
            self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_STORAGE_CONNECTION_STRING)
        
        container_client = self.blob_service_client.get_container_client(self.container_name)
        try:
            self.container_client = container_client.create_container()
            logger.info(f"Container '{self.container_name}' created successfully.")
        except Exception as e:
            self.container_client = container_client
            logger.info(f"Container '{self.container_name}' already exists.")

    @staticmethod
    def parse_storage_url(storage_url:str)->str:
        parsed_url=urlparse(storage_url)
        path_parts = parsed_url.path.lstrip("/").split("/")
        blob_name = "/".join(path_parts[1:])  # Remaining part is the blob name
        return blob_name
    
    def generate_sas_token(self, blob_name:str)->str:
        """Generates a SAS token for the blob with the specified name."""
        if not self.blob_service_client or not self.container_client:
            self.init_clients()
        sas_token=generate_blob_sas(
        account_name=self.blob_service_client.account_name,
        container_name=self.container_name,
        blob_name=blob_name,
        account_key=AZURE_BLOB_STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(write=True, read=True),
        expiry=datetime.now(timezone.utc)+ timedelta(hours=2)
        )
        return sas_token
    def generate_sas_url(self, blob_name:str):
        """Generates a SAS URL for the blob with the specified name."""
        sas_token=self.generate_sas_token(blob_name)
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
    
        
    def upload_image_to_storage(self, image_file_name:str, image_bytes:bytes, content_type:str)->dict[str]|None:
        try:
            sas_url=self.generate_sas_url(blob_name=image_file_name)
            print(f"Generated SAS URL:{sas_url}")
            response=requests.put(sas_url, data=image_bytes, headers={** self.azure_request_headers, "Content-Type":content_type})
            response.raise_for_status()
            logger.info(f"Successfully uploaded {image_file_name} to Azure Blob Storage")
            storage_url= f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{image_file_name}"
            return {
                "sas_url":sas_url, "storage_url": storage_url
            }
        except Exception as e:
            logger.error(f"Error uploading image to Azure Blob Storage: {e}")
            return None
            
# container_name="TlrBqorGTDOS4iXOkkMuu3Xfne42".lower()
# storage=AzureBlobStorageService(container_name)
# storage_url="https://destifiblobstorage.blob.core.windows.net/tlrbqorgtdos4ixokkmuu3xfne42/1741473159-sample_image_2.jpg"
# blob_name=storage.parse_storage_url(storage_url)
# sas_url=storage.generate_sas_url(blob_name)
# print(sas_url)