import pandas as pd

# Load the CSV file using latin1 encoding
df = pd.read_csv("data/sales.csv", encoding="latin1")

# Display the first 5 rows
print(df.head())

# Display column names
print("\nColumns:")
print(df.columns)

# Display basic information
print("\nDataset Information:")
print(df.info())