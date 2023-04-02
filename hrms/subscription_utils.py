import requests

import dontmanage

STANDARD_ROLES = [
	# standard roles
	"Administrator",
	"All",
	"Guest",
	# accounts
	"Accounts Manager",
	"Accounts User",
	# projects
	"Projects User",
	"Projects Manager",
	# framework
	"Blogger",
	"Dashboard Manager",
	"Inbox User",
	"Newsletter Manager",
	"Prepared Report User",
	"Report Manager",
	"Script Manager",
	"System Manager",
	"Website Manager",
	"Workspace Manager",
]


@dontmanage.whitelist(allow_guest=True)
def get_add_on_details(plan: str) -> dict[str, int]:
	"""
	Returns the number of employees to be billed under add-ons for SAAS subscription
	site_details = {
	        "country": "India",
	        "plan": "Basic",
	        "credit_balance": 1000,
	        "add_ons": {
	                "employee": 2,
	        },
	        "expiry_date": "2021-01-01", # as per current usage
	}
	"""
	EMPLOYEE_LIMITS = {"Basic": 25, "Essential": 50, "Professional": 100}
	add_on_details = {}

	employees_included_in_plan = EMPLOYEE_LIMITS.get(plan)
	if employees_included_in_plan:
		active_employees = get_active_employees()
		add_on_employees = (
			active_employees - employees_included_in_plan
			if active_employees > employees_included_in_plan
			else 0
		)
	else:
		add_on_employees = 0

	add_on_details["employees"] = add_on_employees
	return add_on_details


def get_active_employees() -> int:
	return dontmanage.db.count("Employee", {"status": "Active"})


@dontmanage.whitelist(allow_guest=True)
def subscription_updated(app: str, plan: str):
	if app in ["hrms", "dontmanageerp"] and plan:
		update_dontmanageerp_access()


def update_dontmanageerp_access():
	"""
	ignores if user has no hrms subscription
	enables dontmanageerp workspaces and roles if user has subscribed to hrms and dontmanageerp
	disables dontmanageerp workspaces and roles if user has subscribed to hrms but not dontmanageerp
	"""
	if not dontmanage.utils.get_url().endswith(".dontmanagehr.com"):
		return

	update_dontmanageerp_workspaces(True)
	update_dontmanageerp_roles(True)


def update_dontmanageerp_workspaces(disable: bool = True):
	dontmanageerp_workspaces = [
		"Home",
		"Assets",
		"Accounting",
		"Buying",
		"CRM",
		"DontManageErp Integrations",
		"DontManageErp Settings",
		"Loans",
		"Manufacturing",
		"Quality",
		"Retail",
		"Selling",
		"Stock",
		"Support",
	]

	for workspace in dontmanageerp_workspaces:
		try:
			workspace_doc = dontmanage.get_doc("Workspace", workspace)
			workspace_doc.flags.ignore_links = True
			workspace_doc.flags.ignore_validate = True
			workspace_doc.public = 0 if disable else 1
			workspace_doc.save()
		except Exception:
			pass


def update_dontmanageerp_roles(disable: bool = True):
	roles = get_dontmanageerp_roles()
	for role in roles:
		try:
			role_doc = dontmanage.get_doc("Role", role)
			role_doc.disabled = disable
			role_doc.flags.ignore_links = True
			role_doc.save()
		except Exception:
			pass


def get_dontmanageerp_roles() -> set:
	dontmanageerp_roles = get_roles_for_app("dontmanageerp")
	hrms_roles = get_roles_for_app("hrms")
	return dontmanageerp_roles - hrms_roles - set(STANDARD_ROLES)


def get_roles_for_app(app_name: str) -> set:
	dontmanageerp_modules = get_modules_by_app(app_name)
	doctypes = get_doctypes_by_modules(dontmanageerp_modules)
	roles = roles_by_doctype(doctypes)

	return roles


def get_modules_by_app(app_name: str) -> list:
	return dontmanage.db.get_all("Module Def", filters={"app_name": app_name}, pluck="name")


def get_doctypes_by_modules(modules: list) -> list:
	return dontmanage.db.get_all("DocType", filters={"module": ("in", modules)}, pluck="name")


def roles_by_doctype(doctypes: list) -> set:
	roles = []
	for d in doctypes:
		permissions = dontmanage.get_meta(d).permissions

		for d in permissions:
			roles.append(d.role)

	return set(roles)


def hide_dontmanageerp() -> bool:
	hr_subscription = has_subscription(dontmanage.conf.sk_hrms)
	dontmanageerp_subscription = has_subscription(dontmanage.conf.sk_dontmanageerp_smb or dontmanage.conf.sk_dontmanageerp)

	if not hr_subscription:
		return False

	if hr_subscription and dontmanageerp_subscription:
		# subscribed for DontManageErp
		return False

	# no subscription for DontManageErp
	return True


def has_subscription(secret_key) -> bool:
	url = f"https://dontmanagecloud.com/api/method/press.api.developer.marketplace.get_subscription_status?secret_key={secret_key}"
	response = requests.request(method="POST", url=url, timeout=5)

	status = response.json().get("message")
	return True if status == "Active" else False
