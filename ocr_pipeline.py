import easyocr
import openpyxl
from openpyxl.styles import Font
from io import BytesIO

reader = easyocr.Reader(['hi'], gpu=False)

def extract_text(img_cv):
    results = reader.readtext(img_cv, detail=0)
    return "\n".join(results)

def export_to_excel(headers, rows):
    wb = openpyxl.Workbook()
    ws = wb.active

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
