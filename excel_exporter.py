from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows

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
