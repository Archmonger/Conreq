function connect() {
    // Create the command socket
    let loc = window.location;
    let ws_start = "";
    if (loc.protocol == "https:") {
        ws_start = "wss://";
    } else {
        ws_start = "ws://";
    }
    let endpoint = ws_start + loc.host;
    let command_socket = new WebSocket(endpoint);

    // Socket events
    command_socket.onopen = function(e) {
        console.log("socket opened", e);
    };

    command_socket.onmessage = function(e) {
        console.log("socket message received", e);
        let command = JSON.parse(e.data);
        console.log("socket message JSON contents", command);
    };

    command_socket.onclose = function(e) {
        console.log(
            "Socket is closed. Reconnect will be attempted in 3 second.",
            e.reason
        );
        setTimeout(function() {
            connect();
        }, 3000);
    };

    command_socket.onerror = function(err) {
        console.error("Socket encountered error: ", err.message, "Closing socket");
        command_socket.close();
    };
}

connect();