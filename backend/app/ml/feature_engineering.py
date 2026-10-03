import pandas as pd
import numpy as np

def engineer_purchase_features(df: pd.DataFrame) -> pd.DataFrame:
    df_eng = df.copy()
    
    # Ensure types
    for col in ['Month', 'VisitorType', 'OperatingSystems', 'Browser', 'Region', 'TrafficType', 'Weekend']:
        if col in df_eng.columns:
            df_eng[col] = df_eng[col].astype(str)
            
    if 'Administrative' in df_eng.columns:
        df_eng['total_pages'] = df_eng['Administrative'] + df_eng['Informational'] + df_eng['ProductRelated']
        df_eng['total_duration'] = df_eng['Administrative_Duration'] + df_eng['Informational_Duration'] + df_eng['ProductRelated_Duration']
        
        df_eng['avg_time_per_page'] = np.where(df_eng['total_pages'] > 0, df_eng['total_duration'] / df_eng['total_pages'], 0)
        df_eng['product_page_share'] = np.where(df_eng['total_pages'] > 0, df_eng['ProductRelated'] / df_eng['total_pages'], 0)
        df_eng['product_time_share'] = np.where(df_eng['total_duration'] > 0, df_eng['ProductRelated_Duration'] / df_eng['total_duration'], 0)
        
        df_eng['is_returning'] = (df_eng['VisitorType'] == 'Returning_Visitor').astype(int)
        df_eng['is_new'] = (df_eng['VisitorType'] == 'New_Visitor').astype(int)
        
        df_eng['is_peak_season'] = df_eng['Month'].isin(['Nov', 'Dec']).astype(int)
        
    if 'PageValues' in df_eng.columns:
        df_eng['has_pagevalue'] = (df_eng['PageValues'] > 0).astype(int)
        
    return df_eng
