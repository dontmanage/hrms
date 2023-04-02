// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Employee Onboarding Template', {
	setup: function(frm) {
		frm.set_query("department", function() {
			return {
				filters: {
					company: frm.doc.company
				}
			};
		});
	}
});
