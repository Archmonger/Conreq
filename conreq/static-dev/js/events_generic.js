$(document).ready(async function () {
	$(".viewport-container").on("prepare", async function () {
		if ($("table").length) {
			$("table").bootstrapTable();
		}
	});

	$(".viewport-container").on("destroy", async function () {
		if ($("table").length) {
			$("table").bootstrapTable("destroy");
		}
	});

	$(".viewport-container").on("loaded-cached", async function () {
		if (masonry_grid != null) {
			masonry_grid.masonry("layout");
		}
		$(youtube_players).each(function () {
			if (this.stopVideo) {
				this.stopVideo();
			}
		});
	});

	$(".sidebar").on("loaded", async function () {
		sidebar_collapse_click_event();
		create_filter_modal_click_event();
		manage_user_btn_click_event();
	});
});
