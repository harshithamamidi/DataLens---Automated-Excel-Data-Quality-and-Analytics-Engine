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

def generate_quality_report(df):

    report = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().mean().values * 100
        ).round(2),
        "Unique Values": df.nunique().values
    })

    return report

def convert_data_types(df):

    for column in df.columns:

        if df[column].dtype == "object":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )


            valid_values = converted.notna().sum()


            if valid_values > 0:

                original_values = df[column].notna().sum()


                if valid_values / original_values > 0.8:

                    df[column] = converted


    return df


def missing_value_chart(df):

    missing = df.isnull().sum()

    missing = missing[
        missing > 0
    ]

    if missing.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x=missing.index,
        y=missing.values,
        ax=ax
    )

    ax.set_title(
        "Missing Values by Column"
    )

    ax.set_xlabel(
        "Columns"
    )

    ax.set_ylabel(
        "Missing Count"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    return fig


def numeric_distribution_chart(df):

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns


    charts = []


    for column in numeric_columns[:3]:

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.histplot(
            data=df,
            x=column,
            kde=True,
            ax=ax
        )

        ax.set_title(
            f"Distribution of {column}"
        )

        plt.tight_layout()

        charts.append(fig)


    return charts


def categorical_distribution_chart(df):

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns


    charts = []


    for column in categorical_columns[:3]:

        values = (
            df[column]
            .value_counts()
            .head(10)
        )


        fig, ax = plt.subplots(
            figsize=(8, 5)
        )


        sns.barplot(
            x=values.values,
            y=values.index,
            ax=ax
        )


        ax.set_title(
            f"Top Categories in {column}"
        )


        ax.set_xlabel(
            "Count"
        )

        ax.set_ylabel(
            column
        )

        plt.tight_layout()


        charts.append(fig)


    return charts


def export_cleaned_data(df, filename):

    output_dir = "output"

    os.makedirs(
        output_dir,
        exist_ok=True
    )


    name = os.path.splitext(
        filename
    )[0]


    output_path = os.path.join(
        output_dir,
        f"{name}_cleaned.xlsx"
    )


    df.to_excel(
        output_path,
        index=False
    )


    return output_path

