// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Bank Transaction", {
	get_payment_doctypes: function() {
		return [
			"Payment Entry",
			"Journal Entry",
			"Sales Invoice",
			"Purchase Invoice",
			"Expense Claim",
		];
	}
})