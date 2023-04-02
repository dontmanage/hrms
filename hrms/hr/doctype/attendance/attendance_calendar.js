// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt
dontmanage.views.calendar["Attendance"] = {
	options: {
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month'
		}
	},
	get_events_method: "hrms.hr.doctype.attendance.attendance.get_events"
};
