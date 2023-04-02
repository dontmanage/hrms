# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import dontmanage
from dontmanage.utils import getdate

from hrms.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates

test_dependencies = ["Employee"]
test_records = dontmanage.get_test_records("Leave Block List")


class TestLeaveBlockList(unittest.TestCase):
	def tearDown(self):
		dontmanage.set_user("Administrator")

	def test_get_applicable_block_dates(self):
		dontmanage.set_user("test@example.com")
		dontmanage.db.set_value(
			"Department", "_Test Department - _TC", "leave_block_list", "_Test Leave Block List"
		)
		self.assertTrue(
			getdate("2013-01-02")
			in [d.block_date for d in get_applicable_block_dates("2013-01-01", "2013-01-03")]
		)

	def test_get_applicable_block_dates_for_allowed_user(self):
		dontmanage.set_user("test1@example.com")
		dontmanage.db.set_value(
			"Department", "_Test Department 1 - _TC", "leave_block_list", "_Test Leave Block List"
		)
		self.assertEqual(
			[], [d.block_date for d in get_applicable_block_dates("2013-01-01", "2013-01-03")]
		)

	def test_get_applicable_block_dates_all_lists(self):
		dontmanage.set_user("test1@example.com")
		dontmanage.db.set_value(
			"Department", "_Test Department 1 - _TC", "leave_block_list", "_Test Leave Block List"
		)
		self.assertTrue(
			getdate("2013-01-02")
			in [
				d.block_date for d in get_applicable_block_dates("2013-01-01", "2013-01-03", all_lists=True)
			]
		)

	def test_get_applicable_block_dates_all_lists_for_leave_type(self):
		dontmanage.set_user("test1@example.com")
		dontmanage.db.set_value("Department", "_Test Department 1 - _TC", "leave_block_list", "")

		block_days = [
			d.block_date
			for d in get_applicable_block_dates(
				"2013-01-01", "2013-01-31", all_lists=True, leave_type="Casual Leave"
			)
		]
		self.assertTrue(getdate("2013-01-16") in block_days)
		self.assertTrue(getdate("2013-01-19") in block_days)
		self.assertTrue(getdate("2013-01-02") in block_days)
		self.assertFalse(getdate("2013-01-25") in block_days)

	def test_get_applicable_block_dates_for_allowed_user_for_leave_type(self):
		dontmanage.set_user("test1@example.com")
		dontmanage.db.set_value("Department", "_Test Department 1 - _TC", "leave_block_list", "")

		block_days = [
			d.block_date
			for d in get_applicable_block_dates("2013-01-01", "2013-01-31", leave_type="Casual Leave")
		]
		self.assertTrue(getdate("2013-01-19") in block_days)
		self.assertFalse(getdate("2013-01-16") in block_days)
		self.assertFalse(getdate("2013-01-02") in block_days)
		self.assertFalse(getdate("2013-01-25") in block_days)
