$(document).ready(async function () {
	$(".viewport-container").on("prepare", async function () {
		// User Management events
		manage_user_btn_click_event();
		delete_user_btn_click_event();
		invite_user_btn_click_event();

		// Searchbar
		search_click_event();

		// Server Settings
		$(
			'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
		).each(async function () {
			let setting_name = $(this).data("setting-name");
			let current_value = $(this).val();
			previous_admin_settings[setting_name] = current_value;
		});
		$(
			'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
		).on("keypress", function (e) {
			let setting_name = $(this).data("setting-name");
			let current_value = $(this).val();
			if (e.which == 13) {
				change_server_setting(setting_name, current_value);
				previous_admin_settings[setting_name] = current_value;
			}
		});
		$(
			'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
		).focusout(async function () {
			let setting_name = $(this).data("setting-name");
			let current_value = $(this).val();
			if (previous_admin_settings[setting_name] != current_value) {
				change_server_setting(setting_name, current_value);
				previous_admin_settings[setting_name] = current_value;
			}
		});
		$(".toggler .settings-item.admin").change(async function () {
			let setting_name = $(this).data("setting-name");
			let current_value = $(this).children("input").is(":checked");
			change_server_setting(setting_name, current_value);
		});
		server_settings_dropdown_click_event();
		refresh_api_key_click_event();
		reload_needed_click_event();

		// Bootstrap Table
		if ($("table").length) {
			$("table").bootstrapTable();
		}

		// Masonry Grid
		if ($(".viewport-container>.viewport-masonry").length) {
			masonry_grid = $(".viewport-container>.viewport-masonry").masonry({
				itemSelector: ".masonry-item",
				gutter: 10,
				horizontalOrder: true,
				fitWidth: true,
				transitionDuration: "0s",
				stagger: "0s",
				isStill: true,
			});
		}

		// Infinite Scroller
		if ($(".viewport-container>.infinite-scroll").length) {
			let elements_path = null;
			if (get_window_location().includes("?")) {
				elements_path = get_window_location() + "&page={{#}}";
			} else {
				elements_path = get_window_location() + "?page={{#}}";
			}
			setTimeout(async function () {
				masonry_grid.infiniteScroll({
					path: elements_path,
					append: ".masonry-item",
					outlayer: masonry_grid.data("masonry"),
					prefill: true,
					elementScroll: ".viewport-container",
					loadOnScroll: false,
					history: false,
					scrollThreshold: $(".viewport-container").height() * 4,
				});

				create_content_modal_click_event();

				masonry_grid.on("append.infiniteScroll", async function () {
					cull_old_posters();
					create_content_modal_click_event();
					timer_start();
				});

				// Only load new page if X seconds have elapsed (rate limit)
				masonry_grid.on(
					"scrollThreshold.infiniteScroll",
					async function () {
						if (timer_seconds() >= 1) {
							masonry_grid.infiniteScroll("loadNextPage");
						}
					}
				);

				infinite_scroller_created = true;
			}, 500);
		}
	});

	$(".viewport-container").on("destroy", function () {
		// Bootstrap Table
		if ($("table").length) {
			$("table").bootstrapTable("destroy");
		}

		// Infinite Scroller
		if (masonry_grid != null) {
			if (infinite_scroller_created) {
				masonry_grid.infiniteScroll("destroy");
				infinite_scroller_created = false;
			}
			masonry_grid.masonry("destroy");
			masonry_grid = null;
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

	$(".viewport-container-top").on("prepare", async function () {
		// Create any carousels that need to be made
		create_all_carousels();

		// More Info page events
		request_btn_click_event();
		create_content_modal_click_event();
		create_report_modal_click_event();
		issue_approve_btn_click_event();
		issue_delete_btn_click_event();
		quick_info_btn_click_event();
		more_info_poster_popup_click_event();
	});

	$(".viewport-container-top").on("destroy", async function () {
		// Carousels
		if (review_carousel != null) {
			review_carousel.destroy();
			review_carousel = null;
		}
		if (videos_carousel != null) {
			videos_carousel.destroy();
			videos_carousel = null;
		}
		if (recommended_carousel != null) {
			recommended_carousel.destroy();
			recommended_carousel = null;
		}
		if (images_carousel != null) {
			images_carousel.destroy();
			images_carousel = null;
		}
		if (collection_carousel != null) {
			collection_carousel.destroy();
			collection_carousel = null;
		}
		if (cast_carousel != null) {
			cast_carousel.destroy();
			cast_carousel = null;
		}
		if (crew_carousel != null) {
			crew_carousel.destroy();
			crew_carousel = null;
		}
	});

	$(".sidebar").on("loaded", async function () {
		sidebar_collapse_click_event();
		create_filter_modal_click_event();
		manage_user_btn_click_event();
	});
});
