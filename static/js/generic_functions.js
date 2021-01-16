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
var settings_save_failed_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: "Failed to save settings. Check logs for details.",
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
