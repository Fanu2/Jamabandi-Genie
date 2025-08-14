import streamlit as st
from PIL import Image
import numpy as np
import cv2

from ocr_pipeline import extract_text, export_to_excel
from schema_mapping import normalize_headers

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

    if st.button("Export to Excel"):
        excel_file = export_to_excel(headers, rows)
        st.download_button(
            label="Download Excel",
            data=excel_file,
            file_name="jamabandi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
