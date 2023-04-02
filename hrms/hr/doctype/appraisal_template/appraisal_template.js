// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Appraisal Template", {
	setup(frm) {
		frm.get_field("rating_criteria").grid.editable_fields = [
			{fieldname: "criteria", columns: 6},
			{fieldname: "per_weightage", columns: 5},
		];
	},
});
