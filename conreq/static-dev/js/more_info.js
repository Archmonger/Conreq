var create_all_carousels = async function () {
	create_review_carousel();
	create_video_carousel();
	create_image_carousel();
	viewport_carousel_constructor();
};

var all_carousels = [];
var viewport_carousel_constructor = async function () {
	$(".viewport .carousel.auto-construct:not(.constructed)").each(
		async function () {
			let current_carousel = $(this);
			let inner_container = current_carousel.find(
				".carousel-inner-container"
			)[0];
			let controls = current_carousel.find(".carousel-controls")[0];
			all_carousels.push(
				tns({
					container: inner_container,
					controlsContainer: controls,
					swipeAngle: 60,
					autoWidth: true,
					loop: false,
					speed: 300,
					mouseDrag: true,
					gutter: 10,
					nav: false,
					slideBy: "page",
					edgePadding: 20,
				})
			);
			current_carousel.addClass("constructed");
		}
	);
};

var viewport_carousel_destructor = async function () {
	$(all_carousels).each(async function () {
		this.destroy();
	});
	all_carousels = [];
};

var review_carousel = null;
var create_review_carousel = async function () {
	if ($(".reviews-inner-container").length) {
		review_carousel = tns({
			container: ".reviews-inner-container",
			items: 1,
			speed: 300,
			swipeAngle: 60,
			rewind: true,
			mouseDrag: true,
			gutter: 10,
			controls: false,
			navPosition: "bottom",
			autoplayPosition: "bottom",
			autoplayButtonOutput: false,
			responsive: {
				1601: {
					items: 3,
				},
				1151: {
					items: 2,
				},
			},
		});
	}
};

var youtube_players = null;
var create_youtube_players = async function () {
	youtube_players = [];
	$(".youtube-player").each(async function () {
		let player = new YT.Player(this, {
			height: "", // Set by CSS
			width: "", // Set by CSS
			videoId: $(this).data("video-key"),
			playerVars: {
				frameborder: "0",
				enablejsapi: "1",
				modestbranding: "1",
			},
		});
		youtube_players.push(player);
	});
};

var videos_carousel = null;
var create_video_carousel = async function () {
	// Create youtube video players
	create_youtube_players();

	// Set up the carousel
	if ($(".videos-inner-container").length) {
		videos_carousel = tns({
			container: ".videos-inner-container",
			controlsContainer: ".videos-carousel-controls",
			swipeAngle: 60,
			autoWidth: true,
			loop: false,
			items: 3,
			speed: 300,
			mouseDrag: true,
			gutter: 10,
			nav: false,
			slideBy: "page",
			edgePadding: 20,
		});
	}
};

var images_carousel = null;
var create_image_carousel = async function () {
	if ($(".artwork-inner-container").length) {
		images_carousel = tns({
			container: ".artwork-inner-container",
			controlsContainer: ".artwork-carousel-controls",
			swipeAngle: 60,
			loop: false,
			items: 3,
			autoWidth: true,
			speed: 300,
			mouseDrag: true,
			gutter: 10,
			nav: false,
			slideBy: "page",
			edgePadding: 20,
		});

		$(document).ready(async function () {
			$(".artwork-container").magnificPopup({
				delegate: "a",
				type: "image",
				mainClass: "mfp-no-margins", // class to remove default margin from left and right side
				gallery: {
					enabled: true,
					navigateByImgClick: true,
					preload: [1, 1], // Will preload 1 before and 1 after the current image
				},
			});
		});
	}
};
