# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class TrainingFeedback(Document):
	def validate(self):
		training_event = dontmanage.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			dontmanage.throw(_("{0} must be submitted").format(_("Training Event")))

		emp_event_details = dontmanage.db.get_value(
			"Training Event Employee",
			{"parent": self.training_event, "employee": self.employee},
			["name", "attendance"],
			as_dict=True,
		)

		if not emp_event_details:
			dontmanage.throw(
				_("Employee {0} not found in Training Event Participants.").format(
					dontmanage.bold(self.employee_name)
				)
			)

		if emp_event_details.attendance == "Absent":
			dontmanage.throw(_("Feedback cannot be recorded for an absent Employee."))

	def on_submit(self):
		employee = dontmanage.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			dontmanage.db.set_value("Training Event Employee", employee, "status", "Feedback Submitted")

	def on_cancel(self):
		employee = dontmanage.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			dontmanage.db.set_value("Training Event Employee", employee, "status", "Completed")
