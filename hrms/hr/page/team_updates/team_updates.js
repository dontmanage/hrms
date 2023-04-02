dontmanage.pages['team-updates'].on_page_load = function(wrapper) {
	var page = dontmanage.ui.make_app_page({
		parent: wrapper,
		title: __('Team Updates'),
		single_column: true
	});

	dontmanage.team_updates.make(page);
	dontmanage.team_updates.run();

	if(dontmanage.model.can_read('Daily Work Summary Group')) {
		page.add_menu_item(__('Daily Work Summary Group'), function() {
			dontmanage.set_route('Form', 'Daily Work Summary Group');
		});
	}
}

dontmanage.team_updates = {
	start: 0,
	make: function(page) {
		var me = dontmanage.team_updates;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		me.more = $('<div class="for-more"><button class="btn btn-sm btn-default btn-more">'
			+ __("More") + '</button></div>').appendTo(me.page.main)
			.find('.btn-more').on('click', function() {
				me.start += 40;
				me.run();
			});
	},
	run: function() {
		var me = dontmanage.team_updates;
		dontmanage.call({
			method: 'hrms.hr.page.team_updates.team_updates.get_data',
			args: {
				start: me.start
			},
			callback: function(r) {
				if (r.message && r.message.length > 0) {
					r.message.forEach(function(d) {
						me.add_row(d);
					});
				} else {
					dontmanage.show_alert({message: __('No more updates'), indicator: 'gray'});
					me.more.parent().addClass('hidden');
				}
			}
		});
	},
	add_row: function(data) {
		var me = dontmanage.team_updates;

		data.by = dontmanage.user.full_name(data.sender);
		data.avatar = dontmanage.avatar(data.sender);
		data.when = comment_when(data.creation);

		var date = dontmanage.datetime.str_to_obj(data.creation);
		var last = me.last_feed_date;

		if((last && dontmanage.datetime.obj_to_str(last) != dontmanage.datetime.obj_to_str(date)) || (!last)) {
			var diff = dontmanage.datetime.get_day_diff(dontmanage.datetime.get_today(), dontmanage.datetime.obj_to_str(date));
			var pdate;
			if(diff < 1) {
				pdate = 'Today';
			} else if(diff < 2) {
				pdate = 'Yesterday';
			} else {
				pdate = dontmanage.datetime.global_date_format(date);
			}
			data.date_sep = pdate;
			data.date_class = pdate=='Today' ? "date-indicator blue" : "date-indicator";
		} else {
			data.date_sep = null;
			data.date_class = "";
		}
		me.last_feed_date = date;

		$(dontmanage.render_template('team_update_row', data)).appendTo(me.body);
	}
}
