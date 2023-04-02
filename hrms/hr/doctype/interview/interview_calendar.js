
dontmanage.views.calendar['Interview'] = {
	field_map: {
		'start': 'from',
		'end': 'to',
		'id': 'name',
		'title': 'subject',
		'allDay': 'allDay',
		'color': 'color'
	},
	order_by: 'scheduled_on',
	gantt: true,
	get_events_method: 'hrms.hr.doctype.interview.interview.get_events'
};
