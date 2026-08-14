import os
import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
import seaborn as sns


def load_dataset(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(file_path)

    elif extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)

    elif extension == ".json":
        df = pd.read_json(file_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")

    df = df.apply(
        lambda col: col.str.strip()
        if col.dtype == "object"
        else col
    )

    df.replace(
        ["?", ""],
        pd.NA,
        inplace=True
    )

    return df


def profile_data(df):

    profile = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (MB)": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2
        )
    }

    return profile


def remove_duplicates(df):

    initial_count = len(df)

    df = df.drop_duplicates()

    removed = initial_count - len(df)

    return df, removed


def drop_sparse_columns(df, threshold=0.4):

    missing_ratio = df.isnull().mean()

    columns_to_drop = missing_ratio[
        missing_ratio > threshold
    ].index.tolist()

    df = df.drop(
        columns=columns_to_drop
    )

    return df, columns_to_drop


def drop_sparse_rows(df, threshold=0.4):

    missing_ratio = df.isnull().mean(axis=1)

    rows_to_drop = missing_ratio[
        missing_ratio > threshold
    ].index.tolist()

    df = df.drop(
        index=rows_to_drop
    )

    return df, len(rows_to_drop)


def fill_missing_values(df):

    for column in df.columns:

        if is_numeric_dtype(df[column]):

            median = df[column].median()

            if pd.notnull(median):
                df[column] = df[column].fillna(median)
            else:
                df[column] = df[column].fillna(0)

        else:

            mode_value = df[column].mode()

            if not mode_value.empty:
                df[column] = df[column].fillna(mode_value[0])

            else:
                df[column] = df[column].fillna("Unknown")

    return df
