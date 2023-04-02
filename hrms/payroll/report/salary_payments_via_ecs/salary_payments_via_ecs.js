// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.require("assets/hrms/js/salary_slip_deductions_report_filters.js", function() {

	let ecs_checklist_filter = hrms.salary_slip_deductions_report_filters
	ecs_checklist_filter['filters'].push({
		fieldname: "type",
		label: __("Type"),
		fieldtype: "Select",
		options:["", "Bank", "Cash", "Cheque"]
	})

	dontmanage.query_reports["Salary Payments via ECS"] = ecs_checklist_filter
});
