import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate 365 days of data
dates = pd.date_range(start="2023-01-01", periods=365, freq="D")
stores = ["Store_A", "Store_B"]

data = []
for store in stores:
    base_sales = 1000 if store == "Store_A" else 1500
    for date in dates:
        # Add weekly seasonality and some random noise
        seasonality = 200 if date.weekday() >= 5 else 0
        noise = np.random.normal(0, 50)
        sales = max(0, base_sales + seasonality + noise)
        
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Store": store,
            "Daily_Revenue": round(sales, 2)
        })

df = pd.DataFrame(data)
df.to_csv("mock_sales_data.csv", index=False)
print("mock_sales_data.csv created successfully!")
