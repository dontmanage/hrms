// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.views.calendar["Training Event"] = {
	field_map: {
		"start": "start_time",
		"end": "end_time",
		"id": "name",
		"title": "event_name",
		"allDay": "allDay"
	},
	gantt: true,
	get_events_method: "dontmanage.desk.calendar.get_events",
}
