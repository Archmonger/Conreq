// Requested toast message
var requested_toast_message = function () {
  iziToast.show({
    icon: "fas fa-check-circle",
    title: "Requested!",
    message: "Server is searching for a download...",
    displayMode: "replace",
    titleColor: "var(--accent-color)",
    messageColor: "var(--accent-color)",
    iconColor: "var(--accent-color)",
    progressBarColor: "var(--accent-color)",
  });
};

// No selection toast message
var no_selection_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Rejected!",
    message: "No items selected.",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// No selection toast message
var login_failed_toast_message = function () {
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
var disconnected_toast_message = function () {
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
var reconnected_toast_message = function () {
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
var settings_save_failed_toast_message = function (error_message) {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: error_message,
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Saving settings succeeded
var settings_save_success_toast_message = function () {
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
var passwords_dont_match_toast_message = function () {
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
var conreq_submission_failed_toast_message = function () {
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
var invite_copied_toast_message = function () {
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
var copy_to_clipboard = function (str) {
  const el = document.createElement("textarea");
  el.value = str;
  el.setAttribute("readonly", "");
  el.style.position = "absolute";
  el.style.left = "-99999px";
  document.body.appendChild(el);
  el.select();
  document.execCommand("copy");
  document.body.removeChild(el);
};

// Request Content
var request_content = function ({
  tmdb_id = null,
  tvdb_id = null,
  content_type = null,
  seasons = null,
  episode_ids = null,
}) {
  let obtained_params = obtain_common_parameters(
    tmdb_id,
    tvdb_id,
    content_type
  );
  let json_payload = {
    tmdb_id: obtained_params.tmdb_id,
    tvdb_id: obtained_params.tvdb_id,
    content_type: obtained_params.content_type,
    seasons: seasons,
    episode_ids: episode_ids,
  };

  $.ajax({
    type: "POST",
    url: $(".request-button").data("request-url"),
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    data: JSON.stringify(json_payload),
    contentType: "application/json; charset=utf-8",
    dataType: "application/json; charset=UTF-8",
  });
};

// Post to a URL
var post_url = function (url, callback) {
  $.ajax({
    type: "POST",
    url: url,
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    success: callback,
  });
};

// Post JSON to a URL
var post_json = function (url, data, callback) {
  $.ajax({
    type: "POST",
    url: url,
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "application/json; charset=UTF-8",
    success: callback,
  });
};
