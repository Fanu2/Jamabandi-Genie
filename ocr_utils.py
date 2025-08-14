import cv2
import pytesseract
import pandas as pd

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

def extract_table(image):
    data = pytesseract.image_to_data(image, lang='hin', output_type=pytesseract.Output.DATAFRAME)
    data = data.dropna(subset=['text'])
    rows = data.groupby('block_num')['text'].apply(list).tolist()
    return pd.DataFrame(rows)
