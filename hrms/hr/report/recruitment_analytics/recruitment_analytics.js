// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Recruitment Analytics"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"on_date",
			"label": __("On Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.now_date(),
			"reqd": 1,
		},
	]
};
