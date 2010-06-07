$(document).ready(function() {
    $(".thumbnail > div").html($("<img/>").attr({"src":$($(".thumbnail a")[0]).attr("href")}));
});
