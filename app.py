import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import cv2

from ocr_pipeline import extract_text, export_to_excel
from jamabandi_mapper_component import jamabandi_mapper_component

# 📍 Region Detector
def detect_region(text):
    text = text.lower()
    if "फतेहाबाद" in text or "भटिंडा" in text:
        return "Punjab"
    elif "करनाल" in text or "यमुनानगर" in text:
        return "Haryana"
    return "Default"

st.set_page_config(page_title="Jamabandi OCR Genie", layout="wide")
st.title("Jamabandi OCR Genie 🧞‍♂️")

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
if use_demo:
    image = Image.open("demo_images/demo_jamabandi.png").convert("RGB")
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
    region_hint = detect_region(raw_text)
    st.info(f"📍 Detected Region: {region_hint}")

    mapped_df = jamabandi_mapper_component(df_raw, region_hint=region_hint) if mode == "Schema Mapping" else df_raw

    if st.button("Export to Excel"):
        excel_file = export_to_excel(mapped_df.columns.tolist(), mapped_df.values.tolist())
        st.download_button(
            label="Download Excel",
            data=excel_file,
            file_name="jamabandi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
