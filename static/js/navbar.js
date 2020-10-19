// Event
$("#content-search").bind("enterKey", function(e) {
    let parameters = $(this).val();
    window.location = "/search/?query=" + encodeURI(parameters);
});

// Event Listener
$("#content-search").keyup(function(e) {
    if (e.keyCode == 13) {
        $(this).trigger("enterKey");
    }
});