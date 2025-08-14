import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import cv2

from ocr_pipeline import extract_text, export_to_excel
from jamabandi_mapper_component import jamabandi_mapper_component
from schema_mapping import normalize_headers

st.set_page_config(page_title="Jamabandi OCR Genie", layout="wide")
st.title("Jamabandi OCR Genie 🧞‍♂️")

# 🧭 Sidebar Onboarding
with st.sidebar:
    st.header("🧭 Onboarding Tips")
    st.markdown("""
    - Upload high-resolution Jamabandi scans (JPG/PNG)
    - Hindi documents only (Devanagari/Mangal font)
    - Common headers like `खाता संख्या`, `खसरा नंबर` will be auto-normalized
    - Click 'Export to Excel' to download styled output
    """)

    mode = st.radio("Choose Mode", ["Quick Export", "Schema Mapping"])
    use_demo = st.checkbox("Use Demo Image")

# 📤 File Upload or Demo Load
uploaded_file = None
if use_demo:
    uploaded_file = "demo_images/demo_jamabandi.png"  # Replace with actual path or load from repo
else:
    uploaded_file = st.file_uploader("Upload Jamabandi scan", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Running OCR..."):
        raw_text = extract_text(img_cv)
        headers, rows = normalize_headers(raw_text)

    st.success("OCR Complete!")
    st.text_area("Extracted Text", raw_text, height=300)
    st.write("🔤 Normalized Headers:", headers)
    st.write("📄 Extracted Rows:", rows)

    df_raw = pd.DataFrame(rows, columns=headers)

    # 🧩 Optional Schema Mapping
    if mode == "Schema Mapping":
        jamabandi_mapper_component(df_raw)

    # 📥 Excel Export
    if st.button("Export to Excel"):
        excel_file = export_to_excel(headers, rows)
        st.download_button(
            label="Download Excel",
            data=excel_file,
            file_name="jamabandi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
