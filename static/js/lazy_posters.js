var callback_error = function(element) {
    element.src = "/static/images/transparent.png";
};

var lazyloader = new LazyLoad({
    threshold: 0,
    callback_error: callback_error,
});

let viewport_selector = ".viewport-container";

element_ready(viewport_selector).then(function() {
    // Lazy load page elements
    lazyloader.update();

    // Select the target node
    let target = document.querySelector(viewport_selector);

    // Create an observer instance
    let observer = new MutationObserver(function() {
        // Lazy load on page updates
        lazyloader.update();

        // Delete old masonry items
        // let masonry_items = $(".viewport-posters > .masonry-item");
        // if (masonry_items.length > 650) {
        // setTimeout(function() {
        //     $(".viewport-container").scrollTop(0);
        // }, 500);
        // masonry_grid
        //     .masonry("remove", masonry_items.slice(0, 625))
        //     .masonry("layout");
        // console.log("Deleting excess masonry items!");
        // }
        console.log("Viewport changes observed!");
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