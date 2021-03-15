let masonry_grid = null;
let infinite_scroller_created = false;
let previous_admin_settings = new Map();
let viewport_container_class = ".viewport-container";
let viewport_class = ".viewport";
let page_reload_needed = false;
let viewport_http_request = $.ajax({});
let viewport_http_request_aborted = false;
let base_url = $("#base-url").val() + "/";

// Create the lazyloader
let callback_error = async function (element) {
	element.src = "/static/images/transparent.png";
};
var lazyloader = new LazyLoad({
	threshold: 0,
	callback_error: callback_error,
});

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
			"#" + add_base_url(get_window_location_no_params())
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

// Sets and returns the window location with the base url removed
let remove_base_url = function (
	window_location = null,
	set_window_location = true
) {
	// Get the current location
	if (!window_location) {
		window_location = get_window_location();
	}
	// Remove the base URL
	if (window_location && window_location.startsWith(base_url)) {
		window_location = window_location.slice(base_url.length);
	}
	// Replace the current page in the browser history
	if (set_window_location && window.history.replaceState) {
		window.history.replaceState({}, null, "#" + window_location);
	}
	return window_location;
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
let add_viewport_event_listeners = async function () {
	$(".viewport-container").trigger("add_events");
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
let destroy_viewport = async function () {
	$(".viewport-container").trigger("destroy");
	if (masonry_grid != null) {
		if (infinite_scroller_created) {
			masonry_grid.infiniteScroll("destroy");
			infinite_scroller_created = false;
		}
		masonry_grid.masonry("destroy");
		masonry_grid = null;
	}
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

	$(".viewport-container>*:not(.loading-animation-container)").remove();
};

// Preforms any actions needed to prepare the viewport
let prepare_viewport = async function () {
	$(".viewport-container").trigger("prepare");
	// Create any carousels that need to be made
	create_all_carousels();

	// Create the masonry grid
	masonry_grid = $(".viewport-masonry").masonry({
		itemSelector: ".masonry-item",
		gutter: 10,
		horizontalOrder: true,
		fitWidth: true,
		transitionDuration: "0s",
		stagger: "0s",
		isStill: true,
	});

	// Configure infinite scrolling
	if ($(".infinite-scroll").length) {
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
	add_viewport_event_listeners();
};

// Gets the viewport from a URL
let get_viewport = async function (location, success = function () {}) {
	$(".viewport-container").trigger("change");
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
			$(".viewport-container>*").remove();
			$(".viewport-container").append(
				"<p>Could not connect to the server!</p>"
			);
			$(".viewport-container>p").css("text-align", "center");
		}
		viewport_http_request_aborted = false;
	});
	return http_request;
};

// Fetch the new viewport and update the current tab
var generate_viewport = async function (fresh_reload = true) {
	// Check if the whole webpage needs to be reloaded
	if (page_reload_needed && fresh_reload) {
		location.reload();
	}

	// Read the URL hash to determine what page we are on
	let window_location = get_window_location();

	// If there is no window location, default to the first tab
	if (!window_location) {
		if (window.history.replaceState) {
			// Replace the current page in the browser history to add a hash
			window.history.replaceState({}, null, $(".nav-tab a").attr("href"));
			window_location = window.location.hash.split("#")[1];
		}
	}

	// Make the URL pretty by removing the base URL
	remove_base_url();

	// Change the current tab
	update_active_tab();

	// Asynchronously fetch new viewport content
	viewport_loaded = false;
	get_viewport(add_base_url(window_location), async function (viewport_html) {
		// Save that the page was successfully loaded
		viewport_loaded = true;

		// Destroy old JS elements and event handlers
		await destroy_viewport();

		// Inject and configure the new content
		$(".viewport-container")[0].innerHTML = DOMPurify.sanitize(
			viewport_html
		);
		await prepare_viewport();
		update_page_title();
		$(".viewport-container").trigger("loaded");

		// Display the new content
		$(".viewport-container>.loading-animation-container").hide();
		$(".viewport-container>*:not(.loading-animation-container)").show();

		// Set scroll position
		if (fresh_reload) {
			$(viewport_container_class).scrollTop(0);
		}
	});

	// If the page is taking too long to load, show a loading animation
	setTimeout(async function () {
		if (!viewport_loaded && fresh_reload) {
			// Hide the viewport and display the loading animation
			$(".viewport-container>.loading-animation-container").show();
			$(".viewport-container>*:not(.loading-animation-container)").hide();
		}
	}, 1000);
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
$(document).ready(async function () {
	generate_viewport();
});

// Fetch a new page when the URL changes
if ("onhashchange" in window) {
	// Window anchor change event supported
	window.onhashchange = async function () {
		generate_viewport();
	};
} else {
	// Window anchor change event not supported
	var storedHash = window.location.hash;
	window.setInterval(async function () {
		if (window.location.hash != storedHash) {
			generate_viewport();
		}
	}, 100);
}
