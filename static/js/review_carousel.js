var reviewCarousel = tns({
    container: ".moreInfo-reviews",
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