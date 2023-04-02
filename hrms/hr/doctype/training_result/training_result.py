# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document

from dontmanageerp.setup.doctype.employee.employee import get_employee_emails


class TrainingResult(Document):
	def validate(self):
		training_event = dontmanage.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			dontmanage.throw(_("{0} must be submitted").format(_("Training Event")))

		self.employee_emails = ", ".join(get_employee_emails([d.employee for d in self.employees]))

	def on_submit(self):
		training_event = dontmanage.get_doc("Training Event", self.training_event)
		training_event.status = "Completed"
		for e in self.employees:
			for e1 in training_event.employees:
				if e1.employee == e.employee:
					e1.status = "Completed"
					break

		training_event.save()


@dontmanage.whitelist()
def get_employees(training_event):
	return dontmanage.get_doc("Training Event", training_event).employees
