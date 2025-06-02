# Copyright (c) 2025, ptpratul2@gmail.com and contributors
# For license information, please see license.txt

import frappe
import pandas as pd
from frappe.model.document import Document
from frappe.utils.file_manager import get_file_path

class ItemBulkUpdate(Document):
	def on_submit(self):
		
		if not self.excel_file:
			frappe.msgprint("No file uploaded")
			return

		try:
			file_path = get_file_path(self.excel_file)
			df = pd.read_excel(file_path)
			frappe.msgprint(f"Loaded {len(df)} rows from file")

			log = []

			for i, row in df.iterrows():
				item_code = str(row.get("item_code")).strip()
				is_stock_item = int(row.get("is_stock_item"))

				try:
					frappe.db.set_value("Item", item_code, "is_stock_item", is_stock_item)
					frappe.db.commit()
					log.append(f" Force-updated {item_code}")
				except Exception as e:
					log.append(f" Error updating {item_code}: {e}")


			self.status_log = "\n".join(log)
			frappe.db.commit()

		except Exception as e:
			frappe.msgprint(f" Error processing file: {e}")
