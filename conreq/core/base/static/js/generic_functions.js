var http_request = $.ajax({});
let start_time, end_time;
var base_url = "";
var masonry_grid = null;
var infinite_scroller_created = false;
var previous_admin_settings = new Map();

// Asychronous sleeping
var sleep = function (ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
};

// Returns the window location with the base url added
var add_base_url = function (window_location = null) {
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

// Gets the current window location from the hash
var get_window_location = function (raw = false) {
	// Read the URL hash to determine what page we are on
	let window_location = window.location.hash.split(/#(.+)/)[1];
	if (
		raw == false &&
		window_location &&
		window_location.startsWith("/display/")
	) {
		// Remove display from the non-raw url.
		// It's only used to signify something is to be added to the secondary viewport.
		window_location = window_location.slice("/display".length);
	}
	if (window_location) {
		return window_location;
	}
	return "";
};

// Gets the current window location from the hash without parameters
var get_window_location_no_params = function () {
	let window_location = get_window_location();
	// Read the URL hash to determine what page we are on
	if (window_location.includes("?")) {
		return window_location.split(/\?(.+)/)[0];
	}
	return window_location;
};

// Gets the current window location from the hash
var get_window_params = function () {
	// Read the URL hash to determine what page we are on
	let window_hash = window.location.hash;

	if (window_hash.includes("?")) {
		return window.location.hash.split(/\?(.+)/)[1];
	}
	return "";
};

// Successful copy event
let copy_to_clipboard_success = async function () {
	invite_copied_toast_message();
	$(".invite_link").remove();
};

// Legacy: Copies the text of an element to the clipboard
let copy_to_clipboard_fallback = async function () {
	let invite_link_element = document.getElementById("invite_link");
	invite_link_element.select();
	document.execCommand("copy")
		? copy_to_clipboard_success()
		: conreq_no_response_toast_message();
};

// Copies the text of an element to the clipboard
var copy_to_clipboard = async function () {
	let max_retries = 10;

	// Wait for the element to exist
	for (let try_num = 0; try_num <= max_retries; try_num++) {
		if (document.getElementById("invite_link") != null) {
			break;
		} else if (try_num >= max_retries) {
			// The element failed to load in time, notify the user.
			conreq_no_response_toast_message();
			return;
		}
		await sleep(250);
	}
	let invite_link_element = document.getElementById("invite_link");

	// Copy to clipboard using the Navigator API
	if (typeof navigator.clipboard != "undefined") {
		window.navigator.clipboard
			.writeText(invite_link_element.textContent)
			.then(copy_to_clipboard_success, copy_to_clipboard_fallback);
	}

	// Fallback to legacy copy to clipboard method
	else {
		copy_to_clipboard_fallback();
	}
};

// Creates a page element that copy_to_clipboard can copy from
var create_invite_link_elem = function (invite_link) {
	const el = document.createElement("textarea");
	el.value = invite_link;
	el.textContent = invite_link;
	el.readOnly = true;
	el.style.position = "absolute";
	el.style.left = "-99999px";
	el.id = "invite_link";
	el.className = "invite_link";
	document.body.appendChild(el);
};

// Post to a URL
var post_url = function (url, callback) {
	http_request.abort();
	http_request = $.ajax({
		type: "POST",
		url: url,
		headers: {
			"X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
				.value,
		},
		success: callback,
	});
	return http_request;
};

// Post JSON to a URL
var post_json = function (url, data, callback) {
	http_request.abort();
	http_request = $.ajax({
		type: "POST",
		url: url,
		headers: {
			"X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
				.value,
		},
		data: JSON.stringify(data),
		contentType: "application/json; charset=utf-8",
		success: callback,
	});
	return http_request;
};

// Gets a URL
var get_url = function (location, success = function () {}) {
	http_request.abort();
	http_request = $.get(location, function (response = null) {
		return success(response);
	});
	return http_request;
};

// Post a form to a URL
var post_modal_form = function (callback) {
	let modal_form = $(".modal-body form");
	if (modal_form.length) {
		let url = modal_form.attr("action");
		http_request.abort();
		http_request = $.ajax({
			type: "POST",
			url: url,
			headers: {
				"X-CSRFToken": document.getElementsByName(
					"csrfmiddlewaretoken"
				)[0].value,
			},
			data: modal_form.serialize(),
			success: callback,
		});
		return http_request;
	}
	console.warn("Attempted to submit modal form that doesn't exist!");
	return false;
};

// Determine what seasons/episodes were selected
var modal_checkbox_aggregator = function () {
	let params = {
		seasons: [],
		episodes: [],
		episode_ids: [],
	};

	let season_checkboxes = $(".checkbox");
	let season_checkboxes_not_specials = $(".checkbox:not(.specials)");
	let season_checkboxes_not_specials_checked = $(
		".checkbox:not(.specials):checked"
	);

	let seasons = [];
	let episodes = [];
	let episode_ids = [];
	// Iterate through every season checkbox
	season_checkboxes.prop("checked", function (index, season_checkmark) {
		// Whole season was requested
		if (season_checkmark == true) {
			seasons.push($(this).data("season-number"));
		}
		// Individual episode was requested
		else if (season_checkmark == false) {
			let episode_container = $($(this).data("all-suboptions-container"));
			let episode_checkboxes = episode_container.find("input");
			episode_checkboxes.prop(
				"checked",
				function (index, episode_checkmark) {
					if (episode_checkmark == true) {
						episodes.push($(this).data("episode"));
						episode_ids.push($(this).data("episode-id"));
					}
				}
			);
		}
	});

	// Request the whole show
	if (
		season_checkboxes_not_specials_checked.length ==
		season_checkboxes_not_specials.length
	) {
		return true;
	}

	// Request parts of the show
	else if (seasons.length || episode_ids.length || episodes.length) {
		params.seasons = seasons;
		params.episodes = episodes;
		params.episode_ids = episode_ids;
		return params;
	}

	// Request nothing
	else {
		return params;
	}
};

// Change a server setting
var change_server_setting = function (setting_name = null, value = null) {
	let json_payload = {
		setting_name: setting_name,
		value: value,
	};
	post_json(
		$(".viewport.server.settings").data("url"),
		json_payload,
		function (json_response) {
			if (json_response.command_name == "new conreq api key") {
				$("#conreq-api-key").text(json_response.value);
			}
			if (json_response.success) {
				generate_viewport(false);
				save_success_toast_message();
			} else {
				error_toast_message(json_response.error_message);
			}
		}
	).fail(async function () {
		error_toast_message("Internal server error.");
	});
};

// Performs a content search
let perform_search = async function (searchbar) {
	let searchbar_input = $(searchbar);
	let parameters = searchbar_input.val();
	let content_type = searchbar_input.data("content-type");
	let new_location =
		searchbar_input.data("search-url") + "?query=" + escape(parameters);
	if (content_type) {
		new_location += "&content_type=" + content_type;
	}
	window.location = new_location;
};

// Removes old posters from the infinite scroller to save memory
var cull_old_posters = async function () {
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
				.addClass("culled")
				.text("Hidden to save memory.");

			// Output to console that posters have been deleted
			console.info(
				"Hiding the content of " +
					num_of_posters_to_delete +
					" posters because a new page has loaded."
			);
		}
	}
};

// Hide any floaty objects
var hide_modals_and_popups = async function () {
	$("#modal-container").modal("hide");
	$.magnificPopup.close();
	if (window.matchMedia("(max-width: 800px)").matches) {
		if (!$("#sidebar").hasClass("collapsed")) {
			$("#sidebar").addClass("collapsed");
		}
	}
};

$.fn.replaceWithPush = function (a) {
	let $a = $(DOMPurify.sanitize(a));

	this.replaceWith($a);
	return $a;
};
