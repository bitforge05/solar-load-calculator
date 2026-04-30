import openpyxl
from openpyxl.utils import get_column_letter
import os

class ExcelHandler:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def fill_template(self, data: dict, output_path: str):
        """
        Fills the Excel template with extracted data.
        Maps JSON keys to specific cells.
        """
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template not found at {self.template_path}")

        # Load workbook (data_only=False to preserve formulas)
        wb = openpyxl.load_workbook(self.template_path)
        sheet = wb.active

        # Mapping of data keys to Excel cells
        # This is a sample mapping. In a real scenario, this would match the user's template.
        mapping = {
            "consumer_name": "B2",
            "consumer_number": "B3",
            "billing_month": "B4",
            "meter_number": "B5",
            "tariff_type": "B6",
            "units_consumed": "B8",
            "bill_amount": "B9",
            "sanctioned_load": "B10",
            "connected_load": "B11",
            "contract_demand": "B12"
        }

        for key, cell in mapping.items():
            if key in data and data[key] is not None:
                sheet[cell] = data[key]

        # Save to the new path
        wb.save(output_path)
        return output_path
