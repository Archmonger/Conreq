// HELPER FUNCTIONS
let obtain_common_parameters = function(
    tmdb_id = null,
    tvdb_id = null,
    content_type = null
) {
    let url_params = new URLSearchParams(window.location.search);
    let results = { tmdb_id: null, tvdb_id: null, content_type: null };

    // Content Type
    if (content_type != null) {
        results.content_type = content_type;
    } else if (url_params.has("content_type")) {
        results.content_type = url_params.get("content_type");
    }
    // TMDB ID
    if (tmdb_id != null) {
        results.tmdb_id = tmdb_id;
    } else if (url_params.has("tmdb_id")) {
        results.tmdb_id = url_params.get("tmdb_id");
    }
    // TVDB ID
    if (tvdb_id != null) {
        results.tvdb_id = tvdb_id;
    } else if (url_params.has("tvdb_id")) {
        results.tvdb_id = url_params.get("tvdb_id");
    }

    // Return calculated parameters
    return results;
};

// Create masonry grid
var masonry_grid;

var refresh_viewport = function() {
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

// Make the function wait until the connection is made...
var waitForSocketConnection = function(socket, callback) {
    setTimeout(function() {
        if (socket.readyState === 1) {
            console.log("Websocket connection established");
            if (callback != null) {
                callback();
            }
        } else {
            waitForSocketConnection(socket, callback);
        }
    }, 5); // wait 5 milisecond for the connection...
};

// WEBSOCKET CREATION
var COMMAND_SOCKET = null;
let RETRY_COUNTER = 0;
let MAX_FAST_RETRIES = 30;

function connect() {
    // Note: this websocket automatically reconnects upon disconnection
    let loc = window.location;
    let ws_start = "";
    if (loc.protocol == "https:") {
        ws_start = "wss://";
    } else {
        ws_start = "ws://";
    }
    let endpoint = ws_start + loc.host + "/ws";
    COMMAND_SOCKET = new WebSocket(endpoint);

    // RECEIVABLE COMMANDS
    COMMAND_SOCKET.onmessage = function(response) {
        // Websocket message received, parse for JSON
        console.log(response);
        json_response = JSON.parse(response.data);

        // Check for valid commands
        if (json_response.command_name == "forbidden") {
            location.reload();
        } else if (json_response.command_name == "render page element") {
            // Determine what needs to be replaced
            let selected_element = $(json_response.selector);
            let parent_element = selected_element.parent();

            // Show the loading icon
            let loading_icon = parent_element.children(".loading-animation");
            if (loading_icon.length) {
                loading_icon.hide();
            }

            // Place the new HTML on the page
            selected_element[0].innerHTML = DOMPurify.sanitize(json_response.html);
            selected_element.show();

            refresh_viewport();
        }
    };

    // WEBSOCKET EVENT: ON OPEN
    COMMAND_SOCKET.onopen = function(response) {
        RETRY_COUNTER = 0;
        console.log(response);
    };

    // WEBSOCKET EVENT: ON CLOSE
    COMMAND_SOCKET.onclose = function() {
        // Automatically reconnect upon disconnection
        RETRY_COUNTER++;
        if (RETRY_COUNTER <= MAX_FAST_RETRIES) {
            console.log(
                RETRY_COUNTER,
                "Websocket is closed. Reconnect will be attempted in 3 second."
            );
            setTimeout(function() {
                connect();
            }, 3000);
        } else {
            console.log(
                "Websocket is closed. Reconnect will be attempted in 30 second."
            );
            setTimeout(function() {
                connect();
            }, 30000);
        }
    };

    // WEBSOCKET EVENT: ON ERROR
    COMMAND_SOCKET.onerror = function(error) {
        console.error(
            "Websocket encountered an error: ",
            error.message,
            "Closing socket..."
        );
        COMMAND_SOCKET.close();
    };
}

connect();

// SENDABLE COMMAND: REQUEST CONTENT
var request_content = function({
    tmdb_id = null,
    tvdb_id = null,
    content_type = null,
    seasons = null,
    episode_ids = null,
}) {
    let obtained_params = obtain_common_parameters(
        tmdb_id,
        tvdb_id,
        content_type
    );
    let json_payload = {
        command_name: "request",
        parameters: {
            tmdb_id: obtained_params.tmdb_id,
            tvdb_id: obtained_params.tvdb_id,
            content_type: obtained_params.content_type,
            seasons: seasons,
            episode_ids: episode_ids,
        },
    };
    COMMAND_SOCKET.send(JSON.stringify(json_payload));

    requested_toast_message();
};

// SENDABLE COMMAND: GENERATE EPISODE MODAL
var generate_episode_modal = function(tmdb_id = null, tvdb_id = null) {
    // Hide the old modal content
    $("#modal-content").hide();
    // Display the loading animation
    $("#modal-dialog .spinner-border").show();

    let obtained_params = obtain_common_parameters(tmdb_id, tvdb_id);
    let json_payload = {
        command_name: "generate modal",
        parameters: {
            modal_type: "episode selector",
            tmdb_id: obtained_params.tmdb_id,
            tvdb_id: obtained_params.tvdb_id,
        },
    };
    COMMAND_SOCKET.send(JSON.stringify(json_payload));
};

// SENDABLE COMMAND: GENERATE DISCOVER TAB
var generate_discover_tab = function(content_type = null) {
    // Hide the old modal content
    $(".viewport").hide();
    // Display the loading animation
    $(".viewport-container>.spinner-border").show();

    let obtained_params = obtain_common_parameters(null, null, content_type);
    let json_payload = {
        command_name: "generate discover tab",
        parameters: {
            content_type: obtained_params.content_type,
        },
    };
    COMMAND_SOCKET.send(JSON.stringify(json_payload));
};