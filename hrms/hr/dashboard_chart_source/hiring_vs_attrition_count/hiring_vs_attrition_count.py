# Copyright (c) 2022, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _
from dontmanage.desk.doctype.dashboard_chart.dashboard_chart import get_result
from dontmanage.utils import getdate
from dontmanage.utils.dashboard import cache_source
from dontmanage.utils.dateutils import get_period


@dontmanage.whitelist()
@cache_source
def get_data(
	chart_name=None,
	chart=None,
	no_cache=None,
	filters=None,
	from_date=None,
	to_date=None,
	timespan=None,
	time_interval=None,
	heatmap_year=None,
) -> dict[str, list]:
	if filters:
		filters = dontmanage.parse_json(filters)

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if not to_date:
		to_date = getdate()

	hiring = get_records(from_date, to_date, "date_of_joining", filters.get("company"))
	attrition = get_records(from_date, to_date, "relieving_date", filters.get("company"))

	hiring_data = get_result(hiring, filters.get("time_interval"), from_date, to_date, "Count")
	attrition_data = get_result(attrition, filters.get("time_interval"), from_date, to_date, "Count")

	return {
		"labels": [get_period(r[0], filters.get("time_interval")) for r in hiring_data],
		"datasets": [
			{"name": _("Hiring Count"), "values": [r[1] for r in hiring_data]},
			{"name": _("Attrition Count"), "values": [r[1] for r in attrition_data]},
		],
	}


def get_records(
	from_date: str, to_date: str, datefield: str, company: str
) -> tuple[tuple[str, float, int]]:
	filters = [
		["Employee", "company", "=", company],
		["Employee", datefield, ">=", from_date, False],
		["Employee", datefield, "<=", to_date, False],
	]

	data = dontmanage.db.get_list(
		"Employee",
		fields=[f"{datefield} as _unit", "SUM(1)", "COUNT(*)"],
		filters=filters,
		group_by="_unit",
		order_by="_unit asc",
		as_list=True,
		ignore_ifnull=True,
	)

	return data
