import pytesseract
import openpyxl
from openpyxl.styles import Font
from io import BytesIO

def extract_text(img_cv):
    return pytesseract.image_to_string(img_cv, lang="hin")

def export_to_excel(headers, rows):
    wb = openpyxl.Workbook()
    ws = wb.active

    # Apply Mangal font
    mangal_font = Font(name="Mangal", size=12)

    ws.append(headers)
    for row in rows:
        ws.append(row)

    for row in ws.iter_rows():
        for cell in row:
            cell.font = mangal_font

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output
