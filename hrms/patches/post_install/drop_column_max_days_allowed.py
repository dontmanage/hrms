import dontmanage


def execute():
	if dontmanage.db.exists("DocType", "Leave Type"):
		if dontmanage.db.has_column("Leave Type", "max_days_allowed"):
			dontmanage.db.sql("alter table `tabLeave Type` drop column max_days_allowed")
