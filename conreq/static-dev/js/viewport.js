let masonry_grid = null;
let infinite_scroller_created = false;
let previous_admin_settings = new Map();
var viewport_container_top_class = ".viewport-container-top";
var viewport_container_class = ".viewport-container";
let viewport_class = ".viewport";
let page_reload_needed = false;
let viewport_http_request = $.ajax({});
let viewport_http_request_aborted = false;
let base_url = $("#base-url").val() + "/";

// Create the lazyloader
var lazyloader = new LazyLoad({
	threshold: 0,
	callback_error: async function (element) {
		element.src = "/static/images/transparent.png";
	},
});

// Hide any floaty objects
let hide_modals_and_popups = async function () {
	$("#modal-container").modal("hide");
	$.magnificPopup.close();
};

// Removes old posters from the infinite scroller to save memory
let cull_old_posters = async function () {
	let viewport_container = $(viewport_container_class);
	let viewport = $(viewport_class);
	if (document.querySelector(".viewport-masonry")) {
		// Logic to delete excess masonry items
		let masonry_items = $(".viewport-masonry > .masonry-item");

		// Calculate the current state of the viewport
		let scroll_position = viewport_container.scrollTop();
		let card_width = $(".masonry-item").outerWidth() + 10;
		let card_height = $(".masonry-item").outerHeight() + 10;
		let viewport_width = viewport.width();
		let viewport_container_height = viewport_container.height();
		let cards_per_row = (viewport_width + 10) / card_width;
		let deletable_num_of_rows = Math.max(
			0,
			Math.floor(
				(scroll_position - viewport_container_height * 6) / card_height
			)
		);
		let num_of_posters_to_delete = deletable_num_of_rows * cards_per_row;

		// If there are posters to delete, do it.
		if (num_of_posters_to_delete > 0 && masonry_grid != null) {
			// Delete the contents of old elements
			masonry_items
				.slice(0, num_of_posters_to_delete)
				.empty()
				.css("padding", "10")
				.text("Hidden to save memory.");

			// Output to console that posters have been deleted
			console.log(
				"Hiding the content of " +
					num_of_posters_to_delete +
					" posters because a new page has loaded."
			);
		}
	}
};

// Updates the current tab based on the URL
let update_active_tab = async function () {
	$(".nav-tab").each(async function () {
		nav_tab = $(this);
		// Set the active tab
		if (
			nav_tab.children("a").attr("href") ==
			"#" + get_window_location_no_params()
		) {
			if (!nav_tab.hasClass("active")) {
				nav_tab.addClass("active");
			}
		}
		// Remove any old active tabs
		else if (nav_tab.hasClass("active")) {
			nav_tab.removeClass("active");
		}
	});
};

// Updates the page name
let update_page_title = async function () {
	document.title = $("#page-name").val() + " - " + $("#app-name").val();
};

// Helper to show the active viewport
let select_active_viewport = async function (viewport_selector) {
	if (viewport_selector == viewport_container_class) {
		$(viewport_container_top_class).attr("hidden", "");
		$(viewport_container_class).removeAttr("hidden");
	} else {
		$(viewport_container_class).attr("hidden", "");
		$(viewport_container_top_class).removeAttr("hidden");
	}
};

// Determine if a cached viewport exists
let cached_viewport_exists = function () {
	return Boolean($("main[data-url='" + get_window_location() + "']").length);
};

// Show the cached viewport
let display_cached_viewport = async function () {
	update_active_tab();
	update_page_title();
	$("main:not([data-url='" + get_window_location() + "'])").attr(
		"hidden",
		""
	);
	$("main[data-url='" + get_window_location() + "']").removeAttr("hidden");
};

// Returns the window location with the base url added
let add_base_url = function (window_location = null) {
	// Get the current location
	if (!window_location) {
		window_location = get_window_location();
	}
	// Append the base URL
	if (window_location && !window_location.startsWith(base_url)) {
		window_location = base_url + window_location;
	}
	return window_location;
};

// Adds viewport related event listeners
let add_viewport_event_listeners = async function (viewport_selector) {
	$(viewport_selector).trigger("add_events");
	// More Info page events
	request_btn_click_event();
	create_content_modal_click_event();
	create_report_modal_click_event();
	issue_approve_btn_click_event();
	issue_delete_btn_click_event();
	quick_info_btn_click_event();
	more_info_poster_popup_click_event();

	// Server Settings menu events
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

	// User Management events
	user_delete_btn_click_event();
	user_invite_btn_click_event();

	// Searchbar
	search_click_event();
};

// Destroys old viewport JS instances
let destroy_viewport = async function (viewport_selector) {
	$(viewport_selector).trigger("destroy");
	// TODO: Make this if statement more intelligent by tying it into an on(viewport_selector) trigger
	if (viewport_selector == viewport_container_class) {
		if (masonry_grid != null) {
			if (infinite_scroller_created) {
				masonry_grid.infiniteScroll("destroy");
				infinite_scroller_created = false;
			}
			masonry_grid.masonry("destroy");
			masonry_grid = null;
		}
	}

	// TODO: Make this if statement more intelligent by tying it into an on(viewport_selector) trigger
	if (viewport_selector == viewport_container_top_class) {
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
	}

	$(viewport_selector + ">*:not(.loading-animation-container)").remove();
};

