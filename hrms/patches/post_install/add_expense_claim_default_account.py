import dontmanage


def execute():
	dontmanage.reload_doc("setup", "doctype", "company")

	companies = dontmanage.get_all("Company", fields=["name", "default_payable_account"])

	for company in companies:
		if not company.default_expense_claim_payable_account and company.default_payable_account:
			dontmanage.db.set_value(
				"Company",
				company.name,
				"default_expense_claim_payable_account",
				company.default_payable_account,
			)
