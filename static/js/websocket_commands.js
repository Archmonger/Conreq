// CREATE WEBSOCKET
let COMMAND_SOCKET = null;
let RETRY_COUNTER = 0;
let MAX_FAST_RETRIES = 30;

function connect() {
    // This websocket automatically reconnects upon disconnection
    let loc = window.location;
    let ws_start = "";
    if (loc.protocol == "https:") {
        ws_start = "wss://";
    } else {
        ws_start = "ws://";
    }
    let endpoint = ws_start + loc.host;
    COMMAND_SOCKET = new WebSocket(endpoint);

    // Socket events
    COMMAND_SOCKET.onopen = function(e) {
        RETRY_COUNTER = 0;
        console.log("Websocket opened.", e);
    };

    COMMAND_SOCKET.onmessage = function(e) {
        console.log("Websocket message received.", e);
    };

    COMMAND_SOCKET.onclose = function(e) {
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

    COMMAND_SOCKET.onerror = function(err) {
        console.error(
            "Websocket encountered an error: ",
            err.message,
            "Closing socket..."
        );
        COMMAND_SOCKET.close();
    };
}

connect();

// AVAILABLE COMMANDS

// Command to request
var request_command = function(
    tmdb_id = null,
    tvdb_id = null,
    content_type = null
) {
    // {command_name:"", parameters: {tmdb_id="", tvdb_id=""} }
    let json_payload = {
        command_name: "request",
        parameters: {
            tmdb_id: tmdb_id,
            tvdb_id: tvdb_id,
            content_type: content_type,
        },
    };

    // A parameter was passed in to the function call
    if (tmdb_id != null || tvdb_id != null) {
        json_payload.parameters.tmdb_id = tmdb_id;
        json_payload.parameters.tvdb_id = tvdb_id;
        COMMAND_SOCKET.send(JSON.stringify(json_payload));
    }

    // Attempt to obtain ID from the URL
    else {
        let url_params = new URLSearchParams(window.location.search);

        // Movies
        if (
            url_params.has("content_type") &&
            url_params.get("content_type") == "movie"
        ) {
            json_payload.parameters.content_type = url_params.get("content_type");
            // TMDB ID was obtained
            if (url_params.has("tmdb_id")) {
                json_payload.parameters.tmdb_id = url_params.get("tmdb_id");
                COMMAND_SOCKET.send(JSON.stringify(json_payload));
            }
        }

        // TV Shows
        else if (
            url_params.has("content_type") &&
            url_params.get("content_type") == "tv"
        ) {
            json_payload.parameters.content_type = url_params.get("content_type");
            // TVDB ID was obtained
            if (url_params.has("tvdb_id")) {
                json_payload.parameters.tvdb_id = url_params.get("tvdb_id");
                COMMAND_SOCKET.send(JSON.stringify(json_payload));
            }

            // TMDB ID was obtained
            else if (url_params.has("tmdb_id")) {
                json_payload.parameters.tmdb_id = url_params.get("tmdb_id");
                COMMAND_SOCKET.send(JSON.stringify(json_payload));
            }
        }

        // Could not determine parameters
        else {
            console.log("Request command did not receive an ID!");
        }
    }
};