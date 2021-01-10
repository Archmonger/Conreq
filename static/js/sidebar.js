new SimpleBar($("#sidebar")[0]);

$(".nav-tab").each(function() {
    $(this).click(function() {
        $("#sidebar").collapse("hide");
    });
});