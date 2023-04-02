import dontmanage


def execute():
	dontmanage.reload_doc("hr", "doctype", "training_event")
	dontmanage.reload_doc("hr", "doctype", "training_event_employee")

	# no need to run the update query as there is no old data
	if not dontmanage.db.exists(
		"Training Event Employee", {"attendance": ("in", ("Mandatory", "Optional"))}
	):
		return

	dontmanage.db.sql(
		"""
		UPDATE `tabTraining Event Employee`
		SET is_mandatory = 1
		WHERE attendance = 'Mandatory'
		"""
	)
	dontmanage.db.sql(
		"""
		UPDATE `tabTraining Event Employee`
		SET attendance = 'Present'
		WHERE attendance in ('Mandatory', 'Optional')
	"""
	)
