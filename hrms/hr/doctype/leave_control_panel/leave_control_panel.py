# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _, msgprint
from dontmanage.model.document import Document
from dontmanage.utils import cint, comma_and, cstr, flt


class LeaveControlPanel(Document):
	def get_employees(self):
		conditions, values = [], []
		for field in ["company", "employment_type", "branch", "designation", "department"]:
			if self.get(field):
				conditions.append("{0}=%s".format(field))
				values.append(self.get(field))

		condition_str = " and " + " and ".join(conditions) if len(conditions) else ""

		e = dontmanage.db.sql(
			"select name from tabEmployee where status='Active' {condition}".format(
				condition=condition_str
			),
			tuple(values),
		)

		return e

	def validate_values(self):
		for f in ["from_date", "to_date", "leave_type", "no_of_days"]:
			if not self.get(f):
				dontmanage.throw(_("{0} is required").format(self.meta.get_label(f)))
		self.validate_from_to_dates("from_date", "to_date")

	@dontmanage.whitelist()
	def allocate_leave(self):
		self.validate_values()
		leave_allocated_for = []
		employees = self.get_employees()
		if not employees:
			dontmanage.throw(_("No employee found"))

		for d in self.get_employees():
			try:
				la = dontmanage.new_doc("Leave Allocation")
				la.set("__islocal", 1)
				la.employee = cstr(d[0])
				la.employee_name = dontmanage.db.get_value("Employee", cstr(d[0]), "employee_name")
				la.leave_type = self.leave_type
				la.from_date = self.from_date
				la.to_date = self.to_date
				la.carry_forward = cint(self.carry_forward)
				la.new_leaves_allocated = flt(self.no_of_days)
				la.docstatus = 1
				la.save()
				leave_allocated_for.append(d[0])
			except Exception:
				pass
		if leave_allocated_for:
			msgprint(_("Leaves Allocated Successfully for {0}").format(comma_and(leave_allocated_for)))
