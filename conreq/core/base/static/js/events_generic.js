$(document).ready(async function () {
	$(".viewport-container").on("loaded", async function () {
		// Bootstrap Table
		if ($("table").length) {
			$("table").bootstrapTable();
		}

		// User Management events
		invite_user_btn_click_event();
	});

	$(".viewport-container").on("destroy", function () {
		// Bootstrap Table
		if ($("table").length) {
			$("table").bootstrapTable("destroy");
		}
	});

	$(".sidebar").on("loaded", async function () {
		sidebar_collapse_click_event();
		manage_user_btn_click_event();
	});
});
