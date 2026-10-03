import pandas as pd
from pathlib import Path

def main():
    data_path = Path("data/raw/online_shoppers_intention.csv")
    output_path = Path("results/metrics/data_audit.md")
    
    if not data_path.exists():
        print(f"Error: {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    
    rows, cols = df.shape
    missing_vals = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    
    # Target
    target_col = "Revenue"
    target_exists = target_col in df.columns
    if target_exists:
        purchase_rate = df[target_col].mean() * 100
    
    # Months
    month_col = "Month"
    if month_col in df.columns:
        months_present = set(df[month_col].unique())
    else:
        months_present = set()
    
    expected_months = {"Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}
    missing_expected = expected_months - months_present
    unexpected_months = months_present - expected_months

    with open(output_path, "w") as f:
        f.write("# Data Audit Report\n\n")
        f.write("## 1. Dataset Shape and Basic Checks\n")
        f.write(f"- **Rows:** {rows} (Expected: 12,330) - {'Pass' if rows == 12330 else 'Fail'}\n")
        f.write(f"- **Columns:** {cols} (Expected: 18) - {'Pass' if cols == 18 else 'Fail'}\n")
        f.write(f"- **Missing Values:** {missing_vals} (Expected: 0) - {'Pass' if missing_vals == 0 else 'Fail'}\n")
        f.write(f"- **Exact Duplicate Rows:** {duplicates} (Expected: 125) - {'Pass' if duplicates == 125 else 'Fail'}\n\n")
        
        f.write("## 2. Target Variable (`Revenue`)\n")
        f.write(f"- **Target column present:** {'Yes' if target_exists else 'No'}\n")
        if target_exists:
            f.write(f"- **Type:** {df[target_col].dtype}\n")
            f.write(f"- **Purchase Rate (overall):** {purchase_rate:.2f}% (Expected: ~15.5%)\n")
            # Calculate purchase rate after removing duplicates
            df_no_dups = df.drop_duplicates()
            purchase_rate_no_dups = df_no_dups[target_col].mean() * 100
            f.write(f"- **Purchase Rate (without duplicates):** {purchase_rate_no_dups:.2f}% (Expected: ~15.6%)\n\n")
            
        f.write("## 3. Categorical Values Check (`Month`)\n")
        f.write(f"- **Months Present:** {', '.join(sorted(months_present))}\n")
        if not missing_expected and not unexpected_months:
             f.write("- **Status:** Pass. Matches expected months exactly (Jan and Apr absent).\n")
        else:
             f.write(f"- **Missing from expected:** {missing_expected}\n")
             f.write(f"- **Unexpected months found:** {unexpected_months}\n")

if __name__ == "__main__":
    main()
