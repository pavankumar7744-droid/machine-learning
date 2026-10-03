import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

def run_stage2():
    print("Running Stage 2: EDA and Cleaning...")
    data_path = 'data/raw/online_shoppers_intention.csv'
    df = pd.read_csv(data_path)
    
    # Audit
    audit_results = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': int(df.isnull().sum().sum()),
        'duplicates': int(df.duplicated().sum())
    }
    
    with open('results/metrics/data_audit.json', 'w') as f:
        json.dump(audit_results, f, indent=4)
        
    print(f"Data Audit: {audit_results}")
    
    # Cleaning
    df_clean = df.drop_duplicates().copy()
    if 'Revenue' in df_clean.columns:
        df_clean['Revenue'] = df_clean['Revenue'].astype(int)
        
    df_clean.to_csv('data/processed/online_shoppers_cleaned.csv', index=False)
    
    # EDA Plots
    sns.set_theme(style="whitegrid")
    
    # 1. Target Distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Revenue', data=df_clean)
    plt.title('Purchase Distribution')
    plt.savefig('results/plots/purchase_distribution.png')
    plt.close()
    
    # 2. PageValues by Revenue
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Revenue', y='PageValues', data=df_clean)
    plt.title('PageValues vs Revenue')
    plt.yscale('symlog')
    plt.savefig('results/plots/pagevalues_vs_revenue.png')
    plt.close()
    
    # 3. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    # Select only numeric columns for correlation
    numeric_df = df_clean.select_dtypes(include=['float64', 'int64', 'int32'])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=False, cmap='coolwarm')
    plt.title('Numeric Correlation Heatmap')
    plt.savefig('results/plots/correlation_heatmap.png')
    plt.close()
    
    print("Stage 2 completed. Output in results/metrics/ and results/plots/")

if __name__ == "__main__":
    run_stage2()
