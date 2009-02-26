function removeTag(tag, removeButton) {
    $("#id_tags > option:selected").each(function (index, option){
        if (option.innerHTML == tag)
            return option.selected = false;
    });
    $(removeButton).parent().fadeOut("fast", function(){ $(this).remove() });
}
function updateSelectedList() {
    var selected = "";
    $("#id_tags > option:selected").each(function(index, option) {
        var tag = option.innerHTML;
        selected = selected + "<div class=\"item\"><span class=\"tagName\">"+tag+"</span><span class=\"removeButton\" onclick=\"removeTag('"+tag+"', this)\">x</span></div>";
    });
    $("#selectedItems").remove();
    $("#id_tags").before("<div id=\"selectedItems\">"+selected+"</div>");
}
$(document).ready(function() {
    $("#tags").attr("id", "id_tags");
    $("#id_tags").change(updateSelectedList);
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
        },
        minchar:2
        });
});
