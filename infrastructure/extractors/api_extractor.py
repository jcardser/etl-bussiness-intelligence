# infrastructure/extractors/api_extractor.py
from domain.interfaces.extractor_interface import IExtractor

class APIExtractor(IExtractor):
    def __init__(self, api_client):
        self.api_client = api_client

    def extract(self, url):
        return self.api_client.read_api(url)