// Preforms any actions needed to prepare the viewport
let prepare_viewport = async function (viewport_selector) {
	$(viewport_selector).attr("data-url", get_window_location());
	$(viewport_selector).trigger("prepare");
	// Create any carousels that need to be made
	create_all_carousels();

	// Create the masonry grid
	if ($(viewport_selector + ">.viewport-masonry").length) {
		masonry_grid = $(viewport_selector + ">.viewport-masonry").masonry({
			itemSelector: ".masonry-item",
			gutter: 10,
			horizontalOrder: true,
			fitWidth: true,
			transitionDuration: "0s",
			stagger: "0s",
			isStill: true,
		});
	}

	// Configure infinite scrolling
	if ($(viewport_selector + ">.infinite-scroll").length) {
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
				elementScroll: viewport_selector,
				loadOnScroll: false,
				history: false,
				scrollThreshold: $(viewport_selector).height() * 4,
			});

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

	// Lazy load page elements
	lazyloader.update();

	// Add event listeners
	add_viewport_event_listeners(viewport_selector);
};

// Gets the viewport from a URL
let get_viewport = async function (
	location,
	viewport_selector,
	success = function () {}
) {
	$(viewport_selector).trigger("change");
	// Abandon an old http request if the user clicks something else
	if (viewport_http_request.status == undefined) {
		viewport_http_request_aborted = true;
		viewport_http_request.abort();
	}
	// Load the viewport html
	viewport_http_request = $.get(location, function (response = null) {
		return success(response);
	}).fail(async function () {
		if (!viewport_http_request_aborted) {
			conreq_no_response_toast_message();
			$(viewport_container_class).hide();
			$(viewport_container_top_class + ">*").remove();
			$(viewport_container_top_class).append(
				"<p>Could not connect to the server!</p>"
			);
			$(viewport_container_top_class + ">p").css("text-align", "center");
		}
		viewport_http_request_aborted = false;
	});
	return http_request;
};

// Fetch the new viewport and update the current tab
var generate_viewport = async function (fresh_reload = true) {
	hide_modals_and_popups();

	if (cached_viewport_exists()) {
		display_cached_viewport();
	} else {
		let viewport_selector = null;
		if (get_window_location(true).startsWith("display/")) {
			// Display on the top layer
			viewport_selector = viewport_container_top_class;
		} else {
			// Display on the primary viewport
			viewport_selector = viewport_container_class;
		}
		// Check if the whole webpage needs to be reloaded
		if (page_reload_needed) {
			location.reload();
		}

		// Read the URL hash to determine what page we are on
		let window_location = get_window_location();

		// If there is no window location, default to the first tab
		if (!window_location) {
			if (window.history.replaceState) {
				// Replace the current page in the browser history to add a hash
				window.history.replaceState(
					{},
					null,
					$(".nav-tab a").attr("href")
				);
				window_location = window.location.hash.split("#")[1];
			}
		}

		// Change the current tab
		update_active_tab();

		// Asynchronously fetch new viewport content
		viewport_loaded = false;
		get_viewport(
			add_base_url(window_location),
			viewport_selector,
			async function (viewport_html) {
				// Save that the page was successfully loaded
				viewport_loaded = true;

				// Destroy old JS elements and event handlers
				await destroy_viewport(viewport_selector);

				// Inject and configure the new content
				$(viewport_selector)[0].innerHTML = DOMPurify.sanitize(
					viewport_html
				);
				select_active_viewport(viewport_selector);
				await prepare_viewport(viewport_selector);
				update_page_title();
				$(viewport_selector).trigger("loaded");

				// Display the new content
				$(viewport_selector + ">.loading-animation-container").hide();
				$(
					viewport_selector + ">*:not(.loading-animation-container)"
				).show();

				// Set scroll position
				if (fresh_reload) {
					$(viewport_selector).scrollTop(0);
				}
			}
		);

		// If the page is taking too long to load, show a loading animation
		setTimeout(async function () {
			if (!viewport_loaded && fresh_reload) {
				// Hide the viewport and display the loading animation
				select_active_viewport(viewport_selector);
				$(viewport_selector + ">.loading-animation-container").show();
				$(
					viewport_selector + ">*:not(.loading-animation-container)"
				).hide();
			}
		}, 1000);
	}
};

// Perform actions whenever the HTML on the page changes
let page_mutation_observer = async function () {
	let observer = new MutationObserver(async function () {
		$("html").trigger("modified");
		// Initiate Lazyload on any new images
		lazyloader.update();
	});

	// Configuration of the observer
	let config = {
		attributes: false,
		characterData: false,
		subtree: true,
		childList: true,
	};

	// Select the target node
	let target = document.querySelector("body");

	// Begin observing the modal
	observer.observe(target, config);
};

// Slide in animations for navbar, sidebar, and viewport
AOS.init();

// Obtain the initial page
page_mutation_observer();
$(document).ready(generate_viewport);

// Fetch a new page when the URL changes
if ("onhashchange" in window) {
	// Window anchor change event supported
	window.onhashchange = generate_viewport;
} else {
	// Window anchor change event not supported
	let stored_hash = window.location.hash;
	window.setInterval(async function () {
		if (window.location.hash != stored_hash) {
			generate_viewport();
		}
	}, 100);
}
