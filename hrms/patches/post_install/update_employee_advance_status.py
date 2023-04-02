import dontmanage


def execute():
	dontmanage.reload_doc("hr", "doctype", "employee_advance")

	advance = dontmanage.qb.DocType("Employee Advance")
	(
		dontmanage.qb.update(advance)
		.set(advance.status, "Returned")
		.where(
			(advance.docstatus == 1)
			& ((advance.return_amount) & (advance.paid_amount == advance.return_amount))
			& (advance.status == "Paid")
		)
	).run()

	(
		dontmanage.qb.update(advance)
		.set(advance.status, "Partly Claimed and Returned")
		.where(
			(advance.docstatus == 1)
			& (
				(advance.claimed_amount & advance.return_amount)
				& (advance.paid_amount == (advance.return_amount + advance.claimed_amount))
			)
			& (advance.status == "Paid")
		)
	).run()
