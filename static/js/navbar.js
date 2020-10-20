// Search Event
$("#content-search").bind("enterKey", function(e) {
    let parameters = $(this).val();
    window.location = "/search/?query=" + encodeURI(parameters);
});

// Search Event Listener
$("#content-search").keyup(function(e) {
    if (e.keyCode == 13) {
        $(this).trigger("enterKey");
    }
});

// Set input value on completion of search event
let searchParams = new URLSearchParams(window.location.search);
if (window.location.pathname == "/search/" && searchParams.has("query")) {
    $("#content-search").val(decodeURI(searchParams.get("query")));
}