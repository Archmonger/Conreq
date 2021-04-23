var create_all_carousels = async function () {
	create_review_carousel();
	create_video_carousel();
	create_recommended_carousel();
	create_image_carousel();
	create_collection_carousel();
	create_cast_carousel();
	create_crew_carousel();
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

var recommended_carousel = null;
var create_recommended_carousel = async function () {
	let loader = $("#recommended_loader");
	if (loader.length) {
		$.get(loader.data("url"), function (fetched_html) {
			loader.replaceWith(DOMPurify.sanitize(fetched_html));

			if ($(".recommended-inner-container").length) {
				recommended_carousel = tns({
					container: ".recommended-inner-container",
					controlsContainer: ".recommended-carousel-controls",
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

				create_content_modal_click_event();

				$(".more-info-recommendations").collapse("show");
			}
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

var collection_carousel = null;
var create_collection_carousel = async function () {
	let loader = $("#collection_loader");
	if (loader.length) {
		$.get(loader.data("url"), function (fetched_html) {
			loader.replaceWith(DOMPurify.sanitize(fetched_html));

			if ($(".collection-inner-container").length) {
				collection_carousel = tns({
					container: ".collection-inner-container",
					controlsContainer: ".collection-carousel-controls",
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

				collection_btn_click_event();
				create_content_modal_click_event();

				$(".more-info-collection").collapse("show");
			}
		});
	}
};

var cast_carousel = null;
var create_cast_carousel = async function () {
	if ($(".cast-inner-container").length) {
		cast_carousel = tns({
			container: ".cast-inner-container",
			controlsContainer: ".cast-carousel-controls",
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

var crew_carousel = null;
var create_crew_carousel = async function () {
	if ($(".crew-inner-container").length) {
		crew_carousel = tns({
			container: ".crew-inner-container",
			controlsContainer: ".crew-carousel-controls",
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
