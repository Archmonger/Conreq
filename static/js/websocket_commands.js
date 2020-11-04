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

let obtain_url_parameters = function() {
    let url_params = new URLSearchParams(window.location.search);
    let results = { tmdb_id: null, tvdb_id: null, content_type: null };

    // Content Type
    if (url_params.has("content_type")) {
        results.content_type = url_params.get("content_type");
    }
    // TMDB ID
    if (url_params.has("tmdb_id")) {
        results.tmdb_id = url_params.get("tmdb_id");
    }
    // TVDB ID
    if (url_params.has("tvdb_id")) {
        results.tvdb_id = url_params.get("tvdb_id");
    }

    // Could not determine ID parameters
    if (results.tmdb_id == null && results.tvdb_id == null) {
        return null;
    }
    // URL parameters were determined
    else {
        return results;
    }
};

// AVAILABLE COMMANDS

/* REQUEST COMMAND STRUCTURE */
// {   command_name: "",
//     parameters: {   tmdb_id: "",
//                     tvdb_id: "",
//                     content_type: "",
//                     seasons: [],
//                     episode_ids: [],
//                 }
// }
var request_command = function(
    tmdb_id = null,
    tvdb_id = null,
    content_type = null,
    seasons = null,
    episode_ids = null
) {
    // Request the server to download some content
    let json_payload = {
        command_name: "request",
        parameters: {
            tmdb_id: tmdb_id,
            tvdb_id: tvdb_id,
            content_type: content_type,
            seasons: seasons,
            episode_ids: episode_ids,
        },
    };

    // ID was passed in to the function call
    if (tmdb_id != null || tvdb_id != null) {
        json_payload.parameters.tmdb_id = tmdb_id;
        json_payload.parameters.tvdb_id = tvdb_id;
        COMMAND_SOCKET.send(JSON.stringify(json_payload));
    }

    // Attempt to obtain ID from the URL
    else {
        let url_params = obtain_url_parameters();
        json_payload.parameters.tmdb_id = url_params.tmdb_id;
        json_payload.parameters.content_type = url_params.content_type;
        json_payload.parameters.tvdb_id = url_params.tvdb_id;
        COMMAND_SOCKET.send(JSON.stringify(json_payload));
    }
};

/* EPISODE MODAL COMMAND STRUCTURE */
// {   command_name: "",
//     parameters: {   tmdb_id: "",
//                     tvdb_id: "",
//                     content_type: "",
//                 }
// }
var episode_modal_command = function(
    tmdb_id = null,
    tvdb_id = null,
    content_type = null
) {
    // Request the server to generate an episode modal
    let json_payload = {
        command_name: "episode modal",
        parameters: {
            tmdb_id: tmdb_id,
            tvdb_id: tvdb_id,
            content_type: content_type,
        },
    };

    // ID was passed in to the function call
    if (tmdb_id != null || tvdb_id != null) {
        json_payload.parameters.tmdb_id = tmdb_id;
        json_payload.parameters.tvdb_id = tvdb_id;
        COMMAND_SOCKET.send(JSON.stringify(json_payload));
    }

    // Attempt to obtain ID from the URL
    else {
        let url_params = obtain_url_parameters();
        json_payload.parameters.tmdb_id = url_params.tmdb_id;
        json_payload.parameters.content_type = url_params.content_type;
        json_payload.parameters.tvdb_id = url_params.tvdb_id;
        COMMAND_SOCKET.send(JSON.stringify(json_payload));
    }
};