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