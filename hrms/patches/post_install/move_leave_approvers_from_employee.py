import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	dontmanage.reload_doc("hr", "doctype", "department_approver")
	dontmanage.reload_doc("setup", "doctype", "employee")
	dontmanage.reload_doc("setup", "doctype", "department")

	if dontmanage.db.has_column("Department", "leave_approver"):
		rename_field("Department", "leave_approver", "leave_approvers")

	if dontmanage.db.has_column("Department", "expense_approver"):
		rename_field("Department", "expense_approver", "expense_approvers")

	if not dontmanage.db.table_exists("Employee Leave Approver"):
		return

	approvers = dontmanage.db.sql(
		"""select distinct app.leave_approver, emp.department from
	`tabEmployee Leave Approver` app, `tabEmployee` emp
		where app.parenttype = 'Employee'
		and emp.name = app.parent
		""",
		as_dict=True,
	)

	for record in approvers:
		if record.department:
			department = dontmanage.get_doc("Department", record.department)
			if not department:
				return
			if not len(department.leave_approvers):
				department.append("leave_approvers", {"approver": record.leave_approver}).db_insert()
