var show_modal_loader = async function () {
	$("#modal-container .loading-animation").show();
	$("#modal-content").hide();
	$("#modal-container").modal("show");
};

var show_modal = async function () {
	$("#modal-container .loading-animation").hide();
	$("#modal-content").show();
	$("#modal-container").modal("show");
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

// TODO: Reassess
$(document).ready(async function () {
	if ($("#sidebar")[0]) {
		new SimpleBar($("#sidebar")[0]);
		sidebar_collapse();
	}
});

// Shows a toast message
var toast_message = async function (parameters) {
	iziToast.show(parameters);
};

// Hide any floaty objects
var hide_popups = async function () {
	$("#modal-container").modal("hide");
	if (window.matchMedia("(max-width: 800px)").matches) {
		if (!$("#sidebar").hasClass("collapsed")) {
			$("#sidebar").addClass("collapsed");
		}
	}
};

// Creates a page element that copy_to_clipboard can copy from
var create_invite_link_elem = function (invite_link) {
	const el = document.createElement("textarea");
	el.value = invite_link;
	el.textContent = invite_link;
	el.readOnly = true;
	el.style.position = "absolute";
	el.style.left = "-99999px";
	el.id = "invite_link";
	el.className = "invite_link";
	document.body.appendChild(el);
};
