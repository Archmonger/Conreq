var callback_error = function(element) {
    element.src = "/static/images/transparent.png";
};

var lazyloader = new LazyLoad({
    threshold: 0,
    callback_error: callback_error,
});

let viewport_selector = ".viewport-container";

element_ready(viewport_selector).then(function() {
    // Select the target node
    let target = document.querySelector(viewport_selector);

    // Create an observer instance
    let observer = new MutationObserver(function() {
        lazyloader.update();
        console.log("New viewport observed! Setting up lazy loads...");
    });

    // Configuration of the observer
    let config = {
        attributes: false,
        characterData: false,
        subtree: true,
        childList: true,
    };

    // Begin observing the modal
    observer.observe(target, config);
});