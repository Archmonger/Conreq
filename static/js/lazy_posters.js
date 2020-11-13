var callback_error = function(element) {
    element.src = "/static/images/transparent.png";
};

var lazyloader = new LazyLoad({
    threshold: 0,
    callback_error: callback_error,
});

let viewport_container_class = ".viewport-container";

element_ready(viewport_container_class).then(function() {
    // Lazy load page elements
    lazyloader.update();

    // Select the target node
    let target = document.querySelector(".viewport");

    // Create an observer instance
    let observer = new MutationObserver(function() {
        // Lazy load and masonry on poster viewport page updates
        lazyloader.update();

        if (document.querySelector(".viewport-posters")) {
            // Delete old masonry items
            let masonry_items = $(".viewport-posters > .masonry-item");
            if (masonry_items.length > 300) {
                console.log("Culling excess masonry items from the viewport");
                // Save the previous scroll position
                let before_removal_height = $(".viewport").height();
                let before_removal_scroll_pos = $(viewport_container_class).scrollTop();

                // Delete half the elements, rounded down to the nearest row
                let card_width = $(".masonry-item").width() + 10;
                let viewport_width = $(".viewport").width();
                let cards_per_row = Math.trunc((viewport_width + 10) / card_width);
                masonry_grid
                    .masonry(
                        "remove",
                        masonry_items.slice(
                            0,
                            Math.floor(Math.floor(masonry_items.length / 2) / cards_per_row) *
                            cards_per_row
                        )
                    )
                    .masonry("layout");
                // Scroll to the previous position
                let after_removal_height = $(".viewport").height();
                let viewport_height_difference =
                    before_removal_height - after_removal_height;
                document
                    .querySelector(".viewport-container")
                    .scrollTo(0, before_removal_scroll_pos - viewport_height_difference);
            }
            console.log("Updating poster viewport");
        }
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