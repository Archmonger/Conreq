var callback_error = function(element) {
    element.src = "/static/images/transparent.png";
};

var lazyloader = new LazyLoad({
    threshold: 0,
    callback_error: callback_error,
});

let viewport_selector = ".viewport-container";

element_ready(viewport_selector).then(function() {
    // Save scroll position of bottom node
    let previous_bottom_node = $(".viewport-posters > .masonry-item").last()[0];
    let scroll_node = null;

    // Lazy load page elements
    lazyloader.update();

    // Select the target node
    let target = document.querySelector(viewport_selector);

    // Create an observer instance
    let observer = new MutationObserver(function() {
        // Lazy load on page updates
        lazyloader.update();

        // Delete old masonry items
        let masonry_items = $(".viewport-posters > .masonry-item");
        if (masonry_items.length > 300) {
            // Delete half the elements, rounded down to the nearest row
            let card_width = $(".masonry-item").width() + 10;
            let viewport_width = $(".viewport").width();
            let cards_per_row = Math.trunc((viewport_width + 10) / card_width);
            scroll_node = previous_bottom_node;
            masonry_grid
                .masonry(
                    "remove",
                    masonry_items.slice(
                        0,
                        Math.floor(Math.floor(masonry_items.length / 2) / cards_per_row) * cards_per_row
                    )
                )
                .masonry("layout");

            // Scroll to the previous bottom node
            scroll_node.scrollIntoView(false);
            $(".viewport-container")[0].scrollBy(0, 30 + 10);
            console.log("Deleting excess masonry items!", scroll_node);
        }
        previous_bottom_node = masonry_items.last()[0];
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