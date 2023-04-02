// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

/* eslint-disable */
dontmanage.query_reports["Daily Work Summary Replies"] = {
	"filters": [
		{
			"fieldname":"group",
			"label": __("Group"),
			"fieldtype": "Link",
			"options": "Daily Work Summary Group",
			"reqd": 1
		},
		{
			"fieldname": "range",
			"label": __("Date Range"),
			"fieldtype": "DateRange",
			"reqd": 1
		}
	]
}
