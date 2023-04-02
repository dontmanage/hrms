# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("hr", "doctype", "shift_assignment")
	if dontmanage.db.has_column("Shift Assignment", "date"):
		dontmanage.db.sql(
			"""update `tabShift Assignment`
            set end_date=date, start_date=date
            where date IS NOT NULL and start_date IS NULL and end_date IS NULL;"""
		)
