import azure.functions as func
import json
import logging
import os
import random
import uuid
from datetime import datetime, timezone

from src.blob_service.azure_blob_service import AzureBlobService
from src.eventhub_service.azure_eventhub_service import AzureEventHubService

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="uploadFile", methods=["POST"])
def upload_file(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    account_url = os.environ["STORAGE_ACCOUNT_URL"]
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


@app.route(route="sendDummyUser", methods=["POST"])
def send_dummy_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Generating dummy user data and sending to EventHub.")

    user = {
        "id": str(uuid.uuid4()),
        "name": random.choice(["Alice", "Bob", "Charlie", "Diana", "Eve"]),
        "age": random.randint(18, 65),
        "email": f"user{random.randint(1000, 9999)}@example.com",
        "country": random.choice(["US", "UK", "DE", "FR", "PL"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        eventhub_service = AzureEventHubService(
            fully_qualified_namespace=os.environ["EVENTHUB_FULLY_QUALIFIED_NAMESPACE"],
            eventhub_name=os.environ["EVENTHUB_NAME"],
        )
        eventhub_service.send_message(json.dumps(user))
        return func.HttpResponse(json.dumps(user), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error(f"Error sending to EventHub: {e}")
        return func.HttpResponse(f"Error sending to EventHub: {e}", status_code=500)
