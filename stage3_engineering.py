import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
import json

def engineer_features(df):
    df_eng = df.copy()
    
    df_eng['total_pages'] = df_eng['Administrative'] + df_eng['Informational'] + df_eng['ProductRelated']
    df_eng['total_duration'] = df_eng['Administrative_Duration'] + df_eng['Informational_Duration'] + df_eng['ProductRelated_Duration']
    
    df_eng['avg_time_per_page'] = np.where(df_eng['total_pages'] > 0, df_eng['total_duration'] / df_eng['total_pages'], 0)
    df_eng['product_page_share'] = np.where(df_eng['total_pages'] > 0, df_eng['ProductRelated'] / df_eng['total_pages'], 0)
    df_eng['product_time_share'] = np.where(df_eng['total_duration'] > 0, df_eng['ProductRelated_Duration'] / df_eng['total_duration'], 0)
    
    df_eng['is_returning'] = (df_eng['VisitorType'] == 'Returning_Visitor').astype(int)
    df_eng['is_new'] = (df_eng['VisitorType'] == 'New_Visitor').astype(int)
    
    df_eng['is_peak_season'] = df_eng['Month'].isin(['Nov', 'Dec']).astype(int)
    df_eng['has_pagevalue'] = (df_eng['PageValues'] > 0).astype(int)
    
    return df_eng

def leakage_audit(df, target_col='Revenue', threshold=0.80):
    leakage_report = {}
    
    y = df[target_col]
    X_raw = df.drop(columns=[target_col])
    
    # Simple numerical encoding for the audit
    X = pd.get_dummies(X_raw, drop_first=True)
    
    for col in X.columns:
        model = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), LogisticRegression(max_iter=1000))
        scores = cross_val_score(model, X[[col]], y, cv=5, scoring='roc_auc', n_jobs=-1)
        mean_auc = scores.mean()
        
        leakage_report[col] = {
            'roc_auc': float(mean_auc),
            'is_leaky': bool(mean_auc > threshold)
        }
    
    return leakage_report

def run_stage3():
    print("Running Stage 3: Feature Engineering and Leakage Audit...")
    df = pd.read_csv('data/processed/online_shoppers_cleaned.csv')
    
    df_eng = engineer_features(df)
    df_eng.to_csv('data/processed/online_shoppers_engineered.csv', index=False)
    
    report = leakage_audit(df_eng)
    
    with open('results/metrics/leakage_audit.json', 'w') as f:
        json.dump(report, f, indent=4)
        
    print("Stage 3 completed. Engineered data saved. Leakage audit in results/metrics/")

if __name__ == '__main__':
    run_stage3()
