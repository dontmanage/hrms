// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Employee Hours Utilization Based On Timesheet"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: dontmanage.datetime.now_date(),
			reqd: 1
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee"
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department"
		},
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project"
		}
	]
};
