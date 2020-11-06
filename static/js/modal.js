var modal_select_all = function() {
    let modal_text = $(".modal-button.select-button").text();
    if (modal_text == "SELECT ALL") {
        $(".modal-button.select-button").text("UNSELECT ALL");
    } else {
        $(".modal-button.select-button").text("SELECT ALL");
    }
};

let modal_body = $(".modal-body")[0];
if (modal_body != null) {
    new SimpleBar(modal_body);
}