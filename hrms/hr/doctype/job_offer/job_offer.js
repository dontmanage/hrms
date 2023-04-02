// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.provide("dontmanageerp.job_offer");

dontmanage.ui.form.on("Job Offer", {
	onload: function (frm) {
		frm.set_query("select_terms", function() {
			return { filters: { hr: 1 } };
		});
	},

	setup: function (frm) {
		frm.email_field = "applicant_email";
	},

	select_terms: function (frm) {
		dontmanageerp.utils.get_terms(frm.doc.select_terms, frm.doc, function (r) {
			if (!r.exc) {
				frm.set_value("terms", r.message);
			}
		});
	},

	refresh: function (frm) {
		if ((!frm.doc.__islocal) && (frm.doc.status == 'Accepted')
			&& (frm.doc.docstatus === 1) && (!frm.doc.__onload || !frm.doc.__onload.employee)) {
			frm.add_custom_button(__('Create Employee'),
				function () {
					dontmanageerp.job_offer.make_employee(frm);
				}
			);
		}

		if(frm.doc.__onload && frm.doc.__onload.employee) {
			frm.add_custom_button(__('Show Employee'),
				function () {
					dontmanage.set_route("Form", "Employee", frm.doc.__onload.employee);
				}
			);
		}
	}

});

dontmanageerp.job_offer.make_employee = function (frm) {
	dontmanage.model.open_mapped_doc({
		method: "hrms.hr.doctype.job_offer.job_offer.make_employee",
		frm: frm
	});
};
