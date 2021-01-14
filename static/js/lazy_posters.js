let viewport_container_class = ".viewport-container";
let viewport_scroller_class = ".viewport-loader";
let viewport_class = ".viewport";

// Create the lazyloader
let callback_error = function (element) {
  element.src = "/static/images/transparent.png";
};
var lazyloader = new LazyLoad({
  threshold: 0,
  callback_error: callback_error,
});

// Lazy load new elements every time the viewport changes
element_ready(viewport_class).then(function () {
  // Create an observer instance
  let observer = new MutationObserver(function () {
    // Update Lazyload
    lazyloader.update();
  });

  // Configuration of the observer
  let config = {
    attributes: false,
    characterData: false,
    subtree: true,
    childList: true,
  };

  // Select the target node
  let target = document.querySelector(viewport_scroller_class);

  // Begin observing the modal
  observer.observe(target, config);
});

// Removes old posters from the infinite scroller
// FIXME: Known bug where if user scrolls while scrollTop is being executed,
// the user is returned to the previous scroll position (absolute in px)
var cull_old_posters = function () {
  let viewport_container = $(viewport_container_class);
  let viewport_scroller = $(viewport_scroller_class);
  let viewport = $(viewport_class);
  if (document.querySelector(".viewport-posters")) {
    // Logic to delete excess masonry items
    let masonry_items = $(".viewport-posters > .masonry-item");

    // Calculate the current state of the viewport
    let current_scroll_pos = viewport_scroller.scrollTop();
    let card_width = $(".masonry-item").width() + 10;
    let card_height = $(".masonry-item").height() + 10;
    let viewport_width = viewport.width();
    let viewport_container_height = viewport_container.height();
    let cards_per_row = (viewport_width + 10) / card_width;
    let deletable_num_of_rows = Math.max(
      0,
      Math.floor((current_scroll_pos - viewport_container_height) / card_height)
    );
    let num_of_posters_to_delete = deletable_num_of_rows * cards_per_row;
    let deletable_content_height = deletable_num_of_rows * card_height;

    console.log(
      "Deleting " +
        num_of_posters_to_delete +
        " posters because a new page has loaded."
    );

    // If there are posters to delete, do it.
    if (num_of_posters_to_delete > 0) {
      // Make sure we have the latest scroll position
      current_scroll_pos = viewport_scroller.scrollTop();

      // Delete the old elements
      masonry_grid
        .masonry("remove", masonry_items.slice(0, num_of_posters_to_delete))
        .masonry("layout");

      // Scroll to the previous position
      viewport_scroller.scrollTop(
        current_scroll_pos - deletable_content_height
      );
    }
  }
};
