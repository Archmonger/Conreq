let loc = window.location;
let ws_start = "";
if (loc.protocol == "https:") {
    ws_start = "wss://";
} else {
    ws_start = "ws://";
}
let endpoint = ws_start + loc.host;
let socket = new WebSocket(endpoint);

socket.onmessage = function(e) {
    console.log("message", e);
};
socket.onopen = function(e) {
    console.log("open", e);
};
socket.onerror = function(e) {
    console.log("error", e);
};
socket.onclose = function(e) {
    console.log("close", e);
};