// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Daily Work Summary Group', {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Daily Work Summary'), function () {
				dontmanage.set_route('List', 'Daily Work Summary');
			});
		}
	}
});
