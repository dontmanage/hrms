import dontmanage


def execute():
	dontmanage.delete_doc("DocType", "Employee Transfer Property", ignore_missing=True)
