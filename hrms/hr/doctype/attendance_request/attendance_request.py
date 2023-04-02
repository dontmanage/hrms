# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import add_days, date_diff, getdate

from dontmanageerp.setup.doctype.employee.employee import is_holiday

from hrms.hr.utils import validate_active_employee, validate_dates


class AttendanceRequest(Document):
	def validate(self):
		validate_active_employee(self.employee)
		validate_dates(self, self.from_date, self.to_date)
		if self.half_day:
			if not getdate(self.from_date) <= getdate(self.half_day_date) <= getdate(self.to_date):
				dontmanage.throw(_("Half day date should be in between from date and to date"))

	def on_submit(self):
		self.create_attendance()

	def on_cancel(self):
		attendance_list = dontmanage.get_list(
			"Attendance", {"employee": self.employee, "attendance_request": self.name}
		)
		if attendance_list:
			for attendance in attendance_list:
				attendance_obj = dontmanage.get_doc("Attendance", attendance["name"])
				attendance_obj.cancel()

	def create_attendance(self):
		request_days = date_diff(self.to_date, self.from_date) + 1
		for number in range(request_days):
			attendance_date = add_days(self.from_date, number)
			skip_attendance = self.validate_if_attendance_not_applicable(attendance_date)
			if not skip_attendance:
				attendance = dontmanage.new_doc("Attendance")
				attendance.employee = self.employee
				attendance.employee_name = self.employee_name
				if self.half_day and date_diff(getdate(self.half_day_date), getdate(attendance_date)) == 0:
					attendance.status = "Half Day"
				elif self.reason == "Work From Home":
					attendance.status = "Work From Home"
				else:
					attendance.status = "Present"
				attendance.attendance_date = attendance_date
				attendance.company = self.company
				attendance.attendance_request = self.name
				attendance.save(ignore_permissions=True)
				attendance.submit()

	def validate_if_attendance_not_applicable(self, attendance_date):
		# Check if attendance_date is a Holiday
		if is_holiday(self.employee, attendance_date):
			dontmanage.msgprint(
				_("Attendance not submitted for {0} as it is a Holiday.").format(attendance_date), alert=1
			)
			return True

		# Check if employee on Leave
		leave_record = dontmanage.db.sql(
			"""select half_day from `tabLeave Application`
			where employee = %s and %s between from_date and to_date
			and docstatus = 1""",
			(self.employee, attendance_date),
			as_dict=True,
		)
		if leave_record:
			dontmanage.msgprint(
				_("Attendance not submitted for {0} as {1} on leave.").format(attendance_date, self.employee),
				alert=1,
			)
			return True

		return False
