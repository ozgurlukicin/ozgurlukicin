function update_image() {
    var path = $("#id_image option:selected").text()
    $("#image_thumb").attr("src", "/media/" + path);
}
$(document).ready(function() {
    $("#id_image").bind("change", update_image);
    $(".image").before("<div class=\"row cells-1 image_filter\"><div><div class=\"column span-4\"><label for=\"image_filter\">Görselleri Filtrele:</label></div><div class=\"column span-flexible\"><input type=\"text\" maxlength=\"32\" name=\"image_filter\" class=\"vTextField\" id=\"filter\"/><p class=\"help\">Burayı kullanarak görsellerde arama yapabilirsiniz.</p></div></div></div>");
    $(".image > div").after("<img src=\"\" id=\"image_thumb\" alt=\"Üstteki arama kutusunu kullanıp listeden bir görsel seçiniz\" />");
    $("#filter").bind("change keyup", filter_images);
    update_image();
});
function filter_images() {
    if ($("#filter").val().length > 2) {
        $("#id_image > option").hide();
        var results =  $("#id_image > option:contains('" + $("#filter").val() + "')");
        results.show();
        if (results.length === 0) {
            $("#filter").css("color", "red");
        } else {
            $("#filter").css("color", "");
        }
    } else {
        $("#id_image > option").show();
        $("#filter").css("color", "");
    }
}
