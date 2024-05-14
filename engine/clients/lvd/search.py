# LVD MODIFICATION START
from typing import List, Tuple
import requests
from engine.base_client.search import BaseSearcher
from engine.clients.lvd.parser import LVDConditionParser

from engine.clients.lvd.config import LVD_COLLECTION_NAME
from engine.clients.lvd.config import LVD_PORT


from chromadb.api.models.Collection import Collection
from chromadb.config import Settings
from chromadb import HttpClient


class LVDSearcher(BaseSearcher):
    search_params = {}
    client: HttpClient = None
    collection: Collection = None
    parser = LVDConditionParser()
    upload_host = None
    upload_port = None

    @classmethod
    def init_client(cls, host, distance, connection_params: dict, search_params: dict):
        cls.client = HttpClient(host=host, port=LVD_PORT)
        cls.collection = cls.client.get_collection(LVD_COLLECTION_NAME)
        cls.search_params = search_params
        cls.upload_host = host
        cls.upload_port = LVD_PORT


    @classmethod
    def search_one(cls, vector, meta_conditions, top) -> List[Tuple[int, float]]:
        data =  {
            "query_embeddings": [vector],
            "include": ["distances"],
            "where": cls.parser.parse(meta_conditions),
            "n_results": top,
            "n_buckets": cls.search_params["n_buckets"],
            "bruteforce_threshold": None,
            "constraint_weight": cls.search_params["constraint_weight"],
        }

        url = f"http://{cls.upload_host}:{cls.upload_port}/api/v1/collections/{cls.collection.id}/query"
        res = requests.post(url, json=data, headers={}, verify=False)
        res = res.json()

        return list(zip(map(int, res.get("ids")[0]), res.get("distances")[0]))
# LVD MODIFICATION END
