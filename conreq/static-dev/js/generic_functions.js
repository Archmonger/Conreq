var http_request = $.ajax({});
let start_time, end_time;

// Requested toast message
var requested_toast_message = function () {
  iziToast.show({
    icon: "fas fa-check-circle",
    title: "Requested!",
    message: "Server is searching for a download.",
    displayMode: "replace",
    titleColor: "var(--accent-color)",
    messageColor: "var(--accent-color)",
    iconColor: "var(--accent-color)",
    progressBarColor: "var(--accent-color)",
  });
};

// Reported toast message
var reported_toast_message = function () {
  iziToast.show({
    icon: "fas fa-check-circle",
    title: "Reported!",
    message: "Server is looking for a solution.",
    displayMode: "replace",
    titleColor: "var(--accent-color)",
    messageColor: "var(--accent-color)",
    iconColor: "var(--accent-color)",
    progressBarColor: "var(--accent-color)",
  });
};

// No selection toast message
var no_selection_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Rejected!",
    message: "Nothing was selected.",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// No selection toast message
var login_failed_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: "Invalid login credentials.",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Server disconnected toast message
var disconnected_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Disconnected!",
    message: "Trying to reconnect...",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Server reconnected toast message
var reconnected_toast_message = function () {
  iziToast.show({
    icon: "fas fa-check-circle",
    title: "Reconnected!",
    displayMode: "replace",
    titleColor: "var(--accent-color)",
    messageColor: "var(--accent-color)",
    iconColor: "var(--accent-color)",
    progressBarColor: "var(--accent-color)",
  });
};

