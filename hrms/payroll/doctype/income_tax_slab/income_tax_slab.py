# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document

# import dontmanage
import dontmanageerp


class IncomeTaxSlab(Document):
	def validate(self):
		if self.company:
			self.currency = dontmanageerp.get_company_currency(self.company)
