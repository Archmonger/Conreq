var create_all_carousels = async function () {
	create_review_carousel();
	create_video_carousel();
	create_recommended_carousel();
	create_image_carousel();
	create_collection_carousel();
	create_cast_carousel();
};

var review_carousel = null;
var create_review_carousel = async function () {
	if ($(".more-info-reviews").length) {
		review_carousel = tns({
			container: ".more-info-reviews",
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

var videos_carousel = null;
let youtube_card_template = `<iframe title="YouTube Video" class="youtube-player" type="text/html" src="https://www.youtube.com/embed/{{video.key}}?modestbranding=1" frameborder="0" allowfullscreen="allowfullscreen" mozallowfullscreen="mozallowfullscreen" msallowfullscreen="msallowfullscreen" oallowfullscreen="oallowfullscreen" webkitallowfullscreen = "webkitallowfullscreen"></iframe>`;
var create_video_carousel = async function () {
	// Create the youtube iframes from the given template
	$(".youtube-player-loader").each(function () {
		$(this).replaceWith(
			youtube_card_template.replace(
				"{{video.key}}",
				$(this).data("video-key")
			)
		);
	});
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
				closeOnContentClick: true,
				closeBtnInside: true,
				fixedContentPos: true,
				mainClass: "mfp-no-margins mfp-with-zoom", // class to remove default margin from left and right side
				image: {
					verticalFit: true,
				},
				zoom: {
					enabled: false,
					duration: 300, // don't foget to change the duration also in CSS
				},
				gallery: {
					enabled: true,
					navigateByImgClick: true,
					preload: [0, 1], // Will preload 0 - before current, and 1 after the current image
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
