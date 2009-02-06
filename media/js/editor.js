$(document).ready(function() {
    $("#id_image").attr("onchange", "update_image(this)");
    $("#id_image").attr("onkeyup", "update_image(this)");
    $("#filter").attr("onchange", "filter_images()");
    $("#filter").attr("onkeyup", "filter_images()");
});
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
    } else {
        $("#id_image > option").show();
        $("#filter").css("color", "");
    }
}
function update_image(selectBox) {
    $("#image_thumb").attr("src", "/media/" + selectBox[selectBox.selectedIndex].innerHTML);
}
