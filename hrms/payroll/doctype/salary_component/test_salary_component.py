# Copyright (c) 2015, DontManage and Contributors
# See license.txt

import unittest

import dontmanage

# test_records = dontmanage.get_test_records('Salary Component')


class TestSalaryComponent(unittest.TestCase):
	pass


def create_salary_component(component_name, **args):
	if not dontmanage.db.exists("Salary Component", component_name):
		dontmanage.get_doc(
			{
				"doctype": "Salary Component",
				"salary_component": component_name,
				"type": args.get("type") or "Earning",
				"is_tax_applicable": args.get("is_tax_applicable") or 1,
			}
		).insert()
