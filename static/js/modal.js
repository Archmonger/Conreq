// Select the target node
let target = document.querySelector("#modal-content");

// Create an observer instance
let observer = new MutationObserver(function() {
    select_all_click_event();
    season_name_click_event();
    episode_name_click_event();
    console.log("mutation observed");
});

// Configuration of the observer
let config = {
    attributes: false,
    characterData: false,
    subtree: false,
    childList: true,
};

// Begin observing the modal
observer.observe(target, config);

// CLICK EVENTS

let select_all_click_event = function() {
    $(".modal-button.select-button").click(function() {
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

let season_name_click_event = function() {
    $(".season").click(function() {
        // Checkmark the season
        let season_block = $(this.parentElement.parentElement);
        let season_checkbox = season_block.find("input");
        season_checkbox.prop("checked", !season_checkbox.prop("checked"));

        // Checkmark all related episodes
        let episode_container = $(season_block.data("episode-container"));
        let episode_checkboxes = episode_container.find("input");
        episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
    });
};

let episode_name_click_event = function() {
    $(".episode").click(function() {
        // Checkmark the individual episode
        let episode_block = $(this.parentElement);
        let episode_checkbox = episode_block.find("input");
        episode_checkbox.prop("checked", !episode_checkbox.prop("checked"));

        // Uncheck the season box
        let season_container = $(episode_block.data("season-container"));
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