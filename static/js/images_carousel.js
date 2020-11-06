var imagesCarousel = tns({
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

$(document).ready(function() {
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