let modal_loaded = false;

// Fetches a modal via AJAX
var generate_modal = async function (modal_url) {
	let modal_dialog = $("#modal-dialog");
	// Fetch the series modal
	modal_loaded = false;
	get_url(modal_url, async function (modal_html) {
		// Save that the modal was successfully loaded
		modal_loaded = true;

		// Place the new HTML on the page
		modal_dialog[0].innerHTML = DOMPurify.sanitize(modal_html);

		// Show the new content
		$("#modal-container .loading-animation").hide();
		$("#modal-content").show();
		$("#modal-container").modal("show");

		// Add click events
		request_btn_click_event();
		content_modal_click_event();
		quick_request_click_event();
		modal_select_all_btn_click_event();
		modal_expand_btn_click_event();
		row_title_click_event();
		row_checkbox_click_event();
		row_suboption_title_click_event();
		row_suboption_checkbox_click_event();
		create_report_modal_click_event();
		report_btn_click_event();
		simple_filter_btn_click_event();
		modal_poster_popup_click_event();
		delete_user_btn_click_event();
		save_user_btn_click_event();
	}).fail(async function () {
		// Server couldn't fetch the modal
		if (http_request.statusText != "abort") {
			conreq_no_response_toast_message();
		}
		$("#modal-container").modal("hide");
	});

	// If the modal is taking too long to load, show a loading animation
	setTimeout(async function () {
		if (!modal_loaded) {
			// Show the loading icon
			$("#modal-content").hide();
			$("#modal-container").modal("show");
			$("#modal-container .loading-animation").show();
		}
	}, 300);
};
