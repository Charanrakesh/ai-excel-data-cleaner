
import streamlit as st
import pandas as pd

st.title("🧠 AI Excel Data Cleaning Tool")

st.write("Upload a messy Excel file and automatically clean it.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Original Data")
    st.dataframe(df)

    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Standardize text columns
    for col in cleaned_df.select_dtypes(include="object").columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        cleaned_df[col] = cleaned_df[col].str.title()

    st.subheader("Cleaned Data")
    st.dataframe(cleaned_df)

    # Download cleaned file
    csv = cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Cleaned Data",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
