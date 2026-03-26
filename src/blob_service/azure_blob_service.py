from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class AzureBlobService:
    def __init__(self, account_url: str):
        # Use DefaultAzureCredential to authenticate with system-assigned managed identity
        self.credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(
            account_url=account_url, credential=self.credential)

    def get_container_client(self, container_name: str) -> ContainerClient:
        return self.blob_service_client.get_container_client(container_name)

    def get_blob_client(self, container_name: str, blob_name: str) -> BlobClient:
        return self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    def upload_blob(self, container_name: str, blob_name: str, data: bytes):
        blob_client = self.get_blob_client(container_name, blob_name)
        blob_client.upload_blob(data)

    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        blob_client = self.get_blob_client(container_name, blob_name)
        download_stream = blob_client.download_blob()
        return download_stream.readall()

    def delete_blob(self, container_name: str, blob_name: str):
        blob_client = self.get_blob_client(container_name, blob_name)
        blob_client.delete_blob()
