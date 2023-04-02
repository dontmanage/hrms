dontmanage.provide("dontmanage.dashboards.chart_sources");

dontmanage.dashboards.chart_sources["Hiring vs Attrition Count"] = {
	method: "hrms.hr.dashboard_chart_source.hiring_vs_attrition_count.hiring_vs_attrition_count.get_data",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company")
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: dontmanage.defaults.get_user_default("year_start_date"),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default:  dontmanage.defaults.get_user_default("year_end_date"),
		},
		{
			fieldname: "time_interval",
			label: __("Time Interval"),
			fieldtype: "Select",
			options: ["Monthly", "Quarterly", "Yearly"],
			default:  "Monthly",
			reqd: 1
		},
	]
};
