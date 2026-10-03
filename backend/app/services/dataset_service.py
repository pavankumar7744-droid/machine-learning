import pandas as pd
import numpy as np
import io
import json

def analyze_dataset(file_bytes: bytes, filename: str) -> dict:
    if filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_bytes))
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        raise ValueError("Unsupported file format")
        
    analysis = {
        'filename': filename,
        'rows': len(df),
        'columns': len(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': int(df.duplicated().sum()),
        'date_columns': [],
        'numerical_columns': [],
        'categorical_columns': []
    }
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            analysis['numerical_columns'].append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            analysis['date_columns'].append(col)
        else:
            # simple heuristic for date strings
            if df[col].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}').any():
                analysis['date_columns'].append(col)
            else:
                analysis['categorical_columns'].append(col)
                
    # Detect target candidates (sales, revenue, etc)
    sales_keywords = ['sale', 'revenue', 'unit', 'qty', 'quantity', 'order', 'transaction', 'amount']
    target_candidates = [col for col in analysis['numerical_columns'] if any(k in col.lower() for k in sales_keywords)]
    
    # Detect group candidates
    group_keywords = ['store', 'shop', 'site', 'branch', 'location', 'region', 'category']
    group_candidates = [col for col in analysis['categorical_columns'] if any(k in col.lower() for k in group_keywords)]
    
    analysis['sales_candidates'] = target_candidates
    analysis['group_candidates'] = group_candidates
    
    analysis['forecast_ready'] = len(analysis['date_columns']) > 0 and len(target_candidates) > 0
    
    return analysis
