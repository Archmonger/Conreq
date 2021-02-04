let modal_dialog = $("#modal-dialog");
let modal_loaded = false;
let ongoing_request = null;

// Fetches a modal via AJAX
var generate_modal = function (modal_url) {
  // Fetch the series modal
  modal_loaded = false;
  http_request = $.get(modal_url, function (modal_html) {
    // Save that the modal was successfully loaded
    modal_loaded = true;

    // Place the new HTML on the page
    modal_dialog[0].innerHTML = DOMPurify.sanitize(modal_html);

    // Show the new content
    $("#modal-container .loading-animation").hide();
    $("#modal-content").show();
    $("#modal-container").modal("show");

    // Add click events
    request_click_event();
    series_modal_click_event();
    modal_select_all_click_event();
    modal_expand_click_event();
    row_title_click_event();
    row_checkbox_click_event();
    row_suboption_title_click_event();
    row_suboption_checkbox_click_event();
    report_modal_click_event();
  }).fail(function () {
    // Server couldn't fetch the modal
    conreq_no_response_toast_message();
    $("#modal-container").modal("hide");
  });

  // If the modal is taking too long to load, show a loading animation
  setTimeout(function () {
    if (!modal_loaded) {
      // Show the loading icon
      $("#modal-content").hide();
      $("#modal-container").modal("show");
      $("#modal-container .loading-animation").show();
    }
  }, 300);
};

// CLICK EVENTS
var request_click_event = function () {
  $(".request-button").each(function () {
    $(this).unbind("click");
    $(this).click(function () {
      let params = {
        tmdb_id: $(this).data("tmdb-id"),
        tvdb_id: $(this).data("tvdb-id"),
        content_type: $(this).data("content-type"),
        seasons: null,
        episode_ids: null,
      };

      // Prevent the user from spamming the request button
      if (ongoing_request == this) {
        return false;
      } else {
        ongoing_request = this;
      }

      // Request a movie
      if (params.content_type == "movie") {
        // request_content(params);
        post_json($(this).data("request-url"), params, function () {
          requested_toast_message();
          $(".request-button").text("REQUESTED");
          $("#modal-container").modal("hide");
          ongoing_request = null;
        }).fail(function () {
          conreq_no_response_toast_message();
          ongoing_request = null;
        });
      }

      // Request a TV show
      else if (params.content_type == "tv") {
        let selection = modal_checkbox_aggregator();
        // Request the whole show
        if (selection == true) {
          post_json($(this).data("request-url"), params, function () {
            requested_toast_message();
            $(".series-modal-button").text("REQUESTED");
            $("#modal-container").modal("hide");
            ongoing_request = null;
          }).fail(function () {
            conreq_no_response_toast_message();
            ongoing_request = null;
          });
        }

        // Request parts of the show
        else if (selection.seasons.length || selection.episode_ids.length) {
          params.seasons = selection.seasons;
          params.episode_ids = selection.episode_ids;
          post_json($(this).data("request-url"), params, function () {
            requested_toast_message();
            $(".series-modal-button").text("REQUESTED");
            $("#modal-container").modal("hide");
            ongoing_request = null;
          }).fail(function () {
            conreq_no_response_toast_message();
            ongoing_request = null;
          });
        }
        // User didn't select anything
        else {
          no_selection_toast_message();
          ongoing_request = null;
        }
      }
    });
  });
};

var series_modal_click_event = function () {
  $(".series-modal-button").each(function () {
    $(this).unbind("click");
    $(this).click(function () {
      let params = {
        tmdb_id: $(this).data("tmdb-id"),
        tvdb_id: $(this).data("tvdb-id"),
        content_type: $(this).data("content-type"),
      };
      generate_modal($(this).data("modal-url") + "?" + $.param(params));
    });
  });
};

var content_preview_modal_click_event = function () {
  $(".content-preview-modal-button").each(function () {
    $(this).unbind("click");
    $(this).click(function () {
      let params = {
        tmdb_id: $(this).data("tmdb-id"),
        tvdb_id: $(this).data("tvdb-id"),
        content_type: $(this).data("content-type"),
      };
      generate_modal($(this).data("modal-url") + "?" + $.param(params));
    });
  });
};

