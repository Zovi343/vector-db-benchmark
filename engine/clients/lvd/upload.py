# LVD MODIFICATION START
from typing import List, Optional
from engine.base_client.upload import BaseUploader
import requests

from engine.clients.lvd.config import LVD_COLLECTION_NAME
from engine.clients.lvd.config import LVD_PORT

from chromadb.api.models.Collection import Collection
from chromadb.config import Settings
from chromadb import HttpClient


class LVDUploader(BaseUploader):
    client: HttpClient = None
    upload_params = {}
    collection: Collection = None
    upload_host = None
    upload_port = None

    @classmethod
    def init_client(cls, host, distance, connection_params, upload_params):
        # cls.client = QdrantClient(host=host, prefer_grpc=True, **connection_params)
        cls.client = HttpClient(host=host, port=LVD_PORT)
        cls.collection = cls.client.get_collection(LVD_COLLECTION_NAME)
        cls.upload_params = upload_params
        cls.upload_host = host
        cls.upload_port = LVD_PORT


    @classmethod
    def upload_batch(
        cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    ):
        id_strings = [str(elem) for elem in ids]
        if metadata is not None and len(metadata) > 0:
            if not bool(metadata[0]):  # check if metadata dict empty
                metadata = None

        cls.collection.add(
            embeddings=vectors,
            metadatas=metadata,
            ids=id_strings,
        )

    @classmethod
    def post_upload(cls, _distance):
        url = f"http://{cls.upload_host}:{cls.upload_port}/api/v1/collections/{cls.collection.id}/build_index"
        requests.post(url, json={}, headers={}, verify=False)
        return {}


    @classmethod
    def delete_client(cls):
        if cls.client is not None:
            del cls.client
# LVD MODIFICATION START
