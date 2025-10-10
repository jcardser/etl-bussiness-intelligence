import pandas as pd

class DataFrameValidator:
    def is_valid(self, df: pd.DataFrame):
        """Valida que el DataFrame no esté vacío y tenga columnas."""
        if df is None:
            return False
        if df.empty:
            print("⚠️  El DataFrame está vacío.")
            return False
        return True
