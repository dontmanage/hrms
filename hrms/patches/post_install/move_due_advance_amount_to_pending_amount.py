# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	"""Move from due_advance_amount to pending_amount"""

	if dontmanage.db.has_column("Employee Advance", "due_advance_amount"):
		dontmanage.db.sql(
			"""
			UPDATE `tabEmployee Advance`
			SET pending_amount=due_advance_amount
			WHERE pending_amount IS NULL AND due_advance_amount IS NOT NULL
		"""
		)
