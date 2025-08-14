import streamlit as st
from PIL import Image
import numpy as np
import cv2
from utils.ocr_pipeline import extract_text, export_to_excel
from schema_mapping import normalize_headers

st.title("Jamabandi OCR Genie 🧞‍♂️")
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
        st.write("Normalized Headers:", headers)

        if st.button("Export to Excel"):
            excel_file = export_to_excel(headers, rows)
            st.download_button("Download Excel", data=excel_file, file_name="jamabandi.xlsx")
