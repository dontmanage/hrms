import dontmanage

# this patch should have been included with this PR https://github.com/dontmanage/dontmanageerp/pull/14302


def execute():
	if dontmanage.db.table_exists("Additional Salary Component"):
		if not dontmanage.db.table_exists("Additional Salary"):
			dontmanage.rename_doc("DocType", "Additional Salary Component", "Additional Salary")

		dontmanage.delete_doc("DocType", "Additional Salary Component")
