import requests

import dontmanage
from dontmanage.utils import now_datetime

from dontmanageerp.setup.utils import enable_all_roles_and_domains

country_info = {}


@dontmanage.whitelist(allow_guest=True)
def get_country(fields=None):
	global country_info
	ip = dontmanage.local.request_ip

	if ip not in country_info:
		fields = ["countryCode", "country", "regionName", "city"]
		res = requests.get(
			"https://pro.ip-api.com/json/{ip}?key={key}&fields={fields}".format(
				ip=ip, key=dontmanage.conf.get("ip-api-key"), fields=",".join(fields)
			)
		)

		try:
			country_info[ip] = res.json()

		except Exception:
			country_info[ip] = {}

	return country_info[ip]


def before_tests():
	dontmanage.clear_cache()
	# complete setup if missing
	from dontmanage.desk.page.setup_wizard.setup_wizard import setup_complete

	year = now_datetime().year
	if not dontmanage.get_list("Company"):
		setup_complete(
			{
				"currency": "INR",
				"full_name": "Test User",
				"company_name": "Wind Power LLC",
				"timezone": "Asia/Kolkata",
				"company_abbr": "WP",
				"industry": "Manufacturing",
				"country": "India",
				"fy_start_date": f"{year}-01-01",
				"fy_end_date": f"{year}-12-31",
				"language": "english",
				"company_tagline": "Testing",
				"email": "test@dontmanageerp.com",
				"password": "test",
				"chart_of_accounts": "Standard",
			}
		)

	enable_all_roles_and_domains()
	dontmanage.db.commit()  # nosemgrep
