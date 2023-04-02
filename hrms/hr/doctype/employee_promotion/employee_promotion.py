# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import getdate

from hrms.hr.utils import update_employee_work_history, validate_active_employee


class EmployeePromotion(Document):
	def validate(self):
		validate_active_employee(self.employee)

	def before_submit(self):
		if getdate(self.promotion_date) > getdate():
			dontmanage.throw(
				_("Employee Promotion cannot be submitted before Promotion Date"),
				dontmanage.DocstatusTransitionError,
			)

	def on_submit(self):
		employee = dontmanage.get_doc("Employee", self.employee)
		employee = update_employee_work_history(
			employee, self.promotion_details, date=self.promotion_date
		)

		if self.revised_ctc:
			employee.ctc = self.revised_ctc

		employee.save()

	def on_cancel(self):
		employee = dontmanage.get_doc("Employee", self.employee)
		employee = update_employee_work_history(employee, self.promotion_details, cancel=True)

		if self.revised_ctc:
			employee.ctc = self.current_ctc

		employee.save()
