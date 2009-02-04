function filter_images() {
    if ($("#filter").val().length > 2) {
        $("#id_image > option").hide();
        var results =  $("#id_image > option:contains('" + $("#filter").val() + "')")
        results.show();
        if (results.length == 0) {
            $("#filter").css("color", "red");
        } else {
            $("#filter").css("color", "");
        }
    }
}
