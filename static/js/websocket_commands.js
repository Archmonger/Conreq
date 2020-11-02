let loc = window.location;
let ws_start = "";
if (loc.protocol == "https:") {
    ws_start = "wss://";
} else {
    ws_start = "ws://";
}
let endpoint = ws_start + loc.host;
let command_socket = new WebSocket(endpoint);

command_socket.onmessage = function(e) {
    console.log("socket message received", e);
    let command = JSON.parse(e.data);
    console.log("socket message JSON contents", command);
};
command_socket.onopen = function(e) {
    console.log("socket opened", e);
};
command_socket.onerror = function(e) {
    console.log("socket error", e);
};
command_socket.onclose = function(e) {
    console.log("socket closed", e);
};