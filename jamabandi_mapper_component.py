import streamlit as st
import pandas as pd
import json
import os
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from rapidfuzz import process

# 🗂 Predefined Jamabandi schemas
JAMABANDI_SCHEMAS = {
    "Haryana Standard": {
        "विवरण सहित मालिक नाम": "Owner Name",
        "विवरण सहित कारकातार": "Cultivator",
        "रकबा और किस्म जमीन": "Area and Land Type",
        "खेवट संख्या": "Khewat No.",
        "खाता संख्या": "Khata No.",
        "फसल का नाम": "Crop Name",
        "जमाबंदी वर्ष": "Jamabandi Year"
    },
    "Punjab Variant": {
        "मालिक का नाम": "Owner Name",
        "किसान का नाम": "Cultivator",
        "कुल रकबा": "Total Area",
        "खसरा नंबर": "Khasra No.",
        "फसल विवरण": "Crop Details",
        "वर्ष": "Year"
    },
    "Custom Mapping": {}
}

# 📥 Load saved custom mapping
def load_custom_mapping():
    if os.path.exists("custom_mapping.json"):
        with open("custom_mapping.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 💾 Save custom mapping
def save_custom_mapping(mapping):
    with open("custom_mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

# 🔁 Rename headers using schema
def remap_headers(df, schema):
    return df.rename(columns=lambda col: schema.get(col.strip(), col))

# 🧵 Fuzzy match headers to schema keys
def fuzzy_remap(df, schema):
    mapped = {}
    for col in df.columns:
        match, score = process.extractOne(col, schema.keys())
        mapped[col] = schema.get(match, col) if score > 80 else col
    return df.rename(columns=mapped)

# 📤 Export to Excel with Mangal font
def export_with_mangal_font(df, filename="jamabandi_cleaned.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Jamabandi Data"

    mangal_font = Font(name="Mangal", size=12)

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            cell.font = mangal_font

    wb.save(filename)

# 🧞‍♂️ Main schema mapping component
def jamabandi_mapper_component(df_raw):
    st.sidebar.header("🗂 Jamabandi Schema Selection")
    schema_choice = st.sidebar.selectbox("Choose Schema", list(JAMABANDI_SCHEMAS.keys()))

    if schema_choice == "Custom Mapping":
        st.subheader("🔧 Define Custom Header Mapping")
        custom_map = load_custom_mapping()
        updated_map = {}

        for col in df_raw.columns:
            default = custom_map.get(col, col)
            new_label = st.text_input(f"Rename '{col}' to:", value=default)
            updated_map[col] = new_label

        if st.button("💾 Save Custom Mapping"):
            save_custom_mapping(updated_map)
            st.success("✅ Custom mapping saved")

        mapped_df = remap_headers(df_raw, updated_map)

    else:
        selected_schema = JAMABANDI_SCHEMAS[schema_choice]
        mapped_df = fuzzy_remap(df_raw, selected_schema)

    st.subheader("✅ Mapped Table Preview")
    st.dataframe(mapped_df)

    if st.button("📤 Export to Excel"):
        export_with_mangal_font(mapped_df)
        st.success("Exported with Mangal font as jamabandi_cleaned.xlsx")

    return mapped_df
