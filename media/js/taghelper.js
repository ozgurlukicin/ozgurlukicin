function removeTag(tag, removeButton) {
    /* deselects given tag (as string) from select box and removes it from tag list */
    $("#id_tags > option:selected").each(function (index, option){
        if (option.innerHTML == tag)
            return option.selected = false;
    });
    $(removeButton).parent().fadeOut("fast", function(){ $(this).remove() });
}
function updateSelectedList() {
    /* cleans and fills tag list by looking at selected items in selectbox */
    var selected = "";
    $("#id_tags > option:selected").each(function(index, option) {
        var tag = option.innerHTML;
        selected = selected + "<div class=\"item\"><span class=\"tagName\">"+tag+"</span><span class=\"removeButton\" onclick=\"removeTag('"+tag+"', this)\">x</span></div>";
    });
    $("#selectedItems").remove();
    $("#id_tags").before("<div id=\"selectedItems\">"+selected+"</div>");
}
$(document).ready(function() {
    $("#tags").attr("id", "id_tags"); /* I'll use this on forum too, but it has tags instead of id_tags, that's why I'm modifying it */
    $("#id_tags").change(updateSelectedList);
    /* create a tag input field for filtering through tags */
    $("#id_tags").before("<input id=\"tagfilter\" class=\"vTextField\" type=\"text\" />");
    updateSelectedList();
    /* add autocompletion support to our tag input field, fills autocomplete list from the selectbox */
    $("#tagfilter").autocomplete({
        source:"#id_tags",
        onSelect:function(){
            /* select the given tag in selectbox and update tag list */
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