// Saving settings failed
var settings_save_failed_toast_message = function (error_message) {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: error_message,
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Saving settings succeeded
var settings_save_success_toast_message = function () {
  iziToast.show({
    icon: "fas fa-check-circle",
    title: "Saved!",
    displayMode: "replace",
    titleColor: "var(--accent-color)",
    messageColor: "var(--accent-color)",
    iconColor: "var(--accent-color)",
    progressBarColor: "var(--accent-color)",
  });
};

// Password confirm failed
var passwords_dont_match_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: "Passwords don't match!",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Failed to perform conreq first time setup
var conreq_submission_failed_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: "One or more issues detected with submission!",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Invite link has been copied to cliboard
var invite_copied_toast_message = function () {
  iziToast.show({
    icon: "fas fa-check-circle",
    title: "Valid for 7 days.",
    message: "Invite link has been copied to clipboard! ",
    displayMode: "replace",
    titleColor: "var(--accent-color)",
    messageColor: "var(--accent-color)",
    iconColor: "var(--accent-color)",
    progressBarColor: "var(--accent-color)",
  });
};

// Failed to fetch something
var conreq_no_response_toast_message = function () {
  iziToast.show({
    icon: "fas fa-exclamation-triangle",
    title: "Error!",
    message: "The server failed to process this request!",
    displayMode: "replace",
    titleColor: "#9a5c0f",
    messageColor: "#9a5c0f",
    iconColor: "#c57615",
    progressBarColor: "var(--accent-color)",
  });
};

// Gets the current window location from the hash
var get_window_location = function () {
  // Read the URL hash to determine what page we are on
  return window.location.hash.split(/#(.+)/)[1];
};

// Gets the current window location from the hash
var get_window_parameters = function () {
  // Read the URL hash to determine what page we are on
  let window_hash = window.location.hash;

  if (window_hash.includes("?")) {
    return window.location.hash.split(/\?(.+)/)[1];
  }
  return "";
};

// Copies the text of an element to the clipboard
var copy_to_clipboard = async function () {
  let max_retries = 15;
  for (let try_num = 0; try_num <= max_retries; try_num++) {
    if (document.getElementById("invite_link") != null) {
      break;
    } else if (try_num >= max_retries) {
      conreq_no_response_toast_message();
      return;
    }
    await sleep(100);
  }

  var invite_link_element = document.getElementById("invite_link");
  if (typeof invite_link_element === "undefined") {
    conreq_no_response_toast_message();
    return;
  }

  if (invite_link_element.textContent.includes("undefined")) {
    document.body.removeChild(invite_link_element);
    conreq_no_response_toast_message();
    return;
  }

  if (typeof navigator.clipboard != "undefined") {
    //New ClipBoard API is supported
    window.navigator.clipboard.writeText(invite_link_element.textContent).then(
      function () {
        invite_copied_toast_message();
      },
      function () {
        conreq_no_response_toast_message();
      }
    );
  } else {
    //Fallback to old clipboard method
    invite_link_element.select();
    document.execCommand("copy")
      ? invite_copied_toast_message()
      : conreq_no_response_toast_message();
  }
  document.body.removeChild(invite_link_element);
};

var hide_invite_link = function (...result) {
  var sign_up_url = result[1];
  let invite_link =
    sign_up_url + "?invite_code=" + encodeURI(result[0].invite_code);
  if (invite_link.includes("undefined")) {
    conreq_no_response_toast_message();
    return;
  }
  const el = document.createElement("textarea");
  el.value = invite_link;
  el.textContent = invite_link;
  el.readOnly = true;
  el.style.position = "absolute";
  el.style.left = "-99999px";
  el.id = "invite_link";
  document.body.appendChild(el);
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Post to a URL
var post_url = function (url, callback) {
  http_request.abort();
  http_request = $.ajax({
    type: "POST",
    url: url,
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    success: callback,
  });
  return http_request;
};

// Post JSON to a URL
var post_json = function (url, data, callback) {
  http_request.abort();
  http_request = $.ajax({
    type: "POST",
    url: url,
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    success: callback,
  });
  return http_request;
};

// Gets a URL
var get_url = async function (location, success = function () {}, ...args) {
  http_request.abort();
  http_request = $.get(location, function (response = null) {
    return success(response, args);
  });
  return http_request;
};

// Gets a URL and retries if it fails
let get_url_retries = 0;
var get_viewport = function (location, success = function () {}) {
  http_request.abort();
  http_request = $.get(location, function (response = null) {
    get_url_retries = 0;
    return success(response);
  }).fail(function () {
    get_url_retries++;
    if (get_url_retries <= 5 && this.url == get_window_location()) {
      setTimeout(function () {
        get_viewport(location, success);
      }, 200 * (get_url_retries * 5));
    } else {
      conreq_no_response_toast_message();
    }
  });
  return http_request;
};

// Determine what seasons/episodes were selected
var modal_checkbox_aggregator = function () {
  let params = {
    seasons: [],
    episodes: [],
    episode_ids: [],
  };

  let season_checkboxes = $(".checkbox");
  let season_checkboxes_not_specials = $(".checkbox:not(.specials)");
  let season_checkboxes_not_specials_checked = $(
    ".checkbox:not(.specials):checked"
  );

  let seasons = [];
  let episodes = [];
  let episode_ids = [];
  // Iterate through every season checkbox
  season_checkboxes.prop("checked", function (index, season_checkmark) {
    // Whole season was requested
    if (season_checkmark == true) {
      seasons.push($(this).data("season-number"));
    }
    // Individual episode was requested
    else if (season_checkmark == false) {
      let episode_container = $($(this).data("all-suboptions-container"));
      let episode_checkboxes = episode_container.find("input");
      episode_checkboxes.prop("checked", function (index, episode_checkmark) {
        if (episode_checkmark == true) {
          episodes.push($(this).data("episode"));
          episode_ids.push($(this).data("episode-id"));
        }
      });
    }
  });

  // Request the whole show
  if (
    season_checkboxes_not_specials_checked.length ==
    season_checkboxes_not_specials.length
  ) {
    return true;
  }

  // Request parts of the show
  else if (seasons.length || episode_ids.length || episodes.length) {
    params.seasons = seasons;
    params.episodes = episodes;
    params.episode_ids = episode_ids;
    return params;
  }

  // Request nothing
  else {
    return params;
  }
};

// Timer used for rate limiting the infinite scroller
var timer_start = function () {
  start_time = new Date();
};
timer_start();

// Calculates seconds elapsed from timer_start()
var timer_seconds = function () {
  end_time = new Date();
  let time_diff = end_time - start_time; // in ms
  // strip the ms
  time_diff /= 1000;

  // get seconds
  return Math.round(time_diff);
};

// Change a server setting
var change_server_setting = function (setting_name = null, value = null) {
  let json_payload = {
    setting_name: setting_name,
    value: value,
  };
  post_json(
    $(".viewport.server.settings").data("url"),
    json_payload,
    function (json_response) {
      if (json_response.command_name == "new conreq api key") {
        $("#conreq-api-key").text(json_response.value);
      }
      if (json_response.success) {
        settings_save_success_toast_message();
      } else {
        settings_save_failed_toast_message(json_response.error_message);
      }
    }
  ).fail(function () {
    settings_save_failed_toast_message("Internal server error.");
  });
};
