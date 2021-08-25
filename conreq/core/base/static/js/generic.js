var http_request = $.ajax({});
let start_time, end_time;
var base_url = "";

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

// TODO: Remove this
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

// TODO: Remove this
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

// TODO: Remove this
// Gets a URL
var get_url = function (location, success = function () {}) {
	http_request.abort();
	http_request = $.get(location, function (response = null) {
		return success(response);
	});
	return http_request;
};

// Hide any floaty objects
var hide_popups = async function () {
	$("#modal-container").modal("hide");
	if (window.matchMedia("(max-width: 800px)").matches) {
		if (!$("#sidebar").hasClass("collapsed")) {
			$("#sidebar").addClass("collapsed");
		}
	}
};

$.fn.replaceWithPush = function (a) {
	let $a = $(a);

	this.replaceWith($a);
	return $a;
};
