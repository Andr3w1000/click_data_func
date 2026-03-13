import azure.functions as func
import logging
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from blob_service.azure_blob_service import AzureBlobService

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="uploadFile", methods=["POST"])
def upload_file(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    account_url = "https://bandipyfuncstorage.blob.core.windows.net"
    container_name = "landing"

    file = req.files.get('file')
    if file is None:
        return func.HttpResponse("No file provided.", status_code=400)

    try:
        blob_service = AzureBlobService(account_url)
        blob_service.upload_blob(container_name, file.filename, file.stream)
        return func.HttpResponse(f"File {file.filename} uploaded successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return func.HttpResponse(f"Error uploading file: {e}", status_code=500)
