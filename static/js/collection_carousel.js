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

$(".more-info-collection-btn").click(function() {
    $(".more-info-collection")[0].scrollIntoView({
        behavior: "smooth",
    });
});