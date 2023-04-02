import dontmanage


def execute():
	if dontmanage.db.table_exists("Offer Letter") and not dontmanage.db.table_exists("Job Offer"):
		dontmanage.rename_doc("DocType", "Offer Letter", "Job Offer", force=True)
		dontmanage.rename_doc("DocType", "Offer Letter Term", "Job Offer Term", force=True)
		dontmanage.reload_doc("hr", "doctype", "job_offer")
		dontmanage.reload_doc("hr", "doctype", "job_offer_term")

		dontmanage.delete_doc_if_exists("Print Format", {"name": "Offer Letter", "standard": "Yes"})
