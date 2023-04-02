import dontmanage


def execute():
	if dontmanage.db.has_column("Leave Type", "based_on_date_of_joining"):
		LeaveType = dontmanage.qb.DocType("Leave Type")
		dontmanage.qb.update(LeaveType).set(LeaveType.allocate_on_day, "Last Day").where(
			(LeaveType.based_on_date_of_joining == 0) & (LeaveType.is_earned_leave == 1)
		).run()

		dontmanage.qb.update(LeaveType).set(LeaveType.allocate_on_day, "Date of Joining").where(
			LeaveType.based_on_date_of_joining == 1
		).run()

		dontmanage.db.sql_ddl("alter table `tabLeave Type` drop column `based_on_date_of_joining`")
