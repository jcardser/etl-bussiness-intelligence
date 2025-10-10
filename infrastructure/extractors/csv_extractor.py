# infrastructure/extractors/csv_extractor.py
from domain.interfaces.services.extractor_interface import IExtractor
import pandas as pd

class CSVExtractor(IExtractor):
    def __init__(self, csv_client):
        self.csv_client = csv_client

    def extract(self, path, sep=",") -> pd.DataFrame:
        return self.csv_client.read_csv(path, sep)
