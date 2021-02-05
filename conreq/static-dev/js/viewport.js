let masonry_grid = null;
let infinite_scroller_created = false;
let previous_admin_settings = new Map();
let viewport_container_class = ".viewport-container";
let viewport_class = ".viewport";
let reload_needed = false;

// Create the lazyloader
let callback_error = function (element) {
  element.src = "/static/images/transparent.png";
};
var lazyloader = new LazyLoad({
  threshold: 0,
  callback_error: callback_error,
});

// Removes old posters from the infinite scroller
let cull_old_posters = function () {
  let viewport_container = $(viewport_container_class);
  let viewport = $(viewport_class);
  if (document.querySelector(".viewport-masonry")) {
    // Logic to delete excess masonry items
    let masonry_items = $(".viewport-masonry > .masonry-item");

    // Calculate the current state of the viewport
    let scroll_position = viewport_container.scrollTop();
    let card_width = $(".masonry-item").width() + 10;
    let card_height = $(".masonry-item").height() + 10;
    let viewport_width = viewport.width();
    let viewport_container_height = viewport_container.height();
    let cards_per_row = (viewport_width + 10) / card_width;
    let deletable_num_of_rows = Math.max(
      0,
      Math.floor(
        (scroll_position - viewport_container_height * 3) / card_height
      )
    );
    let num_of_posters_to_delete = deletable_num_of_rows * cards_per_row;
    let before_deletion_height = viewport.height();

    // If there are posters to delete, do it.
    if (num_of_posters_to_delete > 0 && masonry_grid != null) {
      // Make sure we have the latest scroll position
      scroll_position = viewport_container.scrollTop();

      // Delete the old elements
      masonry_grid
        .masonry("remove", masonry_items.slice(0, num_of_posters_to_delete))
        .masonry("layout");

      // Scroll to the previous position
      viewport_container.scrollTop(
        scroll_position - (before_deletion_height - viewport.height())
      );

      // Output to console that posters have been deleted
      console.log(
        "Deleting " +
          num_of_posters_to_delete +
          " posters because a new page has loaded."
      );
    }
  }
};

// Updates the current tab based on the URL
let update_active_tab = function () {
  $(".nav-tab").each(function () {
    nav_tab = $(this);
    // Set the active tab
    if (
      nav_tab.attr("href") == window.location.hash &&
      !nav_tab.hasClass("active")
    ) {
      nav_tab.addClass("active");
    }
    // Remove any old active tabs
    else if (nav_tab.hasClass("active")) {
      nav_tab.removeClass("active");
    }
  });
};

// Adds viewport related event listeners
let add_event_listeners = function () {
  // More Info page events
  request_click_event();
  series_modal_click_event();
  report_modal_click_event();
  report_selection_modal_click_event();
  content_preview_modal_click_event();

  // Server Settings menu events
  $(
    'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
  ).each(function () {
    let setting_name = $(this).data("setting-name");
    let current_value = $(this).val();
    previous_admin_settings[setting_name] = current_value;
  });
  $(
    'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
  ).on("keypress", function (e) {
    let setting_name = $(this).data("setting-name");
    let current_value = $(this).val();
    if (e.which == 13) {
      change_server_setting(setting_name, current_value);
      previous_admin_settings[setting_name] = current_value;
    }
  });
  $(
    'input[type="text"].settings-item.admin, input[type="url"].settings-item.admin'
  ).focusout(function () {
    let setting_name = $(this).data("setting-name");
    let current_value = $(this).val();
    if (previous_admin_settings[setting_name] != current_value) {
      change_server_setting(setting_name, current_value);
      previous_admin_settings[setting_name] = current_value;
    }
  });
  $(".toggler .settings-item.admin").change(function () {
    let setting_name = $(this).data("setting-name");
    let current_value = $(this).children("input").is(":checked");
    change_server_setting(setting_name, current_value);
  });
  $(".text-input-container.dropdown .dropdown-item").click(function () {
    let setting_name = $(this).parent().data("setting-name");
    let dropdown_id = $(this).data("id");
    change_server_setting(setting_name, dropdown_id);
    let new_text = $(this).text();
    $(this).parent().parent().find(".settings-item-text").text(new_text);
  });
  $(".refresh-conreq-api").click(function () {
    let setting_name = $(this).data("setting-name");
    change_server_setting(setting_name);
  });
  $(".reload-needed").click(function () {
    reload_needed = true;
  });

  // User Management events
  $(".action-btn.delete").click(function () {
    let btn = $(this);
    let delete_query =
      btn.data("delete-url") + "?username=" + encodeURI(btn.data("username"));
    post_url(delete_query, function (result) {
      if (result.success) {
        btn.parent().parent().remove();
      }
    }).fail(function () {
      conreq_no_response_toast_message();
    });
  });
  $(".standard-btn.invite-user").click(function () {
    let btn = $(this);
    let generate_invite_url = btn.data("generate-invite-url");
    let sign_up_url = window.location.origin + btn.data("sign-up-url");
    http_request.abort();
    http_request = $.get(generate_invite_url, function (result) {
      let invite_link =
        sign_up_url + "?invite_code=" + encodeURI(result.invite_code);
      copy_to_clipboard(invite_link);
      invite_copied_toast_message();
    });
  });
};

