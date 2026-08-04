import pandas as pd

df = pd.read_csv("input/adult.csv")

print("Dataset loaded successfully!\n")

print(df.head())

print("\nRows and Columns:", df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)
