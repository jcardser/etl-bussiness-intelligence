from abc import ABC, abstractmethod
import pandas as pd

class IExtractor(ABC):
    """Interfaz base para todos los extractores."""

    @abstractmethod
    def extract(self, *args, **kwargs) -> pd.DataFrame:
        """Extrae datos desde una fuente y los devuelve como DataFrame."""
        pass
