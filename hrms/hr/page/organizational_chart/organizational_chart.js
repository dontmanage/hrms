dontmanage.pages['organizational-chart'].on_page_load = function(wrapper) {
	dontmanage.ui.make_app_page({
		parent: wrapper,
		title: __('Organizational Chart'),
		single_column: true
	});

	$(wrapper).bind('show', () => {
		dontmanage.require('hierarchy-chart.bundle.js', () => {
			let organizational_chart = undefined;
			let method = 'hrms.hr.page.organizational_chart.organizational_chart.get_children';

			if (dontmanage.is_mobile()) {
				organizational_chart = new dontmanageerp.HierarchyChartMobile('Employee', wrapper, method);
			} else {
				organizational_chart = new dontmanageerp.HierarchyChart('Employee', wrapper, method);
			}

			dontmanage.breadcrumbs.add('HR');
			organizational_chart.show();
		});
	});
};
