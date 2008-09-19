var intval=""
$(function() {
            intval = setInterval(function () {
                change_news(1)
            }, 10000)
        });

function change_news(direction) {
    nc = $("#news_count").html();
    $("#news_" + nc).hide();
    if (nc == '1' && direction == -1) nc = 6;
    if (nc == '5' && direction == 1) nc = 0;
    nc = parseInt(nc) + direction;
    $("#news_" + nc).fadeIn();
    $("#news_count").html(nc);
}
