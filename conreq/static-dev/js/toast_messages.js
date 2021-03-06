// Requested toast message
var requested_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-check-circle",
		title: "Requested!",
		message: "Server is searching for a download.",
		displayMode: "replace",
		titleColor: "var(--accent-color)",
		messageColor: "var(--accent-color)",
		iconColor: "var(--accent-color)",
		progressBarColor: "var(--accent-color)",
	});
};

// Reported toast message
var reported_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-check-circle",
		title: "Reported!",
		message: "Server is looking for a solution.",
		displayMode: "replace",
		titleColor: "var(--accent-color)",
		messageColor: "var(--accent-color)",
		iconColor: "var(--accent-color)",
		progressBarColor: "var(--accent-color)",
	});
};

// No selection toast message
var no_selection_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Rejected!",
		message: "Nothing was selected.",
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
	});
};

// Login failed toast message
var login_failed_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Error!",
		message: "Invalid login credentials.",
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
	});
};

// Server disconnected toast message
var disconnected_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Disconnected!",
		message: "Trying to reconnect...",
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
	});
};

// Server reconnected toast message
var reconnected_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-check-circle",
		title: "Reconnected!",
		displayMode: "replace",
		titleColor: "var(--accent-color)",
		messageColor: "var(--accent-color)",
		iconColor: "var(--accent-color)",
		progressBarColor: "var(--accent-color)",
	});
};

// Saving settings failed
var settings_save_failed_toast_message = async function (error_message) {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Error!",
		message: error_message,
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
		timeout: 15000,
	});
};

// Saving settings succeeded
var settings_save_success_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-check-circle",
		title: "Saved!",
		displayMode: "replace",
		titleColor: "var(--accent-color)",
		messageColor: "var(--accent-color)",
		iconColor: "var(--accent-color)",
		progressBarColor: "var(--accent-color)",
	});
};

// Password confirm failed
var passwords_dont_match_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Error!",
		message: "Passwords don't match!",
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
	});
};

// Failed to perform conreq first time setup
var conreq_submission_failed_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Error!",
		message: "One or more issues detected with submission!",
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
	});
};

// Invite link has been copied to cliboard
var invite_copied_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-check-circle",
		title: "Valid for 7 days.",
		message: "Invite link has been copied to clipboard! ",
		displayMode: "replace",
		titleColor: "var(--accent-color)",
		messageColor: "var(--accent-color)",
		iconColor: "var(--accent-color)",
		progressBarColor: "var(--accent-color)",
	});
};

// Failed to fetch something
var conreq_no_response_toast_message = async function () {
	iziToast.show({
		icon: "fas fa-exclamation-triangle",
		title: "Error!",
		message: "The server did not respond!",
		displayMode: "replace",
		titleColor: "#9a5c0f",
		messageColor: "#9a5c0f",
		iconColor: "#c57615",
		progressBarColor: "var(--accent-color)",
		timeout: 15000,
	});
};
