# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import scrub
from dontmanage.model.utils.rename_field import rename_field


def execute():
	for doctype in ("Salary Component", "Salary Detail"):
		if dontmanage.db.has_column(doctype, "depends_on_lwp"):
			dontmanage.reload_doc("Payroll", "doctype", scrub(doctype))
			rename_field(doctype, "depends_on_lwp", "depends_on_payment_days")
