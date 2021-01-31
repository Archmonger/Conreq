let modal_dialog = $("#modal-dialog");

// Fetches a modal via AJAX
var generate_modal = function (modal_url) {
  // Show the loading icon
  $("#modal-content").hide();
  $("#modal-container .loading-animation").show();

  // Fetch the series modal
  $.get(modal_url, function (modal_html) {
    // Place the new HTML on the page
    modal_dialog[0].innerHTML = DOMPurify.sanitize(modal_html);

    // Show the new content
    $("#modal-container .loading-animation").hide();

    // Add click events
    select_all_click_event();
    request_click_event();
    season_name_click_event();
    season_checkbox_click_event();
    episode_name_click_event();
    episode_checkbox_click_event();
    expand_click_event();
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

let request_click_event = function () {
  $(".modal-button.request-button").click(function () {
    let params = {
      tvdb_id: null,
      seasons: null,
      episode_ids: null,
    };
    let season_checkboxes = $(".season-checkbox");
    let season_checkboxes_not_specials = $(".season-checkbox:not(.specials)");
    let season_numbers = [];
    let episode_ids = [];

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
        episode_checkboxes.prop("checked", function (index, episode_checkmark) {
          if (episode_checkmark == true) {
            episode_ids.push($(this).data("episode-id"));
          }
        });
      }
    });

    // Request the whole show
    if (season_numbers.length == season_checkboxes_not_specials.length) {
      request_content(params);
      requested_toast_message();
      $("#modal-container").modal("hide");
      console.log("Requested the whole show!");
    }

    // Request parts of the show
    else if (season_numbers.length || episode_ids.length) {
      params.seasons = season_numbers;
      params.episode_ids = episode_ids;
      request_content(params);
      requested_toast_message();
      $("#modal-container").modal("hide");
      console.log("Seasons numbers requested:", season_numbers);
      console.log("Episode IDs requested:", episode_ids);
    }
    // User didn't select anything
    else {
      no_selection_toast_message();
    }
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
