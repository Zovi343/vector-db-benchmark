# LVD MODIFICATION START
from typing import List, Tuple

from engine.base_client.search import BaseSearcher
from engine.clients.chroma.parser import ChromaConditionParser

# from engine.clients.qdrant.config import QDRANT_COLLECTION_NAME

from engine.clients.chroma.config import CHROMA_COLLECTION_NAME
from engine.clients.chroma.config import CHROMA_PORT

# from engine.clients.qdrant.parser import QdrantConditionParser

from chromadb.api.models.Collection import Collection
from chromadb.config import Settings

from chromadb import HttpClient


class ChromaSearcher(BaseSearcher):
    search_params = {}
    client: HttpClient = None
    collection: Collection = None
    parser = ChromaConditionParser()

    @classmethod
    def init_client(cls, host, distance, connection_params: dict, search_params: dict):
        cls.client = HttpClient(host=host, port=CHROMA_PORT)
        cls.collection = cls.client.get_collection(CHROMA_COLLECTION_NAME)
        cls.search_params = search_params

    @classmethod
    def search_one(cls, vector, meta_conditions, top) -> List[Tuple[int, float]]:
        res = cls.collection.query(
            query_embeddings=[vector],
            where=cls.parser.parse(meta_conditions),
            n_results=top,
        )

        return list(zip(map(int, res.get("ids")[0]), res.get("distances")[0]))
# LVD MODIFICATION END
