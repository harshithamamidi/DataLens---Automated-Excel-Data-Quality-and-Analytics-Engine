import streamlit as st
import pandas as pd
import os

from main import (
    remove_duplicates,
    drop_sparse_columns,
    drop_sparse_rows,
    fill_missing_values,
    profile_data,
    generate_quality_report,
    convert_data_types,
    missing_value_chart,
    numeric_distribution_chart,
    categorical_distribution_chart,
    export_cleaned_data
)


st.set_page_config(
    page_title="DataLens",
    layout="wide"
)


st.title("DataLens")

st.subheader(
    "Automated Data Quality and Analytics Engine"
)


st.write(
    "Upload a CSV, Excel, or JSON file to analyze, clean, and visualize your dataset."
)


uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=[
        "csv",
        "xlsx",
        "xls",
        "json"
    ]
)


if uploaded_file is not None:


    file_extension = uploaded_file.name.split(".")[-1].lower()


    if file_extension == "csv":

        df = pd.read_csv(
            uploaded_file
        )


    elif file_extension in ["xlsx", "xls"]:

        df = pd.read_excel(
            uploaded_file
        )


    elif file_extension == "json":

        df = pd.read_json(
            uploaded_file
        )


    df = df.apply(
        lambda col:
        col.str.strip()
        if col.dtype == "object"
        else col
    )


    df.replace(
        ["?", ""],
        pd.NA,
        inplace=True
    )


    df = convert_data_types(df)


    st.success(
        "Dataset uploaded successfully"
    )


    st.header(
        "Dataset Preview"
    )


    st.dataframe(
        df.head()
    )


    st.header(
        "Data Quality Report"
    )


    quality_report = generate_quality_report(
        df
    )


    st.dataframe(
        quality_report,
        use_container_width=True
    )


    profile = profile_data(
        df
    )


    st.header(
        "Dataset Overview"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Rows",
            profile["Rows"]
        )


    with col2:

        st.metric(
            "Columns",
            profile["Columns"]
        )


    with col3:

        st.metric(
            "Missing Values",
            profile["Missing Values"]
        )


    with col4:

        st.metric(
            "Duplicate Rows",
            profile["Duplicate Rows"]
        )


    st.header(
        "Missing Value Analysis"
    )


    missing_chart = missing_value_chart(
        df
    )


    if missing_chart:

        st.pyplot(
            missing_chart
        )

    else:

        st.info(
            "No missing values detected."
        )


    if st.button(
        "Run Data Cleaning"
    ):


        before_rows = df.shape[0]

        before_columns = df.shape[1]

        before_missing = df.isnull().sum().sum()

        before_duplicates = df.duplicated().sum()



        df, removed_duplicates = remove_duplicates(
            df
        )


        df, removed_columns = drop_sparse_columns(
            df
        )


        df, removed_rows = drop_sparse_rows(
            df
        )


        df = fill_missing_values(
            df
        )


        after_rows = df.shape[0]

        after_columns = df.shape[1]

        after_missing = df.isnull().sum().sum()

        after_duplicates = df.duplicated().sum()



        st.success(
            "Data cleaning completed successfully"
        )


        st.header(
            "Cleaning Summary"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Duplicates Removed",
                removed_duplicates
            )


        with col2:

            st.metric(
                "Columns Dropped",
                len(removed_columns)
            )


        with col3:

            st.metric(
                "Rows Dropped",
                removed_rows
            )



        st.header(
            "Before vs After Cleaning"
        )


        comparison = pd.DataFrame(
            {
                "Before Cleaning":
                [
                    before_rows,
                    before_columns,
                    before_missing,
                    before_duplicates
                ],

                "After Cleaning":
                [
                    after_rows,
                    after_columns,
                    after_missing,
                    after_duplicates
                ]
            },

            index=[
                "Rows",
                "Columns",
                "Missing Values",
                "Duplicate Rows"
            ]
        )


        st.dataframe(
            comparison,
            use_container_width=True
        )



        st.header(
            "Cleaned Dataset Quality Report"
        )


        cleaned_report = generate_quality_report(
            df
        )


        st.dataframe(
            cleaned_report,
            use_container_width=True
        )



        st.header(
            "Cleaned Dataset Preview"
        )


        st.dataframe(
            df.head()
        )



        st.header(
            "Data Visualizations"
        )


        numeric_charts = numeric_distribution_chart(
            df
        )


        for chart in numeric_charts:

            st.pyplot(
                chart
            )



        categorical_charts = categorical_distribution_chart(
            df
        )


        for chart in categorical_charts:

            st.pyplot(
                chart
            )



        output_path = export_cleaned_data(
            df,
            uploaded_file.name
        )


        st.success(
            "Cleaned file generated"
        )


        with open(
            output_path,
            "rb"
        ) as file:


            st.download_button(
                label="Download Cleaned Dataset",
                data=file,
                file_name=os.path.basename(output_path),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )