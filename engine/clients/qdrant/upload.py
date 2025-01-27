import os
import time
from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.models import Batch, CollectionStatus, OptimizersConfigDiff

from engine.base_client.upload import BaseUploader
from engine.clients.qdrant.config import QDRANT_COLLECTION_NAME


class QdrantUploader(BaseUploader):
    client = None
    upload_params = {}

    @classmethod
    def init_client(cls, host, distance, connection_params, upload_params):
        os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "true"
        os.environ["GRPC_POLL_STRATEGY"] = "epoll,poll"
        # LVD MODIFICATION START
        cls.client = QdrantClient(host=host, prefer_grpc=False, **connection_params)
        # LVD MODIFICATION END
        cls.upload_params = upload_params

    @classmethod
    def upload_batch(
        cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    ):
        cls.client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=Batch.construct(
                ids=ids,
                vectors=vectors,
                payloads=[payload or {} for payload in metadata],
            ),
            wait=False,
        )

    @classmethod
    def post_upload(cls, _distance):
        cls.client.update_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            optimizer_config=OptimizersConfigDiff(
                max_optimization_threads=1,
            ),
        )

        cls.wait_collection_green()
        return {}

    @classmethod
    def wait_collection_green(cls):
        wait_time = 5.0
        total = 0
        while True:
            time.sleep(wait_time)
            total += wait_time
            collection_info = cls.client.get_collection(QDRANT_COLLECTION_NAME)
            if collection_info.status != CollectionStatus.GREEN:
                continue
            time.sleep(wait_time)
            collection_info = cls.client.get_collection(QDRANT_COLLECTION_NAME)
            if collection_info.status == CollectionStatus.GREEN:
                break
        return total

    @classmethod
    def delete_client(cls):
        if cls.client is not None:
            del cls.client
