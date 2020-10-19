var collectionCarousel = tns({
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

$(".moreInfo-collection-btn").click(function() {
    $(".moreInfo-collection")[0].scrollIntoView({
        behavior: "smooth",
    });
});