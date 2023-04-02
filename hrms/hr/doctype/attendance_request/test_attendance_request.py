# Copyright (c) 2018, DontManage and Contributors
# See license.txt

import unittest
from datetime import date

import dontmanage
from dontmanage.utils import nowdate

test_dependencies = ["Employee"]


class TestAttendanceRequest(unittest.TestCase):
	def setUp(self):
		for doctype in ["Attendance Request", "Attendance"]:
			dontmanage.db.sql("delete from `tab{doctype}`".format(doctype=doctype))

	def tearDown(self):
		dontmanage.db.rollback()

	def test_on_duty_attendance_request(self):
		"Test creation/updation of Attendace from Attendance Request, on duty."
		today = nowdate()
		employee = get_employee()
		attendance_request = dontmanage.new_doc("Attendance Request")
		attendance_request.employee = employee.name
		attendance_request.from_date = date(date.today().year, 1, 1)
		attendance_request.to_date = date(date.today().year, 1, 2)
		attendance_request.reason = "On Duty"
		attendance_request.company = "_Test Company"
		attendance_request.insert()
		attendance_request.submit()

		attendance = dontmanage.db.get_value(
			"Attendance",
			filters={
				"attendance_request": attendance_request.name,
				"attendance_date": date(date.today().year, 1, 1),
			},
			fieldname=["status", "docstatus"],
			as_dict=True,
		)
		self.assertEqual(attendance.status, "Present")
		self.assertEqual(attendance.docstatus, 1)

		# cancelling attendance request cancels linked attendances
		attendance_request.cancel()

		# cancellation alters docname
		# fetch attendance value again to avoid stale docname
		attendance_docstatus = dontmanage.db.get_value(
			"Attendance",
			filters={
				"attendance_request": attendance_request.name,
				"attendance_date": date(date.today().year, 1, 1),
			},
			fieldname="docstatus",
		)
		self.assertEqual(attendance_docstatus, 2)

	def test_work_from_home_attendance_request(self):
		"Test creation/updation of Attendace from Attendance Request, work from home."
		today = nowdate()
		employee = get_employee()
		attendance_request = dontmanage.new_doc("Attendance Request")
		attendance_request.employee = employee.name
		attendance_request.from_date = date(date.today().year, 1, 1)
		attendance_request.to_date = date(date.today().year, 1, 2)
		attendance_request.reason = "Work From Home"
		attendance_request.company = "_Test Company"
		attendance_request.insert()
		attendance_request.submit()

		attendance_status = dontmanage.db.get_value(
			"Attendance",
			filters={
				"attendance_request": attendance_request.name,
				"attendance_date": date(date.today().year, 1, 1),
			},
			fieldname="status",
		)
		self.assertEqual(attendance_status, "Work From Home")

		attendance_request.cancel()

		# cancellation alters docname
		# fetch attendance value again to avoid stale docname
		attendance_docstatus = dontmanage.db.get_value(
			"Attendance",
			filters={
				"attendance_request": attendance_request.name,
				"attendance_date": date(date.today().year, 1, 1),
			},
			fieldname="docstatus",
		)
		self.assertEqual(attendance_docstatus, 2)


def get_employee():
	return dontmanage.get_doc("Employee", "_T-Employee-00001")
