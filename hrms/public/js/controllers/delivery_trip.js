// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Delivery Trip", {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1 && frm.doc.employee) {
			frm.add_custom_button(__("Expense Claim"), function() {
				dontmanage.model.open_mapped_doc({
					method: "hrms.hr.doctype.expense_claim.expense_claim.make_expense_claim_for_delivery_trip",
					frm: frm,
				});
			}, __("Create"));
		}
	}
})