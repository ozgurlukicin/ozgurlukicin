$(document).ready(function() {
    $(".searchresults ul").toggle();
    $(".searchresults ul:first").show();
    $(".searchresults > div").each(function (index, div){
        $(div).find(".title").append("<img src=\"/media/img/new/button_toggle.png\" alt=\"[Gizle/Göster]\" />");
        $(div).find(".title").click(function(){$("." + $(div).attr("class") + " ul").toggle();});
    });
});
