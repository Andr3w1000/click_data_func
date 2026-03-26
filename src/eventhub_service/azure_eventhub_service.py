from azure.eventhub import EventData, EventHubProducerClient
from azure.identity import DefaultAzureCredential


class AzureEventHubService:
    def __init__(self, fully_qualified_namespace: str, eventhub_name: str):
        self.credential = DefaultAzureCredential()
        self.producer = EventHubProducerClient(
            fully_qualified_namespace=fully_qualified_namespace,
            eventhub_name=eventhub_name,
            credential=self.credential,
        )

    def send_message(self, message: str):
        with self.producer:
            batch = self.producer.create_batch()
            batch.add(EventData(message))
            self.producer.send_batch(batch)

    def send_messages(self, messages: list[str]):
        with self.producer:
            batch = self.producer.create_batch()
            for message in messages:
                batch.add(EventData(message))
            self.producer.send_batch(batch)