// Destroys old viewport JS instances
let destroy_viewport = function () {
  if (masonry_grid != null) {
    if (infinite_scroller_created) {
      masonry_grid.infiniteScroll("destroy");
      infinite_scroller_created = false;
    }
    masonry_grid.masonry("destroy");
    masonry_grid = null;
  }
  if (review_carousel != null) {
    review_carousel.destroy();
    review_carousel = null;
  }
  if (videos_carousel != null) {
    videos_carousel.destroy();
    videos_carousel = null;
  }
  if (recommended_carousel != null) {
    recommended_carousel.destroy();
    recommended_carousel = null;
  }
  if (images_carousel != null) {
    images_carousel.destroy();
    images_carousel = null;
  }
  if (collection_carousel != null) {
    collection_carousel.destroy();
    collection_carousel = null;
  }
  if (cast_carousel != null) {
    cast_carousel.destroy();
    cast_carousel = null;
  }

  $(".viewport-container>*:not(.loading-animation-container)").remove();
};

// Preforms any actions needed to prepare the viewport
let refresh_viewport = function () {
  // Create any carousels that need to be made
  create_all_carousels();

  // Create the masonry grid
  masonry_grid = $(".viewport-masonry").masonry({
    itemSelector: ".masonry-item",
    gutter: 10,
    horizontalOrder: true,
    fitWidth: true,
    transitionDuration: "0s",
    stagger: "0s",
    isStill: true,
  });

  // Configure infinite scrolling
  if ($(".infinite-scroll").length) {
    setTimeout(function () {
      masonry_grid.infiniteScroll({
        path: get_window_location() + "?page={{#}}",
        append: ".masonry-item",
        outlayer: masonry_grid.data("masonry"),
        prefill: true,
        elementScroll: ".viewport-container",
        history: false,
        scrollThreshold: $(".viewport-container").height() * 2,
      });

      masonry_grid.on("append.infiniteScroll", function () {
        cull_old_posters();
        content_preview_modal_click_event();
      });

      infinite_scroller_created = true;
    }, 500);
  }

  // Lazy load page elements
  lazyloader.update();
};

// Fetch the new viewport and update the current tab
var generate_viewport = function () {
  // Check if the whole webpage needs to be reloaded
  if (reload_needed) {
    location.reload();
  }

  // Read the URL hash to determine what page we are on
  let window_location = get_window_location();

  // If there is no hash, add one
  if (window_location == "" || window_location == null) {
    if (window.history.replaceState) {
      // Replace the current page in the browser history to add a hash
      window.history.replaceState({}, null, "#/discover/");
      window_location = window.location.hash.split("#")[1];
    }
  }

  // Asynchronously fetch new viewport content
  viewport_loaded = false;
  http_request.abort();

  // Change the current tab
  update_active_tab();

  http_request = $.get(window_location, function (viewport_html) {
    // Save that the page was successfully loaded
    viewport_loaded = true;

    // Destroy old JS elements and event handlers
    destroy_viewport();

    // Inject and configure the new content
    $(".viewport-container")[0].innerHTML = DOMPurify.sanitize(viewport_html);
    refresh_viewport();
    add_event_listeners();

    // Display the new content
    $(".viewport-container>.loading-animation-container").hide();
    $(".viewport-container>*:not(.loading-animation-container)").show();
    setTimeout(function () {
      $(".viewport-container>.viewport").css("opacity", "1");
    }, 10);
  });

  // If the page is taking too long to load, show a loading animation
  setTimeout(function () {
    if (!viewport_loaded) {
      // Hide the viewport and display the loading animation
      $(".viewport-container>*:not(.loading-animation-container)").hide();
      $(".viewport-container>.loading-animation-container").show();
    }
  }, 600);
};

// Perform actions whenever the HTML on the page changes
let page_mutation_observer = function () {
  let observer = new MutationObserver(function () {
    // Initiate Lazyload on any new images
    lazyloader.update();
  });

  // Configuration of the observer
  let config = {
    attributes: false,
    characterData: false,
    subtree: true,
    childList: true,
  };

  // Select the target node
  let target = document.querySelector("body");

  // Begin observing the modal
  observer.observe(target, config);
};

// Obtain the initial page
page_mutation_observer();
generate_viewport();

// Fetch a new page when the URL changes
if ("onhashchange" in window) {
  // Window anchor change event supported?
  window.onhashchange = function () {
    generate_viewport();
  };
} else {
  // Window anchor change event not supported
  var storedHash = window.location.hash;
  window.setInterval(function () {
    if (window.location.hash != storedHash) {
      generate_viewport();
    }
  }, 100);
}