var report_selection_modal_click_event = function () {
  $(".report-selection-modal-button").each(function () {
    $(this).unbind("click");
    $(this).click(function () {
      let params = {
        tmdb_id: $(this).data("tmdb-id"),
        tvdb_id: $(this).data("tvdb-id"),
        content_type: $(this).data("content-type"),
        report_modal: true,
      };
      generate_modal($(this).data("modal-url") + "?" + $.param(params));
    });
  });
};

var report_modal_click_event = function () {
  $(".report-modal-button").each(function () {
    $(this).unbind("click");
    $(this).click(function () {
      let params = {
        tmdb_id: $(this).data("tmdb-id"),
        tvdb_id: $(this).data("tvdb-id"),
        content_type: $(this).data("content-type"),
      };
      generate_modal($(this).data("modal-url") + "?" + $.param(params));
    });
  });
};

let modal_select_all_click_event = function () {
  $(".modal .select-all-button").click(function () {
    let modal_text = this.innerHTML;
    if (modal_text == "SELECT ALL") {
      this.innerHTML = "UNSELECT ALL";
      $(".modal input:not(.specials)").prop("checked", true);
    } else {
      this.innerHTML = "SELECT ALL";
      $(".modal input:not(.specials)").prop("checked", false);
    }
  });
};

let row_title_click_event = function () {
  $(".modal .row-title-container").click(function () {
    // Checkmark the season
    let season_block = $(this.parentElement);
    let season_checkbox = season_block.find("input");
    season_checkbox.prop("checked", !season_checkbox.prop("checked"));

    // Checkmark all related episodes
    let episode_container = $(season_checkbox.data("all-suboptions-container"));
    let episode_checkboxes = episode_container.find("input");
    episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
  });
};

let row_checkbox_click_event = function () {
  $(".modal .checkbox").click(function () {
    // Checkmark all related episodes
    let season_checkbox = $(this);
    let episode_container = $(season_checkbox.data("all-suboptions-container"));
    let episode_checkboxes = episode_container.find("input");
    episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
  });
};

let row_suboption_title_click_event = function () {
  $(".modal .suboption-title-container").click(function () {
    // Checkmark the individual episode
    let episode_block = $(this.parentElement);
    let episode_checkbox = episode_block.find("input");
    episode_checkbox.prop("checked", !episode_checkbox.prop("checked"));

    // Uncheck the season box
    let season_container = $(episode_checkbox.data("season-container"));
    let season_checkbox = season_container.find("input");
    if (episode_checkbox.prop("checked") == false) {
      season_checkbox.prop("checked", false);
    }

    // Checkmark the season box if every episode is checked
    else {
      let all_episodes_container = $(this.parentElement.parentElement);
      let episode_checkboxes = all_episodes_container.find("input");
      let checkmarked_episode_checkboxes = episode_checkboxes.filter(
        "input:checked"
      );
      if (episode_checkboxes.length == checkmarked_episode_checkboxes.length) {
        season_checkbox.prop("checked", true);
      }
    }
  });
};

let row_suboption_checkbox_click_event = function () {
  $(".modal .suboption-checkbox").click(function () {
    // Uncheck the season box
    let episode_checkbox = $(this);
    let season_container = $(episode_checkbox.data("season-container"));
    let season_checkbox = season_container.find("input");
    if (episode_checkbox.prop("checked") == false) {
      season_checkbox.prop("checked", false);
    }

    // Checkmark the season box if every episode is checked
    else {
      let all_episodes_container = $(
        this.parentElement.parentElement.parentElement.parentElement
      );
      console.log(all_episodes_container);
      let episode_checkboxes = all_episodes_container.find("input");
      let checkmarked_episode_checkboxes = episode_checkboxes.filter(
        "input:checked"
      );
      if (episode_checkboxes.length == checkmarked_episode_checkboxes.length) {
        season_checkbox.prop("checked", true);
      }
    }
  });
};

let modal_expand_click_event = function () {
  $(".modal .fa-expand").click(function () {
    $("#modal-container").modal("hide");
  });
};
