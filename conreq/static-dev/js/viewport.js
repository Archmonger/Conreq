let masonry_grid = null;
let infinite_scroller_created = false;
let previous_admin_settings = new Map();
let viewport_container_class = ".viewport-container";
let viewport_class = ".viewport";
let page_reload_needed = false;

// Create the lazyloader
let callback_error = function (element) {
	element.src = "/static/images/transparent.png";
};
var lazyloader = new LazyLoad({
	threshold: 0,
	callback_error: callback_error,
});

// Removes old posters from the infinite scroller to save memory
let cull_old_posters = function () {
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
let update_active_tab = function () {
	$(".nav-tab").each(function () {
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

// Adds viewport related event listeners
let add_event_listeners = function () {
	// More Info page events
	request_btn_click_event();
	create_content_modal_click_event();
	create_report_modal_click_event();
	issue_approve_btn_click_event();
	issue_delete_btn_click_event();

	// Server Settings menu events
	$(
		'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
	).each(function () {
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
	).focusout(function () {
		let setting_name = $(this).data("setting-name");
		let current_value = $(this).val();
		if (previous_admin_settings[setting_name] != current_value) {
			change_server_setting(setting_name, current_value);
			previous_admin_settings[setting_name] = current_value;
		}
	});
	$(".toggler .settings-item.admin").change(function () {
		let setting_name = $(this).data("setting-name");
		let current_value = $(this).children("input").is(":checked");
		change_server_setting(setting_name, current_value);
	});
	$(".text-input-container.dropdown .dropdown-item").click(function () {
		let setting_name = $(this).parent().data("setting-name");
		let dropdown_id = $(this).data("id");
		change_server_setting(setting_name, dropdown_id);
		let new_text = $(this).text();
		$(this).parent().parent().find(".settings-item-text").text(new_text);
	});
	$(".refresh-conreq-api").click(function () {
		let setting_name = $(this).data("setting-name");
		change_server_setting(setting_name);
	});
	$(".reload-needed").click(function () {
		page_reload_needed = true;
	});

	// User Management events
	$(".action-btn.delete").click(function () {
		let btn = $(this);
		let delete_query =
			btn.data("delete-url") +
			"?username=" +
			encodeURI(btn.data("username"));
		post_url(delete_query, function (result) {
			if (result.success) {
				btn.parent().parent().remove();
			}
		}).fail(function () {
			conreq_no_response_toast_message();
		});
	});
	$(".standard-btn.invite-user").click(function () {
		let btn = $(this);
		let generate_invite_url = btn.data("generate-invite-url");
		let sign_up_url = window.location.origin + btn.data("sign-up-url");
		get_url(generate_invite_url, function (result) {
			let invite_link =
				sign_up_url + "?invite_code=" + encodeURI(result.invite_code);
			create_invite_link_elem(invite_link);
		}).fail(conreq_no_response_toast_message);
		copy_to_clipboard();
	});
};

// Destroys old viewport JS instances
let destroy_viewport = function () {
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
let refresh_viewport = function () {
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
		setTimeout(function () {
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

			masonry_grid.on("append.infiniteScroll", function () {
				cull_old_posters();
				create_content_modal_click_event();
				timer_start();
			});

			// Only load new page if X seconds have elapsed (rate limit)
			masonry_grid.on("scrollThreshold.infiniteScroll", function () {
				if (timer_seconds() >= 1) {
					masonry_grid.infiniteScroll("loadNextPage");
				}
			});

			infinite_scroller_created = true;
		}, 500);
	}

	// Lazy load page elements
	lazyloader.update();
};

// Gets the viewport from a URL
let get_viewport = function (location, success = function () {}) {
	http_request = get_url(location, function (response = null) {
		return success(response);
	}).fail(function () {
		if (http_request.statusText != "abort") {
			conreq_no_response_toast_message();
			$(".viewport-container>*").hide();
			$(".viewport>*").hide();
			$(".viewport")
				.css("text-align", "center")
				.css("height", "auto")
				.text("Could not connect to the server!");
			$(".viewport").show();
		}
	});
	return http_request;
};

// Fetch the new viewport and update the current tab
var generate_viewport = function (reset_scroll_pos = true) {
	// Check if the whole webpage needs to be reloaded
	if (page_reload_needed) {
		location.reload();
	}

	// Read the URL hash to determine what page we are on
	let window_location = get_window_location();

	// If there is no hash, add one
	if (window_location == "" || window_location == null) {
		if (window.history.replaceState) {
			// Replace the current page in the browser history to add a hash
			window.history.replaceState({}, null, $(".nav-tab a").attr("href"));
			window_location = window.location.hash.split("#")[1];
		}
	}

	// Change the current tab
	update_active_tab();

	// Save the previous scroll position, if needed
	let previous_scroll_pos = $(viewport_container_class).scrollTop();

	// Asynchronously fetch new viewport content
	viewport_loaded = false;
	get_viewport(window_location, function (viewport_html) {
		// Save that the page was successfully loaded
		viewport_loaded = true;

		// Destroy old JS elements and event handlers
		destroy_viewport();

		// Inject and configure the new content
		$(".viewport-container")[0].innerHTML = DOMPurify.sanitize(
			viewport_html
		);
		refresh_viewport();
		add_event_listeners();

		// Display the new content
		$(".viewport-container>.loading-animation-container").hide();
		$(".viewport-container>*:not(.loading-animation-container)").show();

		// Set scroll position
		if (reset_scroll_pos) {
			$(viewport_container_class).scrollTop(0);
		} else {
			$(viewport_container_class).scrollTop(previous_scroll_pos);
		}
	});

	// If the page is taking too long to load, show a loading animation
	setTimeout(function () {
		if (!viewport_loaded) {
			// Hide the viewport and display the loading animation
			$(".viewport-container>.loading-animation-container").show();
			$(".viewport-container>*:not(.loading-animation-container)").hide();
		}
	}, 1000);
};

// Perform actions whenever the HTML on the page changes
let page_mutation_observer = function () {
	let observer = new MutationObserver(function () {
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

// Obtain the initial page
page_mutation_observer();
generate_viewport();

// Fetch a new page when the URL changes
if ("onhashchange" in window) {
	// Window anchor change event supported?
	window.onhashchange = function () {
		generate_viewport();
	};
} else {
	// Window anchor change event not supported
	var storedHash = window.location.hash;
	window.setInterval(function () {
		if (window.location.hash != storedHash) {
			generate_viewport();
		}
	}, 100);
}
