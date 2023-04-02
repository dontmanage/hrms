# Copyright (c) 2015, DontManage and Contributors and Contributors
# See license.txt

import unittest

import dontmanage

from dontmanageerp.setup.doctype.designation.test_designation import create_designation


class TestJobApplicant(unittest.TestCase):
	def test_job_applicant_naming(self):
		applicant = dontmanage.get_doc(
			{
				"doctype": "Job Applicant",
				"status": "Open",
				"applicant_name": "_Test Applicant",
				"email_id": "job_applicant_naming@example.com",
			}
		).insert()
		self.assertEqual(applicant.name, "job_applicant_naming@example.com")

		applicant = dontmanage.get_doc(
			{
				"doctype": "Job Applicant",
				"status": "Open",
				"applicant_name": "_Test Applicant",
				"email_id": "job_applicant_naming@example.com",
			}
		).insert()
		self.assertEqual(applicant.name, "job_applicant_naming@example.com-1")

	def tearDown(self):
		dontmanage.db.rollback()


def create_job_applicant(**args):
	args = dontmanage._dict(args)

	filters = {
		"applicant_name": args.applicant_name or "_Test Applicant",
		"email_id": args.email_id or "test_applicant@example.com",
	}

	if dontmanage.db.exists("Job Applicant", filters):
		return dontmanage.get_doc("Job Applicant", filters)

	job_applicant = dontmanage.get_doc(
		{
			"doctype": "Job Applicant",
			"status": args.status or "Open",
			"designation": create_designation().name,
		}
	)

	job_applicant.update(filters)
	job_applicant.save()

	return job_applicant
