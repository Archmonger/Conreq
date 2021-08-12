var viewport_container_top_class = ".viewport-container-top";
var viewport_container_class = ".viewport-container";
let viewport_class = ".viewport";
let page_reload_needed = false;
let viewport_http_request = $.ajax({});
let viewport_http_request_aborted = false;

// Create the lazyloader
var lazyloader = new LazyLoad({
	threshold: 0,
	callback_error: async function (element) {
		element.src = "/static/images/transparent.png";
	},
});

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
let update_page_title = async function (viewport_selector) {
	let page_name = DOMPurify.sanitize(
		$(viewport_selector + ">.page-name").val()
	);
	let app_name = $("#app-name").val();
	if (page_name) {
		document.title = page_name + " | " + app_name;
		$(".navbar-brand").text(page_name);
	} else {
		document.title = app_name;
		$(".navbar-brand").text(app_name);
	}
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
	let new_viewport = "main[data-url='" + get_window_location() + "']";
	let old_viewport = $(
		"main:not([data-url='" + get_window_location() + "'])"
	);
	$(new_viewport).trigger("prepare-cached");
	update_active_tab();
	update_page_title(new_viewport);
	old_viewport.attr("hidden", "");
	$(new_viewport).removeAttr("hidden");
	$(new_viewport).trigger("loaded-cached");
};

// Destroys old viewport JS instances
let destroy_viewport = async function (viewport_selector) {
	$(viewport_selector).trigger("destroy");
	$(viewport_selector + ">*:not(.loading-animation-container)").remove();
};

// Preforms any actions needed to prepare the viewport
let prepare_viewport = async function (viewport_selector) {
	$(viewport_selector).trigger("prepare");
	$(viewport_selector).attr("data-url", get_window_location());

	// Lazy load page elements
	lazyloader.update();
};

// Gets the viewport from a URL
let get_viewport = async function (
	location,
	viewport_selector,
	success = function () {}
) {
	$(viewport_selector).trigger("url-changed");

	// Abandon an old http request if the user clicks something else
	if (
		viewport_http_request.statusText != "OK" ||
		viewport_http_request.statusText == null
	) {
		viewport_http_request_aborted = true;
		viewport_http_request.abort();
	}

	// Load the viewport html
	viewport_http_request = $.get(location, function (response = null) {
		return success(response);
	}).fail(async function () {
		if (!viewport_http_request_aborted) {
			console.error("Failed to fetch viewport!");
			conreq_no_response_toast_message();
			await destroy_viewport(viewport_selector);
			$(viewport_selector + ">*").remove();
			$(viewport_selector).append(
				"<h1>Could not connect to the server!</h1>"
			);
			$(viewport_selector + ">h1").css("text-align", "center");
			select_active_viewport(viewport_selector);
		}
		viewport_http_request_aborted = false;
	});
	return http_request;
};

// Fetch the new viewport and update the current tab
var generate_viewport = async function (standard_viewport_load = true) {
	hide_modals_and_popups();

	if (cached_viewport_exists() && standard_viewport_load == true) {
		display_cached_viewport();
	} else {
		let viewport_selector = null;
		if (get_window_location(true).startsWith("/display/")) {
			// Display on the top layer
			viewport_selector = viewport_container_top_class;
		} else {
			// Display on the primary viewport
			viewport_selector = viewport_container_class;
		}
		// Check if the whole webpage needs to be reloaded
		if (page_reload_needed && standard_viewport_load) {
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
				$(viewport_selector)[0].innerHTML =
					DOMPurify.sanitize(viewport_html);
				select_active_viewport(viewport_selector);
				await prepare_viewport(viewport_selector);
				update_page_title(viewport_selector);
				$(viewport_selector).trigger("loaded");

				// Display the new content
				$(viewport_selector + ">.loading-animation-container").hide();
				$(
					viewport_selector + ">*:not(.loading-animation-container)"
				).show();

				// Set scroll position
				if (standard_viewport_load) {
					$(viewport_selector).scrollTop(0);
				}
			}
		);

		// If the page is taking too long to load, show a loading animation
		setTimeout(async function () {
			if (!viewport_loaded && standard_viewport_load) {
				// Hide the viewport and display the loading animation
				select_active_viewport(viewport_selector);
				$(viewport_selector + ">.loading-animation-container").show();
				$(
					viewport_selector + ">*:not(.loading-animation-container)"
				).hide();
			}
		}, 500);
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

$(document).ready(async function () {
	base_url = $("#base-url").val() + "/";
	// Slide in animations for navbar, sidebar, and viewport
	AOS.init();
	// Obtain the initial page
	page_mutation_observer();
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
	let stored_hash = window.location.hash;
	window.setInterval(async function () {
		if (window.location.hash != stored_hash) {
			generate_viewport();
		}
	}, 100);
}
