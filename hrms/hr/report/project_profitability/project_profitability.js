// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Project Profitability"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1)
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": dontmanage.datetime.now_date()
		},
		{
			"fieldname": "customer_name",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		}
	]
};
