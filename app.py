import streamlit as st
import pandas as pd
from rapidfuzz import fuzz

st.set_page_config(page_title="AI Excel Data Cleaning Tool", layout="wide")

st.title("🧠 AI Excel Data Cleaning Tool")

st.write("Upload messy Excel files and automatically clean the data.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("📄 Original Data")
    st.dataframe(df)

    cleaned_df = df.copy()

    # -------------------------
    # Remove Exact Duplicates
    # -------------------------
    exact_duplicates = cleaned_df.duplicated().sum()
    cleaned_df = cleaned_df.drop_duplicates()

    # -------------------------
    # Clean Text Columns
    # -------------------------
    for col in cleaned_df.select_dtypes(include="object").columns:

        cleaned_df[col] = cleaned_df[col].astype(str)

        cleaned_df[col] = cleaned_df[col].str.strip()

        if "email" in col.lower():
            cleaned_df[col] = cleaned_df[col].str.lower()

        else:
            cleaned_df[col] = cleaned_df[col].str.title()

    # -------------------------
    # Convert Date Columns
    # -------------------------
    for col in cleaned_df.columns:
        if "date" in col.lower():
            cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors="coerce")

    # -------------------------
    # Fuzzy Duplicate Detection
    # -------------------------
    fuzzy_duplicates = []

    if "Name" in cleaned_df.columns:

        names = cleaned_df["Name"].tolist()

        for i in range(len(names)):
            for j in range(i+1, len(names)):

                similarity = fuzz.ratio(names[i], names[j])

                if similarity > 85 and names[i] != names[j]:
                    fuzzy_duplicates.append((names[i], names[j]))

    # -------------------------
    # Data Quality Metrics
    # -------------------------
    missing_values = cleaned_df.isnull().sum().sum()

    total_cells = cleaned_df.shape[0] * cleaned_df.shape[1]

    quality_score = 100 - ((missing_values / total_cells) * 100)

    quality_score = round(quality_score,2)

    # -------------------------
    # Display Cleaned Data
    # -------------------------
    st.subheader("🧹 Cleaned Data")
    st.dataframe(cleaned_df)

    # -------------------------
    # Data Quality Dashboard
    # -------------------------
    st.subheader("📊 Data Quality Report")

    col1, col2, col3 = st.columns(3)

    col1.metric("Exact Duplicates Removed", exact_duplicates)
    col2.metric("Missing Values", missing_values)
    col3.metric("Data Quality Score", f"{quality_score}%")

    # -------------------------
    # Show Fuzzy Duplicates
    # -------------------------
    if fuzzy_duplicates:

        st.subheader("⚠ Possible Duplicate Names (Fuzzy Match)")

        for pair in fuzzy_duplicates:
            st.write(pair)

    # -------------------------
    # Download Cleaned File
    # -------------------------
    csv = cleaned_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Cleaned Data",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )
