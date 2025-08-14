import streamlit as st
import pandas as pd
import cv2
from PIL import Image
from jamabandi_mapper_component import jamabandi_mapper_component
from ocr_utils import preprocess_image, extract_table

st.set_page_config(page_title="Jamabandi OCR Mapper", layout="wide")
st.title("📄 Jamabandi OCR-to-CSV Tool")

st.markdown("""
Welcome! Upload a Hindi Jamabandi land record image (Mangal font preferred).  
We'll extract the table, let you map headers, and export clean CSV/Excel for civic/legal use.
""")

uploaded_file = st.file_uploader("Upload Jamabandi Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Running OCR..."):
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        preprocessed = preprocess_image(img_cv)
        df_raw = extract_table(preprocessed)

    st.subheader("🧾 Raw OCR Table")
    st.dataframe(df_raw)

    df_mapped = jamabandi_mapper_component(df_raw)

    st.markdown("✅ Done! You can now download the cleaned file.")
