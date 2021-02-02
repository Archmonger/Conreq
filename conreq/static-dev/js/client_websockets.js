let first_websocket_connection = true;
let display_disconnected_toast = true;
var viewport_loaded = false;

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
  let endpoint = ws_start + loc.host;
  COMMAND_SOCKET = new WebSocket(endpoint);

  // RECEIVABLE COMMANDS
  COMMAND_SOCKET.onmessage = function (response) {
    // Websocket message received, parse for JSON
    console.log(response);
    json_response = JSON.parse(response.data);

    // Check for valid commands
    if (json_response.command_name == "forbidden") {
      location.reload();
    } else if (json_response.command_name == "server settings") {
      if (json_response.success) {
        settings_save_success_toast_message();
      } else {
        settings_save_failed_toast_message(json_response.error_message);
      }
    } else if (json_response.command_name == "new conreq api key") {
      $("#conreq-api-key").text(json_response.value);
    } else {
      console.log(
        "Unknown command " + json_response.command_name + " received!"
      );
    }
  };

  // WEBSOCKET EVENT: ON OPEN
  COMMAND_SOCKET.onopen = function (response) {
    RETRY_COUNTER = 0;
    display_disconnected_toast = true;

    if (first_websocket_connection) {
      first_websocket_connection = false;
    } else {
      // Show a message saying we reconnected
      reconnected_toast_message();

      // Reload the viewport if the last page didn't load
      if (viewport_loaded == false) {
        console.log(
          "Viewport previously failed to load... Reloading the viewport!"
        );
        generate_viewport();
      }
    }
  };

  // WEBSOCKET EVENT: ON CLOSE
  COMMAND_SOCKET.onclose = function () {
    // Toast message to notify that the user has disconnected from the server
    if (display_disconnected_toast) {
      disconnected_toast_message();
      first_websocket_connection = false;
      display_disconnected_toast = false;
    }

    // Automatically reconnect upon disconnection
    RETRY_COUNTER++;
    if (RETRY_COUNTER <= MAX_FAST_RETRIES) {
      console.log(
        RETRY_COUNTER,
        "Websocket is closed. Reconnect will be attempted in 3 second."
      );
      setTimeout(function () {
        connect();
      }, 3000);
    } else {
      console.log(
        "Websocket is closed. Reconnect will be attempted in 30 second."
      );
      setTimeout(function () {
        connect();
      }, 30000);
    }
  };

  // WEBSOCKET EVENT: ON ERROR
  COMMAND_SOCKET.onerror = function (error) {
    if (display_disconnected_toast) {
      disconnected_toast_message();
      first_websocket_connection = false;
      display_disconnected_toast = false;
    }

    console.error(
      "Websocket encountered an error: ",
      error.message,
      "Closing socket..."
    );
    COMMAND_SOCKET.close();
  };
}

// First connection attempt
connect();

// SENDABLE COMMAND: CHANGE SERVER SETTING
var change_server_setting = function (setting_name = null, value = null) {
  let json_payload = {
    command_name: "server settings",
    parameters: {
      setting_name: setting_name,
      value: value,
    },
  };
  COMMAND_SOCKET.send(JSON.stringify(json_payload));
};
