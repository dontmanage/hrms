# Copyright (c) 2018, DontManage and Contributors
# See license.txt

import unittest

import dontmanage
from dontmanage.tests.utils import DontManageTestCase
from dontmanage.utils import add_months, getdate

import dontmanageerp
from dontmanageerp.setup.doctype.employee.test_employee import make_employee

from hrms.hr.utils import DuplicateDeclarationError


class TestEmployeeTaxExemptionDeclaration(DontManageTestCase):
	def setUp(self):
		make_employee("employee@taxexemption.com", company="_Test Company")
		make_employee("employee1@taxexemption.com", company="_Test Company")
		create_payroll_period(company="_Test Company")
		create_exemption_category()
		dontmanage.db.delete("Employee Tax Exemption Declaration")
		dontmanage.db.delete("Salary Structure Assignment")

	def test_duplicate_category_in_declaration(self):
		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name"),
				"company": dontmanageerp.get_default_company(),
				"payroll_period": "_Test Payroll Period",
				"currency": dontmanageerp.get_default_currency(),
				"declarations": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=100000,
					),
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=50000,
					),
				],
			}
		)
		self.assertRaises(dontmanage.ValidationError, declaration.save)

	def test_duplicate_entry_for_payroll_period(self):
		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name"),
				"company": dontmanageerp.get_default_company(),
				"payroll_period": "_Test Payroll Period",
				"currency": dontmanageerp.get_default_currency(),
				"declarations": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=100000,
					),
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=50000,
					),
				],
			}
		).insert()

		duplicate_declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name"),
				"company": dontmanageerp.get_default_company(),
				"payroll_period": "_Test Payroll Period",
				"currency": dontmanageerp.get_default_currency(),
				"declarations": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=100000,
					)
				],
			}
		)
		self.assertRaises(DuplicateDeclarationError, duplicate_declaration.insert)
		duplicate_declaration.employee = dontmanage.get_value(
			"Employee", {"user_id": "employee1@taxexemption.com"}, "name"
		)
		self.assertTrue(duplicate_declaration.insert)

	def test_exemption_amount(self):
		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name"),
				"company": dontmanageerp.get_default_company(),
				"payroll_period": "_Test Payroll Period",
				"currency": dontmanageerp.get_default_currency(),
				"declarations": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=80000,
					),
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		self.assertEqual(declaration.total_exemption_amount, 100000)

	def test_india_hra_exemption(self):
		# set country
		current_country = dontmanage.flags.country
		dontmanage.flags.country = "India"

		setup_hra_exemption_prerequisites("Monthly")
		employee = dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name")

		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": "_Test Payroll Period",
				"currency": "INR",
				"monthly_house_rent": 50000,
				"rented_in_metro_city": 1,
				"declarations": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=80000,
					),
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		# Monthly HRA received = 3000
		# should set HRA exemption as per actual annual HRA because that's the minimum
		self.assertEqual(declaration.monthly_hra_exemption, 3000)
		self.assertEqual(declaration.annual_hra_exemption, 36000)
		# 100000 Standard Exemption + 36000 HRA exemption
		self.assertEqual(declaration.total_exemption_amount, 136000)

		# reset
		dontmanage.flags.country = current_country

	def test_india_hra_exemption_with_daily_payroll_frequency(self):
		# set country
		current_country = dontmanage.flags.country
		dontmanage.flags.country = "India"

		setup_hra_exemption_prerequisites("Daily")
		employee = dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name")

		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": "_Test Payroll Period",
				"currency": "INR",
				"monthly_house_rent": 170000,
				"rented_in_metro_city": 1,
				"declarations": [
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		# Daily HRA received = 3000
		# should set HRA exemption as per (rent - 10% of Basic Salary), that's the minimum
		self.assertEqual(declaration.monthly_hra_exemption, 17916.67)
		self.assertEqual(declaration.annual_hra_exemption, 215000)
		# 50000 Standard Exemption + 215000 HRA exemption
		self.assertEqual(declaration.total_exemption_amount, 265000)

		# reset
		dontmanage.flags.country = current_country

	def test_india_hra_exemption_with_weekly_payroll_frequency(self):
		# set country
		current_country = dontmanage.flags.country
		dontmanage.flags.country = "India"

		setup_hra_exemption_prerequisites("Weekly")
		employee = dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name")

		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": "_Test Payroll Period",
				"currency": "INR",
				"monthly_house_rent": 170000,
				"rented_in_metro_city": 1,
				"declarations": [
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		# Weekly HRA received = 3000
		# should set HRA exemption as per actual annual HRA because that's the minimum
		self.assertEqual(declaration.monthly_hra_exemption, 13000)
		self.assertEqual(declaration.annual_hra_exemption, 156000)
		# 50000 Standard Exemption + 156000 HRA exemption
		self.assertEqual(declaration.total_exemption_amount, 206000)

		# reset
		dontmanage.flags.country = current_country

	def test_india_hra_exemption_with_fortnightly_payroll_frequency(self):
		# set country
		current_country = dontmanage.flags.country
		dontmanage.flags.country = "India"

		setup_hra_exemption_prerequisites("Fortnightly")
		employee = dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name")

		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": "_Test Payroll Period",
				"currency": "INR",
				"monthly_house_rent": 170000,
				"rented_in_metro_city": 1,
				"declarations": [
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		# Fortnightly HRA received = 3000
		# should set HRA exemption as per actual annual HRA because that's the minimum
		self.assertEqual(declaration.monthly_hra_exemption, 6500)
		self.assertEqual(declaration.annual_hra_exemption, 78000)
		# 50000 Standard Exemption + 78000 HRA exemption
		self.assertEqual(declaration.total_exemption_amount, 128000)

		# reset
		dontmanage.flags.country = current_country

	def test_india_hra_exemption_with_bimonthly_payroll_frequency(self):
		# set country
		current_country = dontmanage.flags.country
		dontmanage.flags.country = "India"

		setup_hra_exemption_prerequisites("Bimonthly")
		employee = dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name")

		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": "_Test Payroll Period",
				"currency": "INR",
				"monthly_house_rent": 50000,
				"rented_in_metro_city": 1,
				"declarations": [
					dict(
						exemption_sub_category="_Test Sub Category",
						exemption_category="_Test Category",
						amount=80000,
					),
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		# Bimonthly HRA received = 3000
		# should set HRA exemption as per actual annual HRA because that's the minimum
		self.assertEqual(declaration.monthly_hra_exemption, 1500)
		self.assertEqual(declaration.annual_hra_exemption, 18000)
		# 100000 Standard Exemption + 18000 HRA exemption
		self.assertEqual(declaration.total_exemption_amount, 118000)

		# reset
		dontmanage.flags.country = current_country

	def test_india_hra_exemption_with_multiple_salary_structure_assignments(self):
		from hrms.payroll.doctype.salary_slip.test_salary_slip import create_tax_slab
		from hrms.payroll.doctype.salary_structure.test_salary_structure import (
			create_salary_structure_assignment,
			make_salary_structure,
		)

		# set country
		current_country = dontmanage.flags.country
		dontmanage.flags.country = "India"

		employee = make_employee("employee@taxexemption2.com", company="_Test Company")
		payroll_period = create_payroll_period(name="_Test Payroll Period", company="_Test Company")

		create_tax_slab(
			payroll_period,
			allow_tax_exemption=True,
			currency="INR",
			effective_date=getdate("2019-04-01"),
			company="_Test Company",
		)

		dontmanage.db.set_value(
			"Company", "_Test Company", {"basic_component": "Basic Salary", "hra_component": "HRA"}
		)

		# salary structure with base 50000, HRA 3000
		make_salary_structure(
			"Monthly Structure for HRA Exemption 1",
			"Monthly",
			employee=employee,
			company="_Test Company",
			currency="INR",
			payroll_period=payroll_period.name,
			from_date=payroll_period.start_date,
		)

		# salary structure with base 70000, HRA = base * 0.2 = 14000
		salary_structure = make_salary_structure(
			"Monthly Structure for HRA Exemption 2",
			"Monthly",
			employee=employee,
			company="_Test Company",
			currency="INR",
			payroll_period=payroll_period.name,
			from_date=payroll_period.start_date,
			dont_submit=True,
		)
		for component_row in salary_structure.earnings:
			if component_row.salary_component == "HRA":
				component_row.amount = 0
				component_row.amount_based_on_formula = 1
				component_row.formula = "base * 0.2"
				break

		salary_structure.submit()

		create_salary_structure_assignment(
			employee,
			salary_structure.name,
			from_date=add_months(payroll_period.start_date, 6),
			company="_Test Company",
			currency="INR",
			payroll_period=payroll_period.name,
			base=70000,
			allow_duplicate=True,
		)

		declaration = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Declaration",
				"employee": employee,
				"company": "_Test Company",
				"payroll_period": payroll_period.name,
				"currency": "INR",
				"monthly_house_rent": 50000,
				"rented_in_metro_city": 1,
				"declarations": [
					dict(
						exemption_sub_category="_Test1 Sub Category",
						exemption_category="_Test Category",
						amount=60000,
					),
				],
			}
		).insert()

		# Monthly HRA received = 50000 * 6 months + 70000 * 6 months
		# should set HRA exemption as per actual annual HRA because that's the minimum
		self.assertEqual(declaration.monthly_hra_exemption, 8500)
		self.assertEqual(declaration.annual_hra_exemption, 102000)
		# 50000 Standard Exemption + 102000 HRA exemption
		self.assertEqual(declaration.total_exemption_amount, 152000)

		# reset
		dontmanage.flags.country = current_country


def create_payroll_period(**args):
	args = dontmanage._dict(args)
	name = args.name or "_Test Payroll Period"
	if not dontmanage.db.exists("Payroll Period", name):
		from datetime import date

		payroll_period = dontmanage.get_doc(
			dict(
				doctype="Payroll Period",
				name=name,
				company=args.company or dontmanageerp.get_default_company(),
				start_date=args.start_date or date(date.today().year, 1, 1),
				end_date=args.end_date or date(date.today().year, 12, 31),
			)
		).insert()
		return payroll_period
	else:
		return dontmanage.get_doc("Payroll Period", name)


def create_exemption_category():
	if not dontmanage.db.exists("Employee Tax Exemption Category", "_Test Category"):
		category = dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Category",
				"name": "_Test Category",
				"deduction_component": "Income Tax",
				"max_amount": 100000,
			}
		).insert()
	if not dontmanage.db.exists("Employee Tax Exemption Sub Category", "_Test Sub Category"):
		dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Sub Category",
				"name": "_Test Sub Category",
				"exemption_category": "_Test Category",
				"max_amount": 100000,
				"is_active": 1,
			}
		).insert()
	if not dontmanage.db.exists("Employee Tax Exemption Sub Category", "_Test1 Sub Category"):
		dontmanage.get_doc(
			{
				"doctype": "Employee Tax Exemption Sub Category",
				"name": "_Test1 Sub Category",
				"exemption_category": "_Test Category",
				"max_amount": 50000,
				"is_active": 1,
			}
		).insert()


def setup_hra_exemption_prerequisites(frequency, employee=None):
	from hrms.payroll.doctype.salary_slip.test_salary_slip import create_tax_slab
	from hrms.payroll.doctype.salary_structure.test_salary_structure import make_salary_structure

	payroll_period = create_payroll_period(name="_Test Payroll Period", company="_Test Company")
	if not employee:
		employee = dontmanage.get_value("Employee", {"user_id": "employee@taxexemption.com"}, "name")

	create_tax_slab(
		payroll_period,
		allow_tax_exemption=True,
		currency="INR",
		effective_date=getdate("2019-04-01"),
		company="_Test Company",
	)

	make_salary_structure(
		f"{frequency} Structure for HRA Exemption",
		frequency,
		employee=employee,
		company="_Test Company",
		currency="INR",
		payroll_period=payroll_period,
	)

	dontmanage.db.set_value(
		"Company", "_Test Company", {"basic_component": "Basic Salary", "hra_component": "HRA"}
	)
