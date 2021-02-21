let http_request = $.ajax({});
let start_time, end_time;

// Asychronous sleeping
function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

// Gets the current window location from the hash
var get_window_location = function () {
	// Read the URL hash to determine what page we are on
	return window.location.hash.split(/#(.+)/)[1];
};

// Gets the current window location from the hash
var get_window_parameters = function () {
	// Read the URL hash to determine what page we are on
	let window_hash = window.location.hash;

	if (window_hash.includes("?")) {
		return window.location.hash.split(/\?(.+)/)[1];
	}
	return "";
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
		await sleep(100);
	}
	let invite_link_element = document.getElementById("invite_link");

	// Copy to clipboard using the Navigator API
	if (typeof navigator.clipboard != "undefined") {
		window.navigator.clipboard
			.writeText(invite_link_element.textContent)
			.then(
				invite_copied_toast_message,
				conreq_no_response_toast_message
			);
	}

	// Fallback to legacy copy to clipboard method
	else {
		invite_link_element.select();
		document.execCommand("copy")
			? invite_copied_toast_message()
			: conreq_no_response_toast_message();
	}

	// Remove page element created by create_invite_link_elem()
	document.body.removeChild(invite_link_element);
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

// Timer used for rate limiting the infinite scroller
var timer_start = function () {
	start_time = new Date();
};
timer_start();

// Calculates seconds elapsed from timer_start()
var timer_seconds = function () {
	end_time = new Date();
	let time_diff = end_time - start_time; // in ms
	// strip the ms
	time_diff /= 1000;

	// get seconds
	return Math.round(time_diff);
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
				settings_save_success_toast_message();
			} else {
				settings_save_failed_toast_message(json_response.error_message);
			}
		}
	).fail(function () {
		settings_save_failed_toast_message("Internal server error.");
	});
};
