function removeTag(tag) {
    $("#id_tags > option:selected:contains("+tag+")")[0].selected=false;
    $("#selectedItems > .item:contains("+tag+")").remove();
}
function updateSelectedList() {
    var ob = $("#id_tags")[0];
    var selected = "";
    $("#selectedItems").remove();
    for (var i = 0; i < ob.options.length; i++)
        if (ob.options[i].selected) {
            var tag = ob.options[i].innerHTML;
            selected = selected + "<div class=\"item\"><span class=\"tagName\">"+tag+"</span><span class=\"removeButton\" onclick=\"removeTag('"+tag+"')\">x</span></div>";
        }
    $("#id_tags").before("<div id=\"selectedItems\">"+selected+"</div>");
}
$(document).ready(function() {
    $("#id_tags").attr("onkeyup", "updateSelectedList()");
    $("#id_tags").attr("onchange", "updateSelectedList()");
    $("#id_tags").before("<input id=\"tagfilter\" class=\"vTextField\" type=\"text\" />");
    updateSelectedList();
    $("#tagfilter").autocomplete({
        source:"#id_tags",
        onSelect:function(){
            options = $("#id_tags > option");
            var i = 0;
            while (i<options.length && options[i].innerHTML!=$("#tagfilter").val()) {
                i = i + 1;
            }
            options[i].selected = true;
            updateSelectedList();
            /*var length = $("#selectedItems > .item").length;
            if (length > 5) {
                $("#id_tags > option:contains('" + $("#tagfilter").val() + "')")[0].selected = false;
                updateSelectedList();
                $("#selectedItems").append("<p class=\"error\">En fazla 5 tane etiket seçebilirsiniz!</p>");
            }*/
        },
        minchar:2
        });
});
