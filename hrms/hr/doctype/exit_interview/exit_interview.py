# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import get_link_to_form

from dontmanageerp.setup.doctype.employee.employee import get_employee_email


class ExitInterview(Document):
	def validate(self):
		self.validate_relieving_date()
		self.validate_duplicate_interview()
		self.set_employee_email()

	def validate_relieving_date(self):
		if not dontmanage.db.get_value("Employee", self.employee, "relieving_date"):
			dontmanage.throw(
				_("Please set the relieving date for employee {0}").format(
					get_link_to_form("Employee", self.employee)
				),
				title=_("Relieving Date Missing"),
			)

	def validate_duplicate_interview(self):
		doc = dontmanage.db.exists(
			"Exit Interview", {"employee": self.employee, "name": ("!=", self.name), "docstatus": ("!=", 2)}
		)
		if doc:
			dontmanage.throw(
				_("Exit Interview {0} already exists for Employee: {1}").format(
					get_link_to_form("Exit Interview", doc), dontmanage.bold(self.employee)
				),
				dontmanage.DuplicateEntryError,
			)

	def set_employee_email(self):
		employee = dontmanage.get_doc("Employee", self.employee)
		self.email = get_employee_email(employee)

	def on_submit(self):
		if self.status != "Completed":
			dontmanage.throw(_("Only Completed documents can be submitted"))

		self.update_interview_date_in_employee()

	def on_cancel(self):
		self.update_interview_date_in_employee()
		self.db_set("status", "Cancelled")

	def update_interview_date_in_employee(self):
		if self.docstatus == 1:
			dontmanage.db.set_value("Employee", self.employee, "held_on", self.date)
		elif self.docstatus == 2:
			dontmanage.db.set_value("Employee", self.employee, "held_on", None)


@dontmanage.whitelist()
def send_exit_questionnaire(interviews):
	interviews = get_interviews(interviews)
	validate_questionnaire_settings()

	email_success = []
	email_failure = []

	for exit_interview in interviews:
		interview = dontmanage.get_doc("Exit Interview", exit_interview.get("name"))
		if interview.get("questionnaire_email_sent"):
			continue

		employee = dontmanage.get_doc("Employee", interview.employee)
		email = get_employee_email(employee)

		context = interview.as_dict()
		context.update(employee.as_dict())
		template_name = dontmanage.db.get_single_value(
			"HR Settings", "exit_questionnaire_notification_template"
		)
		template = dontmanage.get_doc("Email Template", template_name)

		if email:
			dontmanage.sendmail(
				recipients=email,
				subject=template.subject,
				message=dontmanage.render_template(template.response, context),
				reference_doctype=interview.doctype,
				reference_name=interview.name,
			)
			interview.db_set("questionnaire_email_sent", 1)
			interview.notify_update()
			email_success.append(email)
		else:
			email_failure.append(get_link_to_form("Employee", employee.name))

	show_email_summary(email_success, email_failure)


def get_interviews(interviews):
	import json

	if isinstance(interviews, str):
		interviews = json.loads(interviews)

	if not len(interviews):
		dontmanage.throw(_("Atleast one interview has to be selected."))

	return interviews


def validate_questionnaire_settings():
	settings = dontmanage.db.get_value(
		"HR Settings",
		"HR Settings",
		["exit_questionnaire_web_form", "exit_questionnaire_notification_template"],
		as_dict=True,
	)

	if (
		not settings.exit_questionnaire_web_form or not settings.exit_questionnaire_notification_template
	):
		dontmanage.throw(
			_("Please set {0} and {1} in {2}.").format(
				dontmanage.bold("Exit Questionnaire Web Form"),
				dontmanage.bold("Notification Template"),
				get_link_to_form("HR Settings", "HR Settings"),
			),
			title=_("Settings Missing"),
		)


def show_email_summary(email_success, email_failure):
	message = ""
	if email_success:
		message += _("{0}: {1}").format(dontmanage.bold("Sent Successfully"), ", ".join(email_success))
	if message and email_failure:
		message += "<br><br>"
	if email_failure:
		message += _("{0} due to missing email information for employee(s): {1}").format(
			dontmanage.bold("Sending Failed"), ", ".join(email_failure)
		)

	dontmanage.msgprint(
		message, title=_("Exit Questionnaire"), indicator="blue", is_minimizable=True, wide=True
	)
