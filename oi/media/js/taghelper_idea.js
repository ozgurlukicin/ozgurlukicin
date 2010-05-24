var smartTags = true;
function removeTag(tag, removeButton) {
    /* deselects given tag (as string) from select box and removes it from tag list */
    $("#tags > option:selected").each(function (index, option){
        if (option.innerHTML == tag)
            return option.selected = false;
    });
    $(removeButton).parent().fadeOut("fast", function(){ $(this).remove() });
}
function updateSelectedList() {
    /* cleans and fills tag list by looking at selected items in selectbox */
    var selected = "";
    $("#tags > option:selected").each(function(index, option) {
        var tag = option.innerHTML;
        selected = selected + "<div class=\"item\"><span class=\"tagName\">"+tag+"</span><span class=\"removeButton\" onclick=\"removeTag('"+tag+"', this)\">x</span></div>";
    });
    $("#selectedItems").remove();
    $("#taghelp").after("<div id=\"selectedItems\" style=\"margin-left:220px\">"+selected+"</div>");
}
function toggleTagMode() {
    if (smartTags) {
        smartTags = false;
        $("#tags, #add_tags, .help_text:last").show();
        $("#tagfilter, #selectedItems, #taghelp").hide();
    } else {
        smartTags = true;
        $("#tags, #add_tags, .help_text:last").hide();
        $("#tagfilter, #selectedItems, #taghelp").show();
    }
}
$(document).ready(function() {
    $("#tags").change(updateSelectedList);
    /* create a tag input field for filtering through tags */
    $("#tags, #add_tags, .help_text:last").hide();
    $(".help_text:last").before("<input id=\"tagfilter\" class=\"vTextField\" type=\"text\" /><p id=\"taghelp\" class=\"help_text\">Bir etiket adı yazıp Enter'a basın.</p>");
    $(".help_text:last").after("<a id=\"tagtoggle\" onclick=\"toggleTagMode();\" style=\"cursor:pointer;clear:both;float:left\">[Tüm Etiketleri Göster/Gizle]</a>");
    updateSelectedList();
    /* add autocompletion support to our tag input field, fills autocomplete list from the selectbox */
    $("#tagfilter").autocomplete({
        source:"#tags",
        onSelect:function(){
            /* select the given tag in selectbox and update tag list */
            options = $("#tags > option");
            var i = 0;
            while (i<options.length && options[i].innerHTML!=$("#tagfilter").val()) {
                i = i + 1;
            }
            options[i].selected = true;
            updateSelectedList();
            $("#tagfilter").val("");
        },
        minchar:2
        });
    /* fix css */
    $(".ac_conteiner").css({"margin-left":"0px", "float":"left", "width":"auto"});
    $("#selectedItems, #tagtoggle").css("margin-left","220px");
});
