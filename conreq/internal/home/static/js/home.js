$(document).ready(async function () {
	AOS.init();
});

// TODO: Old code. Reassess all of this.
// var toast_message = async function (parameters) {
// 	iziToast.show(parameters);
// };

// var hide_popups = async function () {
// 	$("#modal-container").modal("hide");
// 	if (window.matchMedia("(max-width: 800px)").matches) {
// 		if (!$("#sidebar").hasClass("collapsed")) {
// 			$("#sidebar").addClass("collapsed");
// 		}
// 	}
// };

// var sidebar_collapse = async function () {
// 	$(".nav-tab.suboption, .navbar-toggler").each(async function () {
// 		console.log(this);
// 		$(this).click(async function () {
// 			if (window.matchMedia("(max-width: 800px)").matches) {
// 				if ($("#sidebar").hasClass("collapsed")) {
// 					$("#sidebar").removeClass("collapsed");
// 				} else {
// 					$("#sidebar").addClass("collapsed");
// 				}
// 			}
// 		});
// 	});
// };

// $(document).ready(async function () {
// 	if ($("#sidebar")[0]) {
// 		new SimpleBar($("#sidebar")[0]);
// 		sidebar_collapse();
// 	}
// });
