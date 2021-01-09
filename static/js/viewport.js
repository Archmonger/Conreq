// Initialize a global masonry grid
var masonry_grid;

// Updates the current tab based on the URL
let update_active_tab = function() {
    $(".nav-tab").each(function() {
        nav_tab = $(this);
        // Set the active tab
        if (
            nav_tab.attr("href") == window.location.hash &&
            !nav_tab.hasClass("active")
        ) {
            nav_tab.addClass("active");
        }
        // Remove any old active tabs
        else if (nav_tab.hasClass("active")) {
            nav_tab.removeClass("active");
        }
    });
};

// Preforms any actions needed to prepare the viewport
let refresh_viewport = function() {
    masonry_grid = $(".viewport-posters").masonry({
        itemSelector: ".masonry-item",
        gutter: 10,
        horizontalOrder: true,
        fitWidth: true,
        transitionDuration: "0s",
        stagger: "0s",
        isStill: true,
    });
    // get Masonry instance
    let masonry_instance = masonry_grid.data("masonry");

    // Determine what path to fetch infinite scrolling content on
    let url_params = new URLSearchParams(window.location.search);
    let discover_path = "discover/";
    if (url_params.has("content_type")) {
        discover_path +=
            "?content_type=" + url_params.get("content_type") + "&page={{#}}";
    } else {
        discover_path += "?page={{#}}";
    }

    // Configure infinite scrolling
    if ($(".infinite-scroll").length) {
        masonry_grid.infiniteScroll({
            path: discover_path,
            append: ".masonry-item",
            outlayer: masonry_instance,
            prefill: true,
            elementScroll: ".viewport-loader",
            history: false,
            scrollThreshold: 2000,
        });
    }

    $(".viewport-posters").css("opacity", "1");

    // Lazy load page elements
    lazyloader.update();
};

// Obtains the viewport content based on the URL, then updates the current tab
let generate_viewport = function() {
    // Read the URL hash to determine what page we are on
    let window_location = window.location.hash.split("#")[1];

    // If there is no hash, add one
    if (window_location == "" || window_location == null) {
        if (window.history.replaceState) {
            //prevents browser from storing history with each change:
            window.history.replaceState({}, null, "#/discover/");
            window_location = window.location.hash.split("#")[1];
        }
    }

    // Change the current tab
    update_active_tab();

    // Hide the old content and display the loading animation
    $(".viewport").hide();
    $(".viewport-container>.spinner-border").show();

    // Fetch the new content, display it, and hide the loading animation
    $.get(window_location, function(viewport_html) {
        $(".viewport-loader")[0].innerHTML = DOMPurify.sanitize(viewport_html);
        refresh_viewport();
        $(".viewport-container>.spinner-border").hide();
        $(".viewport").show();
    });
};

waitForSocketConnection(COMMAND_SOCKET, generate_viewport);

if ("onhashchange" in window) {
    // Window anchor change event supported?
    window.onhashchange = function() {
        waitForSocketConnection(COMMAND_SOCKET, generate_viewport);
    };
} else {
    // Window anchor change event not supported
    var storedHash = window.location.hash;
    window.setInterval(function() {
        if (window.location.hash != storedHash) {
            waitForSocketConnection(COMMAND_SOCKET, generate_viewport);
        }
    }, 100);
}