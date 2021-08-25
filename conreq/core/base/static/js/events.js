let modal_loaded = false;

// TODO: Reassess
var generate_modal = async function (modal_url) {
	let modal_dialog = $("#modal-dialog");
	// Fetch the series modal
	modal_loaded = false;
	get_url(modal_url, async function (modal_html) {
		// Save that the modal was successfully loaded
		modal_loaded = true;

		// Place the new HTML on the page
		modal_dialog[0].innerHTML = modal_html;

		// Show the new content
		$("#modal-container .loading-animation").hide();
		$("#modal-content").show();
		$("#modal-container").modal("show");
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

// TODO: Reassess
var sidebar_collapse = async function () {
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

// TODO: Remove this
var manage_user_btn = async function () {
	$(".manage-user-btn").unbind("click");
	$(".manage-user-btn").click(async function () {
		let params = {
			username: escape($(this).data("username")),
		};
		generate_modal($(this).data("modal-url") + "?" + $.param(params));
	});
};

// TODO: Remove this
$(document).ready(async function () {
	$(".viewport-container").on("loaded", async function () {
		// Bootstrap Table
		if ($("table").length) {
			$("table").bootstrapTable();
		}
	});

	$(".viewport-container").on("destroy", function () {
		// Bootstrap Table
		if ($("table").length) {
			$("table").bootstrapTable("destroy");
		}
	});
});

// TODO: Reassess
$(document).ready(async function () {
	if ($("#sidebar")[0]) {
		new SimpleBar($("#sidebar")[0]);
		sidebar_collapse();
		manage_user_btn();
	}
});

var toast_message = async function (parameters) {
	iziToast.show(parameters);
};
