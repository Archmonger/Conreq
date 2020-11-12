new SimpleBar($(".viewport-container")[0]);

$(".viewport-posters").masonry({
    itemSelector: ".masonry-item",
    gutter: 10,
    horizontalOrder: true,
    fitWidth: true,
    transitionDuration: "0.8s",
    stagger: "0.03s",
});
$(".viewport-posters").css("opacity", "1");