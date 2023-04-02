import dontmanage
from dontmanage.query_builder import Case


def execute():
	PayrollEntry = dontmanage.qb.DocType("Payroll Entry")

	(
		dontmanage.qb.update(PayrollEntry)
		.set(
			"status",
			Case()
			.when(PayrollEntry.docstatus == 0, "Draft")
			.when(PayrollEntry.docstatus == 1, "Submitted")
			.else_("Cancelled"),
		)
		.where((PayrollEntry.status.notin(["Queued", "Failed"])))
	).run()
