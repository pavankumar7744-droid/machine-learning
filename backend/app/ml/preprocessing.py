import pandas as pd
import numpy as np

def load_data(filepath: str) -> pd.DataFrame:
    """Loads dataset from filepath."""
    return pd.read_csv(filepath)

def clean_data(df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
    """Cleans the dataset."""
    df_clean = df.copy()
    
    # Target encoding
    if 'Revenue' in df_clean.columns:
        df_clean['Revenue'] = df_clean['Revenue'].astype(int)
        
    # Drop duplicates
    if drop_duplicates:
        df_clean = df_clean.drop_duplicates().reset_index(drop_drop=True)
        
    return df_clean

def perform_data_audit(df: pd.DataFrame) -> dict:
    """Performs basic data audit and returns a dictionary of stats."""
    stats = {
        'rows': len(df),
        'cols': len(df.columns),
        'missing_values': int(df.isnull().sum().sum()),
        'duplicates': int(df.duplicated().sum()),
        'columns': list(df.columns)
    }
    
    if 'Revenue' in df.columns:
        stats['purchase_rate'] = float(df['Revenue'].mean())
        
    if 'Month' in df.columns:
        stats['months_present'] = list(df['Month'].unique())
        
    return stats
