// Wait for a selector to become available on the DOM
var element_ready = function(selector) {
    return new Promise((resolve, reject) => {
        let el = document.querySelector(selector);
        if (el) {
            resolve(el);
        }
        new MutationObserver((mutationRecords, observer) => {
            // Query for elements matching the specified selector
            Array.from(document.querySelectorAll(selector)).forEach((element) => {
                resolve(element);
                // Once we have resolved we don't need the observer anymore.
                observer.disconnect();
            });
        }).observe(document.documentElement, {
            childList: true,
            subtree: true,
        });
    });
};

// Requested toast message
var requested_toast_message = function() {
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
var no_selection_toast_message = function() {
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
var login_failed_toast_message = function() {
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