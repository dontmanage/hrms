# Copyright (c) 2018, DontManage and Contributors
# See license.txt

import unittest

import dontmanage
from dontmanage.utils import add_days, getdate

from dontmanageerp.setup.doctype.employee.test_employee import make_employee


class TestEmployeeTransfer(unittest.TestCase):
	def setUp(self):
		create_company()

	def tearDown(self):
		dontmanage.db.rollback()

	def test_submit_before_transfer_date(self):
		make_employee("employee2@transfers.com")

		transfer_obj = dontmanage.get_doc(
			{
				"doctype": "Employee Transfer",
				"employee": dontmanage.get_value("Employee", {"user_id": "employee2@transfers.com"}, "name"),
				"transfer_details": [
					{
						"property": "Designation",
						"current": "Software Developer",
						"new": "Project Manager",
						"fieldname": "designation",
					}
				],
			}
		)
		transfer_obj.transfer_date = add_days(getdate(), 1)
		transfer_obj.save()
		self.assertRaises(dontmanage.DocstatusTransitionError, transfer_obj.submit)
		transfer = dontmanage.get_doc("Employee Transfer", transfer_obj.name)
		transfer.transfer_date = getdate()
		transfer.submit()
		self.assertEqual(transfer.docstatus, 1)

	def test_new_employee_creation(self):
		make_employee("employee3@transfers.com")

		transfer = dontmanage.get_doc(
			{
				"doctype": "Employee Transfer",
				"employee": dontmanage.get_value("Employee", {"user_id": "employee3@transfers.com"}, "name"),
				"create_new_employee_id": 1,
				"transfer_date": getdate(),
				"transfer_details": [
					{
						"property": "Designation",
						"current": "Software Developer",
						"new": "Project Manager",
						"fieldname": "designation",
					}
				],
			}
		).insert()
		transfer.submit()
		self.assertTrue(transfer.new_employee_id)
		self.assertEqual(dontmanage.get_value("Employee", transfer.new_employee_id, "status"), "Active")
		self.assertEqual(dontmanage.get_value("Employee", transfer.employee, "status"), "Left")

	def test_employee_history(self):
		employee = make_employee(
			"employee4@transfers.com",
			company="Test Company",
			date_of_birth=getdate("30-09-1980"),
			date_of_joining=getdate("01-10-2021"),
			department="Accounts - TC",
			designation="Accountant",
		)
		transfer = create_employee_transfer(employee)

		count = 0
		department = ["Accounts - TC", "Management - TC"]
		designation = ["Accountant", "Manager"]
		dt = [getdate("01-10-2021"), getdate()]
		to_date = [add_days(dt[1], -1), None]

		employee = dontmanage.get_doc("Employee", employee)
		for data in employee.internal_work_history:
			self.assertEqual(data.department, department[count])
			self.assertEqual(data.designation, designation[count])
			self.assertEqual(data.from_date, dt[count])
			self.assertEqual(data.to_date, to_date[count])
			count = count + 1

		transfer.cancel()
		employee.reload()

		for data in employee.internal_work_history:
			self.assertEqual(data.designation, designation[0])
			self.assertEqual(data.department, department[0])
			self.assertEqual(data.from_date, dt[0])
			self.assertEqual(data.to_date, None)


def create_company():
	if not dontmanage.db.exists("Company", "Test Company"):
		dontmanage.get_doc(
			{
				"doctype": "Company",
				"company_name": "Test Company",
				"default_currency": "INR",
				"country": "India",
			}
		).insert()


def create_employee_transfer(employee):
	doc = dontmanage.get_doc(
		{
			"doctype": "Employee Transfer",
			"employee": employee,
			"transfer_date": getdate(),
			"transfer_details": [
				{
					"property": "Designation",
					"current": "Accountant",
					"new": "Manager",
					"fieldname": "designation",
				},
				{
					"property": "Department",
					"current": "Accounts - TC",
					"new": "Management - TC",
					"fieldname": "department",
				},
			],
		}
	)

	doc.save()
	doc.submit()

	return doc
