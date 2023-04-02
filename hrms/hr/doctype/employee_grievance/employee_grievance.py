# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _, bold
from dontmanage.model.document import Document


class EmployeeGrievance(Document):
	def on_submit(self):
		if self.status not in ["Invalid", "Resolved"]:
			dontmanage.throw(
				_("Only Employee Grievance with status {0} or {1} can be submitted").format(
					bold("Invalid"), bold("Resolved")
				)
			)
