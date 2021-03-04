let searchbar_input = $("#content-search");

// Search Event Action
$("#content-search").on("enterKey", async function () {
	perform_search();
});

// Search Event Listener
$("#content-search").keyup(async function (e) {
	if (e.keyCode == 13) {
		$(this).trigger("enterKey");
	}
});

// Magnifying Glass Click Event
$(".searchbar .fas.fa-search").click(async function () {
	perform_search();
});

// Performs a search
let perform_search = async function () {
	let parameters = searchbar_input.val();
	window.location =
		"#" +
		searchbar_input.data("search-url") +
		"?query=" +
		encodeURI(parameters);
};

// Slide in animations for navbar, sidebar, and viewport
AOS.init();
