let ongoing_request = null;
let report_selection = null;

var delete_user_btn_click_event = async function () {
	$(".delete-user-btn").click(async function () {
		let btn = $(this);
		let delete_query =
			btn.data("delete-url") +
			"?username=" +
			escape(btn.data("username"));
		post_url(delete_query, function (result) {
			if (result.success) {
				$("#modal-container").modal("hide");
				success_toast_message();
			}
		}).fail(async function () {
			conreq_no_response_toast_message();
		});
	});
};

var manage_user_btn_click_event = async function () {
	$(".manage-user-btn").unbind("click");
	$(".manage-user-btn").click(async function () {
		let params = {
			username: escape($(this).data("username")),
		};
		generate_modal($(this).data("modal-url") + "?" + $.param(params));
	});
};

var save_user_btn_click_event = async function () {
	$(".save-user-btn").click(async function () {
		post_modal_form(async function (response) {
			if (response.success) {
				$("#modal-container").modal("hide");
				save_success_toast_message();
			} else {
				error_toast_message(response.message);
			}
		}).fail(async function () {
			conreq_no_response_toast_message();
		});
	});
};

var invite_user_btn_click_event = async function () {
	$(".cr-btn.invite-user").click(async function () {
		let btn = $(this);
		let generate_invite_url = btn.data("generate-invite-url");
		let sign_up_url = window.location.origin + btn.data("sign-up-url");
		get_url(generate_invite_url, function (result) {
			let invite_link =
				sign_up_url + "?invite_code=" + escape(result.invite_code);
			create_invite_link_elem(invite_link);
		}).fail(conreq_no_response_toast_message);
		copy_to_clipboard();
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
