// Create masonry grid
var masonry_grid = $(".viewport-posters").masonry({
    itemSelector: ".masonry-item",
    gutter: 10,
    horizontalOrder: true,
    fitWidth: true,
    transitionDuration: "0s",
    stagger: "0s",
});

// get Masonry instance
let masonry_instance = masonry_grid.data("masonry");

// Determine what path to fetch infinite scrolling content on
let url_params = new URLSearchParams(window.location.search);
let discover_path = "/";
if (url_params.has("content_type")) {
    discover_path +=
        "?content_type=" + url_params.get("content_type") + "&page={{#}}";
} else {
    discover_path += "?page={{#}}";
}

// Configure infinite scrolling
masonry_grid.infiniteScroll({
    path: discover_path,
    append: ".masonry-item",
    outlayer: masonry_instance,
    prefill: true,
    elementScroll: ".viewport-container",
    history: false,
    scrollThreshold: 2000,
});

$(".viewport-posters").css("opacity", "1");