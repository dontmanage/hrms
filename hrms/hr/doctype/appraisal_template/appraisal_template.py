# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import flt


class AppraisalTemplate(Document):
	def validate(self):
		self.validate_total_weightage("goals")
		self.validate_total_weightage("rating_criteria")

	def validate_total_weightage(self, table_name):
		if not self.get(table_name):
			return

		total_weightage = sum(flt(d.per_weightage) for d in self.get(table_name))

		if flt(total_weightage, 2) != 100.0:
			table = _("KRAs") if table_name == "goals" else _("Criteria")
			dontmanage.throw(
				_("Total weightage for all {0} must add up to 100. Currently, it is {1}%").format(
					dontmanage.bold(table), total_weightage
				),
				title=_("Incorrect Weightage Allocation"),
			)
