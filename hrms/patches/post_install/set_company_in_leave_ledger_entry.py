import dontmanage


def execute():
	dontmanage.reload_doc("HR", "doctype", "Leave Allocation")
	dontmanage.reload_doc("HR", "doctype", "Leave Ledger Entry")
	dontmanage.db.sql(
		"""
		UPDATE `tabLeave Ledger Entry` as lle
		SET company = (select company from `tabEmployee` where employee = lle.employee)
		WHERE company IS NULL
		"""
	)
	dontmanage.db.sql(
		"""
		UPDATE `tabLeave Allocation` as la
		SET company = (select company from `tabEmployee` where employee = la.employee)
		WHERE company IS NULL
		"""
	)
