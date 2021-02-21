new SimpleBar($("#sidebar")[0]);

$(".nav-tab.suboption, .navbar-toggler").each(function () {
	$(this).click(function () {
		if (window.matchMedia("(max-width: 800px)").matches) {
			if ($("#sidebar").hasClass("collapsed")) {
				$("#sidebar").removeClass("collapsed");
			} else {
				$("#sidebar").addClass("collapsed");
			}
		}
	});
});

create_filter_modal_click_event();
