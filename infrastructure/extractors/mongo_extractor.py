# infrastructure/extractors/mongo_extractor.py
from domain.interfaces.services.extractor_interface import IExtractor

class MongoExtractor(IExtractor):
    def __init__(self, repository):
        self.repository = repository

    def extract(self, collection_name, query=None, projection=None, limit=0):
        return self.repository.read_collection(collection_name, query, projection, limit)
