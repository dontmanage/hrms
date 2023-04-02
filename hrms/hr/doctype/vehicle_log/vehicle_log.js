// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Vehicle Log", {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__('Expense Claim'), function() {
				frm.events.expense_claim(frm);
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	},

	expense_claim: function(frm){
		dontmanage.call({
			method: "hrms.hr.doctype.vehicle_log.vehicle_log.make_expense_claim",
			args:{
				docname: frm.doc.name
			},
			callback: function(r){
				var doc = dontmanage.model.sync(r.message);
				dontmanage.set_route('Form', 'Expense Claim', r.message.name);
			}
		});
	}
});
