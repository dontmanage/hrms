// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Department", {
	onload: function(frm) {
		frm.set_query("payroll_cost_center", function() {
			return {
				filters: {
					"company": frm.doc.company,
					"is_group": 0
				}
			};
		});
	}
})