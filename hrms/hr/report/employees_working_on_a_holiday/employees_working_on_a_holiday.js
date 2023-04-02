// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.query_reports["Employees working on a holiday"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": dontmanage.datetime.year_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": dontmanage.datetime.year_end()
		},
		{
			"fieldname":"holiday_list",
			"label": __("Holiday List"),
			"fieldtype": "Link",
			"options": "Holiday List"
		}
	]
}
