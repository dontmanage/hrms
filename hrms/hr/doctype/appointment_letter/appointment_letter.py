# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class AppointmentLetter(Document):
	pass


@dontmanage.whitelist()
def get_appointment_letter_details(template):
	body = []
	intro = dontmanage.get_list(
		"Appointment Letter Template",
		fields=["introduction", "closing_notes"],
		filters={"name": template},
	)[0]
	content = dontmanage.get_all(
		"Appointment Letter content",
		fields=["title", "description"],
		filters={"parent": template},
		order_by="idx",
	)
	body.append(intro)
	body.append({"description": content})
	return body
