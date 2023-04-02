# Copyright (c) 2015, DontManage and Contributors and Contributors
# See license.txt

import unittest

import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestAppraisalTemplate(DontManageTestCase):
	def test_incorrect_weightage_allocation(self):
		template = create_appraisal_template()
		template.goals[1].per_weightage = 69.99

		self.assertRaises(dontmanage.ValidationError, template.save)

		template.reload()
		template.goals[1].per_weightage = 70.00
		template.save()


def create_kras(kras):
	for entry in kras:
		if not dontmanage.db.exists("KRA", entry):
			dontmanage.get_doc(
				{
					"doctype": "KRA",
					"title": entry,
				}
			).insert()


def create_criteria(criteria):
	for entry in criteria:
		if not dontmanage.db.exists("Employee Feedback Criteria", entry):
			dontmanage.get_doc(
				{
					"doctype": "Employee Feedback Criteria",
					"criteria": entry,
				}
			).insert()


def create_appraisal_template(title=None, kras=None, rating_criteria=None):
	name = title or "Engineering"

	if dontmanage.db.exists("Appraisal Template", name):
		return dontmanage.get_doc("Appraisal Template", name)

	if not kras:
		kras = [
			{
				"kra": "Quality",
				"per_weightage": 30,
			},
			{
				"kra": "Development",
				"per_weightage": 70,
			},
		]

	if not rating_criteria:
		rating_criteria = [
			{
				"criteria": "Problem Solving",
				"per_weightage": 70,
			},
			{
				"criteria": "Excellence",
				"per_weightage": 30,
			},
		]

	create_kras([entry["kra"] for entry in kras])
	create_criteria([entry["criteria"] for entry in rating_criteria])

	appraisal_template = dontmanage.new_doc("Appraisal Template")
	appraisal_template.template_title = name
	appraisal_template.update({"goals": kras})
	appraisal_template.update({"rating_criteria": rating_criteria})
	appraisal_template.insert()

	return appraisal_template
