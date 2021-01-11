new SimpleBar($("#sidebar")[0]);

$(".nav-tab.suboption").each(function() {
    $(this).click(function() {
        $("#sidebar").collapse("hide");
    });
});