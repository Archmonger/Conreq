let ongoing_request = null;
let report_selection = null;

var request_btn_click_event = async function () {
	$(".request-btn").each(async function () {
		$(this).unbind("click");
		$(this).click(async function () {
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
				post_json($(this).data("request-url"), params, function () {
					let request_btn = $(".request-btn");
					requested_toast_message();
					if ($(window).width() < 1000) {
						$(".request-btn").hide();
					}
					request_btn.text("REQUESTED");
					request_btn.unbind("click");
					request_btn.removeClass("clickable");
					$("#modal-container").modal("hide");
					ongoing_request = null;
				}).fail(async function () {
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
						$(".series-modal-btn").text("REQUESTED");
						$("#modal-container").modal("hide");
						ongoing_request = null;
					}).fail(async function () {
						conreq_no_response_toast_message();
						ongoing_request = null;
					});
				}

				// Request parts of the show
				else if (
					selection.seasons.length ||
					selection.episode_ids.length
				) {
					params.seasons = selection.seasons;
					params.episode_ids = selection.episode_ids;
					post_json($(this).data("request-url"), params, function () {
						requested_toast_message();
						$(".series-modal-btn").text("REQUESTED");
						$("#modal-container").modal("hide");
						ongoing_request = null;
					}).fail(async function () {
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

var collection_btn_click_event = async function () {
	$(".more-info-collection-btn").click(async function () {
		$(".more-info-collection")[0].scrollIntoView({
			behavior: "smooth",
		});
	});
};

var quick_info_btn_click_event = async function () {
	$(".quick-info-read-more-btn").click(async function () {
		$(".more-info-quick-info.collapse").collapse("toggle");
		$(this).remove();
	});
};

var create_content_modal_click_event = async function () {
	$(
		".series-modal-btn, .content-preview-modal-btn, .report-selection-modal-btn"
	).each(async function () {
		$(this).unbind("click");
		$(this).click(async function () {
			let params = {
				tmdb_id: $(this).data("tmdb-id"),
				tvdb_id: $(this).data("tvdb-id"),
				content_type: $(this).data("content-type"),
				report_modal: $(this).hasClass("report-selection-modal-btn"),
			};
			generate_modal($(this).data("modal-url") + "?" + $.param(params));
		});
	});
};

var create_report_modal_click_event = async function () {
	$(".report-modal-btn").each(async function () {
		$(this).unbind("click");
		$(this).click(async function () {
			let params = {
				tmdb_id: $(this).data("tmdb-id"),
				tvdb_id: $(this).data("tvdb-id"),
				content_type: $(this).data("content-type"),
			};

			// Report an issue with a movie
			if (params.content_type == "movie") {
				report_selection = null;
				generate_modal(
					$(this).data("modal-url") + "?" + $.param(params)
				);
			}

			// Report an issue with a TV show
			else if (params.content_type == "tv") {
				// Determine what checkboxes are checked
				let current_selection = modal_checkbox_aggregator();
				report_selection = null;

				// All non-special seasons were checkboxed
				if (current_selection == true) {
					generate_modal(
						$(this).data("modal-url") + "?" + $.param(params)
					);
				}

				// Parts of the show are checkboxed
				else if (
					current_selection.seasons.length ||
					current_selection.episodes.length ||
					current_selection.episode_ids.length
				) {
					report_selection = current_selection;
					generate_modal(
						$(this).data("modal-url") + "?" + $.param(params)
					);
				}

				// User didn't select anything
				else {
					no_selection_toast_message();
				}
			}
		});
	});
};

var create_filter_modal_click_event = async function () {
	$(".filter-modal-btn").each(async function () {
		$(this).unbind("click");
		$(this).click(async function () {
			generate_modal($(this).data("modal-url"));
		});
	});
};

var report_btn_click_event = async function () {
	$(".report-btn").each(async function () {
		$(this).unbind("click");
		$(this).click(async function () {
			let params = {
				tmdb_id: $(this).data("tmdb-id"),
				tvdb_id: $(this).data("tvdb-id"),
				content_type: $(this).data("content-type"),
				issue_ids: $(".checkbox:checked")
					.map(async function () {
						return $(this).data("issue-id");
					})
					.get(),
			};

			// Ensure the user selected something
			if (!params.issue_ids.length) {
				no_selection_toast_message();
				return false;
			}

			// Save the episodes/seasons reported in the previous step
			if (params.content_type == "tv" && report_selection) {
				$.extend(params, report_selection);
			}

			// Prevent the user from spamming the button
			if (ongoing_request == this) {
				return false;
			} else {
				ongoing_request = this;
			}

			// Request a movie
			post_json($(this).data("report-url"), params, function () {
				reported_toast_message();
				$(".request-btn").text("REQUESTED");
				$("#modal-container").modal("hide");
				ongoing_request = null;
			}).fail(async function () {
				conreq_no_response_toast_message();
				ongoing_request = null;
			});
		});
	});
};

var modal_select_all_btn_click_event = async function () {
	$(".modal .select-all-btn").click(async function () {
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

var row_title_click_event = async function () {
	$(".modal .row-title-container").click(async function () {
		// Checkmark the season
		let season_block = $(this.parentElement);
		let season_checkbox = season_block.find("input");
		season_checkbox.prop("checked", !season_checkbox.prop("checked"));

		// Checkmark all related episodes
		let episode_container = $(
			season_checkbox.data("all-suboptions-container")
		);
		let episode_checkboxes = episode_container.find("input");
		episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
	});
};

var row_checkbox_click_event = async function () {
	$(".modal .checkbox").click(async function () {
		// Checkmark all related episodes
		let season_checkbox = $(this);
		let episode_container = $(
			season_checkbox.data("all-suboptions-container")
		);
		let episode_checkboxes = episode_container.find("input");
		episode_checkboxes.prop("checked", season_checkbox.prop("checked"));
	});
};

var row_suboption_title_click_event = async function () {
	$(".modal .suboption-title-container").click(async function () {
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
			if (
				episode_checkboxes.length ==
				checkmarked_episode_checkboxes.length
			) {
				season_checkbox.prop("checked", true);
			}
		}
	});
};

var row_suboption_checkbox_click_event = async function () {
	$(".modal .suboption-checkbox").click(async function () {
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
			let episode_checkboxes = all_episodes_container.find("input");
			let checkmarked_episode_checkboxes = episode_checkboxes.filter(
				"input:checked"
			);
			if (
				episode_checkboxes.length ==
				checkmarked_episode_checkboxes.length
			) {
				season_checkbox.prop("checked", true);
			}
		}
	});
};

var modal_expand_btn_click_event = async function () {
	$(".modal .fa-expand").click(async function () {
		$("#modal-container").modal("hide");
	});
};

var issue_approve_btn_click_event = async function () {
	$(".issue-manage-icons .fas.approve").click(async function () {
		let params = {
			action: "resolve",
			request_id: $(this.parentElement).data("request-id"),
			resolved: !($(this.parentElement).data("resolved") == "True"),
		};
		post_json($(this.parentElement).data("url"), params, function () {
			generate_viewport(false);
		}).fail(async function () {
			conreq_no_response_toast_message();
		});
	});
};

var issue_delete_btn_click_event = async function () {
	$(".issue-manage-icons .fas.delete").click(async function () {
		let params = {
			action: "delete",
			request_id: $(this.parentElement).data("request-id"),
		};
		post_json($(this.parentElement).data("url"), params, function () {
			generate_viewport(false);
		}).fail(async function () {
			conreq_no_response_toast_message();
		});
	});
};

var simple_filter_btn_click_event = async function () {
	$(".simple-filter-btn").click(async function () {
		let extras = "";
		if ($("input.anime-only:checked").length) {
			extras = "&type=anime";
		} else if ($("input.no-anime:checked").length) {
			extras = "&type=no-anime";
		}
		window.location = $(this).data("href") + extras;
		$("#modal-container").modal("hide");
	});
};

var search_click_event = async function () {
	$(".content-search").unbind("keyup");
	$(".content-search").on("keyup", async function (e) {
		if (e.keyCode == 13) {
			perform_search();
		}
	});
	$(".searchbar .fas.fa-search").unbind("click");
	$(".searchbar .fas.fa-search").click(async function () {
		perform_search();
	});
};

var user_delete_btn_click_event = async function () {
	$(".action-btn.delete").click(async function () {
		let btn = $(this);
		let delete_query =
			btn.data("delete-url") +
			"?username=" +
			encodeURI(btn.data("username"));
		post_url(delete_query, function (result) {
			if (result.success) {
				btn.parent().parent().remove();
			}
		}).fail(async function () {
			conreq_no_response_toast_message();
		});
	});
};

var user_invite_btn_click_event = async function () {
	$(".standard-btn.invite-user").click(async function () {
		let btn = $(this);
		let generate_invite_url = btn.data("generate-invite-url");
		let sign_up_url = window.location.origin + btn.data("sign-up-url");
		get_url(generate_invite_url, function (result) {
			let invite_link =
				sign_up_url + "?invite_code=" + encodeURI(result.invite_code);
			create_invite_link_elem(invite_link);
		}).fail(conreq_no_response_toast_message);
		copy_to_clipboard();
	});
};

var reload_needed_click_event = async function () {
	$(".reload-needed").click(async function () {
		page_reload_needed = true;
	});
};

var refresh_api_key_click_event = async function () {
	$(".refresh-conreq-api").click(async function () {
		let setting_name = $(this).data("setting-name");
		change_server_setting(setting_name);
	});
};

var server_settings_dropdown_click_event = async function () {
	$(".text-input-container.dropdown .dropdown-item").click(async function () {
		let setting_name = $(this).parent().data("setting-name");
		let dropdown_id = $(this).data("id");
		change_server_setting(setting_name, dropdown_id).then(
			async function () {
				generate_viewport(false);
			}
		);
	});
};

var sidebar_collapse_click_event = async function () {
	$(".nav-tab.suboption, .navbar-toggler").each(async function () {
		$(this).click(async function () {
			if (window.matchMedia("(max-width: 800px)").matches) {
				if ($("#sidebar").hasClass("collapsed")) {
					$("#sidebar").removeClass("collapsed");
				} else {
					$("#sidebar").addClass("collapsed");
				}
			}
		});
	});
};
