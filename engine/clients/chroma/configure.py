# LVD MODIFICATION START
from benchmark.dataset import Dataset
from engine.base_client.configure import BaseConfigurator
from engine.clients.chroma.config import CHROMA_COLLECTION_NAME
from engine.clients.chroma.config import CHROMA_PORT

from engine.base_client.distances import Distance

from chromadb.config import Settings
from chromadb import HttpClient


class ChromaConfigurator(BaseConfigurator):
    DISTANCE_MAPPING = {
        Distance.L2: "l2",
        Distance.COSINE: "cosine",
        Distance.DOT: "ip",
    }

    def __init__(self, host, collection_params: dict, connection_params: dict):
        super().__init__(host, collection_params, connection_params)

        self.client = HttpClient(host=host, port=CHROMA_PORT)

    def clean(self):
        if CHROMA_COLLECTION_NAME in self.client.list_collections():
            self.client.delete_collection(CHROMA_COLLECTION_NAME)

    def recreate(self, dataset: Dataset, collection_params):
        print("distance: ", self.DISTANCE_MAPPING.get(dataset.config.distance))
        self.client.create_collection(
            CHROMA_COLLECTION_NAME,
            metadata={
                "hnsw:space": self.DISTANCE_MAPPING.get(dataset.config.distance),
                **collection_params, # unpack the collection_params dict
            },
            get_or_create=True, # If True, return the existing collection if it exists.
        )
# LVD MODIFICATION END
