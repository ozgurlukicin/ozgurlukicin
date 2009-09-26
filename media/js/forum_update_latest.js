function syncData(data) {
    if (data) {
    //remove non-existent
    $(".latest > .post").each(function(i) {
        if (data.indexOf(this.id)<0) {
            $(this).addClass("tohide");
        }
    });
    //insert new data
    $(data).each(function(i) {
        if ($(".latest").html().indexOf(this.id)<0) {
            $(".latest").prepend($(this).parent().html());
            $(".latest > .post:first").hide();
        }
    });
    //now do animations
    $(".latest > .post").slideDown();
    $(".tohide").slideUp("normal", function() {
        $(".tohide").remove();
    });
    }
}
var t;
function updatePosts(delay) {
    var id = $(".latest > .post")[0].id;
    $.get("/forum/son-iletiler/"+id+"/", syncData);
    t = setTimeout("updatePosts(" + delay + ")", delay);
}
$(document).ready(function() {
    //get new posts every 20 seconds
    updatePosts(20000);
});
