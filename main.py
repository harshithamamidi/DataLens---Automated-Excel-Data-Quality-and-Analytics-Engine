import os
import pandas as pd

def load_dataset(file_path):
if not os.path.exists(file_path):
raise FileNotFoundError(f"The file {file_path} does not exist.")
extension = os.path.splitext(file_path)[1].split('.')[-1].lower()
if extension == 'csv':
return pd.read_csv(file_path)
elif extension in ['xls', 'xlsx']:
return pd.read_excel(file_path)
elif extension == 'json':
return pd.read_json(file_path)  
else:
raise ValueError(f"Unsupported file format: {extension}")


file_path = "input/adult.csv"

df = load_dataset(file_path)

# Remove leading/trailing spaces from text columns
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# Convert placeholders to missing values
df.replace(["?", ""], pd.NA, inplace=True)

print("Dataset loaded successfully!\n")

print(df.head())

print("\nRows and Columns:", df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)
print(df.dtypes)

def profile_data(df):
    print("\n"+ "=" * 50)
    print("Data Profiling Summary")
    print("=" * 50)

    print(f"\nTotal Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")

    print("\nColumn names")
    print(df.columns.tolist())

    print("\nData types")
    print(df.dtypes)

profile_data(df)

print("\nMissing Values:")
missing = df.isnull().sum()
missing = missing[missing > 0]

if missing.empty:
    print("No missing values found.")
else:
    print(missing)

duplicates = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicates}")

memory_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)
print(f"\nMemory usage of the DataFrame: {memory_usage:.2f} MB")

print("\nSummary Statistics:")
print(df.describe())

print("\nCategorical Summary:")
print(df.describe(include=['object', 'category']))


