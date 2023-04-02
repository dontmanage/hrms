# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document

from hrms.hr.utils import validate_active_employee


class EmployeeIncentive(Document):
	def validate(self):
		validate_active_employee(self.employee)
		self.validate_salary_structure()

	def validate_salary_structure(self):
		if not dontmanage.db.exists("Salary Structure Assignment", {"employee": self.employee}):
			dontmanage.throw(
				_("There is no Salary Structure assigned to {0}. First assign a Salary Stucture.").format(
					self.employee
				)
			)

	def on_submit(self):
		company = dontmanage.db.get_value("Employee", self.employee, "company")

		additional_salary = dontmanage.new_doc("Additional Salary")
		additional_salary.employee = self.employee
		additional_salary.currency = self.currency
		additional_salary.salary_component = self.salary_component
		additional_salary.overwrite_salary_structure_amount = 0
		additional_salary.amount = self.incentive_amount
		additional_salary.payroll_date = self.payroll_date
		additional_salary.company = company
		additional_salary.ref_doctype = self.doctype
		additional_salary.ref_docname = self.name
		additional_salary.submit()
