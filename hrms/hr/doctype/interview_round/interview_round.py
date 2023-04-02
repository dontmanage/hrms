# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt


import json

import dontmanage
from dontmanage.model.document import Document


class InterviewRound(Document):
	pass


@dontmanage.whitelist()
def create_interview(doc):
	if isinstance(doc, str):
		doc = json.loads(doc)
		doc = dontmanage.get_doc(doc)

	interview = dontmanage.new_doc("Interview")
	interview.interview_round = doc.name
	interview.designation = doc.designation

	if doc.interviewers:
		interview.interview_details = []
		for data in doc.interviewers:
			interview.append("interview_details", {"interviewer": data.user})
	return interview
