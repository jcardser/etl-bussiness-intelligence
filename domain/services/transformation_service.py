import pandas as pd

class TransformationService:
    def __init__(self):
        pass

    def clean_reviews(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['comments'] = df['comments'].fillna('').str.strip()
        df['reviewer_name'] = df['reviewer_name'].fillna('Unknown')
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        print("🧹 Datos transformados correctamente.")
        return df
