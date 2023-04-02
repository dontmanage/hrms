# Copyright (c) 2020, DontManage and Contributors
# MIT License. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("setup", "doctype", "employee")

	if dontmanage.db.has_column("Employee", "reason_for_resignation"):
		dontmanage.db.sql(
			""" UPDATE `tabEmployee`
            SET reason_for_leaving = reason_for_resignation
            WHERE status = 'Left' and reason_for_leaving is null and reason_for_resignation is not null
        """
		)
