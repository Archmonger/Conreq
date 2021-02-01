let modal_dialog = $("#modal-dialog");

// Fetches a modal via AJAX
var generate_modal = function (modal_url) {
  // Show the loading icon
  $("#modal-content").hide();
  $("#modal-container .loading-animation").show();

  // Fetch the series modal
  http_request = $.get(modal_url, function (modal_html) {
    // Place the new HTML on the page
    modal_dialog[0].innerHTML = DOMPurify.sanitize(modal_html);

    // Show the new content
    $("#modal-container .loading-animation").hide();

    // Add click events
    select_all_click_event();
    request_click_event();
    series_modal_click_event();
    season_name_click_event();
    season_checkbox_click_event();
    episode_name_click_event();
    episode_checkbox_click_event();
    expand_click_event();
  }).fail(function () {
    // Server could'get fetch the modal!
    $("#modal-container").modal("hide");
    conreq_no_response_toast_message();
  });
};

// CLICK EVENTS
let select_all_click_event = function () {
  $(".modal-button.select-button").click(function () {
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
      let season_checkboxes = $(".season-checkbox");
      let season_checkboxes_not_specials = $(".season-checkbox:not(.specials)");
      let season_numbers = [];
      let episode_ids = [];

      // Request a movie
      if (params.content_type == "movie") {
        // request_content(params);
        post_json($(this).data("request-url"), params, function () {
          requested_toast_message();
          $("#modal-container").modal("hide");
          $(".request-button").remove();
        }).fail(function () {
          conreq_no_response_toast_message();
        });
      }
      // Request a TV show
      else if (params.content_type == "tv") {
        // Iterate through every season checkbox
        season_checkboxes.prop("checked", function (index, season_checkmark) {
          // Whole season was requested
          if (season_checkmark == true) {
            season_numbers.push($(this).data("season-number"));
          }
          // Individual episode was requested
          else if (season_checkmark == false) {
            let episode_container = $($(this).data("episode-container"));
            let episode_checkboxes = episode_container.find("input");
            episode_checkboxes.prop(
              "checked",
              function (index, episode_checkmark) {
                if (episode_checkmark == true) {
                  episode_ids.push($(this).data("episode-id"));
                }
              }
            );
          }
        });

        // Request the whole show
        if (season_numbers.length == season_checkboxes_not_specials.length) {
          post_json($(this).data("request-url"), params, function () {
            requested_toast_message();
            $("#modal-container").modal("hide");
          }).fail(function () {
            conreq_no_response_toast_message();
          });
        }

        // Request parts of the show
        else if (season_numbers.length || episode_ids.length) {
          params.seasons = season_numbers;
          params.episode_ids = episode_ids;
          post_json($(this).data("request-url"), params, function () {
            requested_toast_message();
            $("#modal-container").modal("hide");
          }).fail(function () {
            conreq_no_response_toast_message();
          });
        }
        // User didn't select anything
        else {
          no_selection_toast_message();
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
      $("#modal-container").modal("show");
      generate_modal($(this).data("modal-url") + "?" + $.param(params));
    });
  });
};

let season_name_click_event = function () {
  $(".season").click(function () {
    // Checkmark the season
    let season_block = $(this.parentElement.parentElement);
    let season_checkbox = season_block.find("input");
    season_checkbox.prop("checked", !season_checkbox.prop("checked"));

    // Checkmark all related episodes
    let episode_container = $(season_checkbox.data("episode-container"));
    let episode_checkboxes = episode_container.find("input");
    episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
  });
};

let season_checkbox_click_event = function () {
  $(".season-checkbox").click(function () {
    // Checkmark all related episodes
    let season_checkbox = $(this);
    let episode_container = $(season_checkbox.data("episode-container"));
    let episode_checkboxes = episode_container.find("input");
    episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
  });
};

let episode_name_click_event = function () {
  $(".episode").click(function () {
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

let episode_checkbox_click_event = function () {
  $(".episode-checkbox").click(function () {
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

let expand_click_event = function () {
  $("#modal-container .fa-expand").click(function () {
    $("#modal-container").modal("hide");
  });
};
