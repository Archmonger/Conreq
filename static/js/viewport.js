// Initialize a global masonry grid
var masonry_grid = null;
var infinite_scroller_created = false;

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

// Adds all click events required
let add_click_events = function() {
    $(".request-button.tv").click(function() {
        generate_episode_modal();
    });
    $(".request-button.movie").click(function() {
        request_content({});
    });
};

// Destroys old viewport JS instances
let destroy_viewport = function() {
    if (masonry_grid != null) {
        if (infinite_scroller_created) {
            masonry_grid.infiniteScroll("destroy");
            infinite_scroller_created = false;
        }
        masonry_grid.masonry("destroy");
        masonry_grid = null;
    }
    if (review_carousel != null) {
        review_carousel.destroy();
        review_carousel = null;
    }
    if (videos_carousel != null) {
        videos_carousel.destroy();
        videos_carousel = null;
    }
    if (recommended_carousel != null) {
        recommended_carousel.destroy();
        recommended_carousel = null;
    }
    if (images_carousel != null) {
        images_carousel.destroy();
        images_carousel = null;
    }
    if (collection_carousel != null) {
        collection_carousel.destroy();
        collection_carousel = null;
    }
    if (cast_carousel != null) {
        cast_carousel.destroy();
        cast_carousel = null;
    }
};

// Preforms any actions needed to prepare the viewport
let refresh_viewport = function() {
    // Destroy old JS elements
    destroy_viewport();

    // Create any carousels that need to be made
    create_all_carousels();

    // Create the masonry grid
    masonry_grid = $(".viewport-posters").masonry({
        itemSelector: ".masonry-item",
        gutter: 10,
        horizontalOrder: true,
        fitWidth: true,
        transitionDuration: "0s",
        stagger: "0s",
        isStill: true,
    });

    // Determine what path to fetch infinite scrolling content on
    let url_params = new URLSearchParams(window.location.search);
    let discover_path = window.location.hash.split("#/")[1];
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
            outlayer: masonry_grid.data("masonry"),
            prefill: true,
            elementScroll: ".viewport-loader",
            history: false,
            scrollThreshold: 2000,
        });

        masonry_grid.on("append.infiniteScroll", function() {
            cull_old_posters();
        });

        infinite_scroller_created = true;
    }

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
    $(".viewport-loader>*").fadeOut();
    $(".viewport-container>.spinner-border").show();

    // Fetch the new content, display it, and hide the loading animation
    $.get(window_location, function(viewport_html) {
        $(".viewport-loader")[0].innerHTML = DOMPurify.sanitize(viewport_html);
        refresh_viewport();
        $(".viewport-container>.spinner-border").hide();
        $(".viewport-loader>*").fadeIn();

        // Add any click events needed
        add_click_events();
    });
};

// Obtain the initial page
generate_viewport();

// Fetch a new page when the URL changes
if ("onhashchange" in window) {
    // Window anchor change event supported?
    window.onhashchange = function() {
        generate_viewport();
    };
} else {
    // Window anchor change event not supported
    var storedHash = window.location.hash;
    window.setInterval(function() {
        if (window.location.hash != storedHash) {
            generate_viewport();
        }
    }, 100);
}