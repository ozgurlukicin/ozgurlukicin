function syncData(data) {
    if (data) {
    //remove non-existent
    $(".latest > .post").each(function(i) {
        if (data.indexOf(parseInt(this.id.replace("id","")))<0) {
            $(this).addClass("tohide");
        }
    });
    //insert new data
    $(data).each(function(i) {
        if ($(".latest").html().indexOf(parseInt(this.id.replace("id","")))<0) {
            $(this).addClass("newcomer");
            $(".latest").prepend(this);
        }
    });
    //now do animations
    $(".latest > .newcomer").slideDown();
    $(".latest > .newcomer").removeClass("newcomer");
    $(".tohide").slideUp("normal", function() {
        $(".tohide").remove();
    });
    }
    $(".ajaxloader").hide();
}
var t;
function updatePosts(delay) {
    var id = $(".latest > .post")[0].id.replace("id","");
    $(".ajaxloader").show();
    $.get("/forum/son-iletiler/"+id+"/", syncData);
    t = setTimeout("updatePosts(" + delay + ")", delay);
}
$(document).ready(function() {
    //get new posts every 30 seconds
    updatePosts(30000);
});
