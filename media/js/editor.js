$(document).ready(function() {
    $("#id_image").attr("onchange", "update_image(this)");
    $("#id_image").attr("onkeyup", "update_image(this)");
    $("#filter").attr("onchange", "filter_images()");
    $("#filter").attr("onkeyup", "filter_images()");
    document.getElementById("id_slug").onchange = function() { this._changed = true; };
    document.getElementById("id_title").onkeyup = function() {
        var e = document.getElementById("id_slug");
        if (!e._changed) { e.value = URLify(document.getElementById("id_title").value, 50); }
    }
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
tinyMCE.init({
    mode : "textareas",
    theme : "advanced",
    theme_advanced_buttons1 : "undo,redo,charmap,search,replace,|,link,unlink,image,emotions,|,code,fullscreen",
    theme_advanced_buttons2 : "formatselect,fontsizeselect,bold,italic,underline,strikethrough,sub,sup,|,justifyleft,justifycenter,justifyright,justifyfull,outdent,indent,|,bullist,numlist,|,forecolor,backcolor,removeformat",
    theme_advanced_buttons3 : "",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_path_location : "bottom",
    theme_advanced_resizing : true,
    browsers : "msie,gecko,opera,safari",
    dialog_type : "modal",
    entity_encoding : "raw",
    relative_urls : false,
    convert_urls : false,
    width : "783",
    height : "300",
    extended_valid_elements : "a[name|href|target|title],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|name|style],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
    advimage_update_dimensions_onchange: true,
    file_browser_callback : 'oiFileBrowser',
    plugins : "advimage,autosave,searchreplace,table,visualchars,advlink,emotions,media,style,template,xhtmlxtras,fullscreen",
    gecko_spellcheck : true,
    language : "tr"
});

function oiFileBrowser (field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        file : "/admin/upload/image/tinymce/",
        title : "File Browser",
        width : 300,
        height : 100,
        close_previous : "no"
    }, {
        window : win,
        input : field_name,
        resizable : "yes",
        inline : "yes",
    });
    return false;
}
