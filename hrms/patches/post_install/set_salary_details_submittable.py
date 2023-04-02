import dontmanage


def execute():
	ss = dontmanage.qb.DocType("Salary Structure").as_("ss")
	sd = dontmanage.qb.DocType("Salary Detail").as_("sd")

	(
		dontmanage.qb.update(sd)
		.inner_join(ss)
		.on(ss.name == sd.parent)
		.set(sd.docstatus, 1)
		.where((ss.docstatus == 1) & (sd.parenttype == "Salary Structure"))
	).run()
