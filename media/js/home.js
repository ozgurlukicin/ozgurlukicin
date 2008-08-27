$(document).ready(function() {
            setInterval(function () {
                if ($("#news_count").html() == '5') {
                    goFirst();
                } else {
                        next_news()
                }
            }, 10000)
        });

function next_news() {
    $(".active").hide();
    $("#news_count").html(parseInt($("#news_count").html()) + 1);
    if ($("#news_count").html() == '6') goFirst();
    $(".active").next().addClass("active");
    $(".active:first").removeClass("active");
    $(".active").fadeIn();
}
function prev_news() {
    $("#news_count").html(parseInt($("#news_count").html()) - 1);
    if ($("#news_count").html() == '') goLast();
    $(".active").hide();
    $(".active").prev().addClass("active");
    $(".active:last").removeClass("active");
    $(".active").fadeIn();
}
function goFirst() {
    $("#news_count").html('1');
    $(".active").hide();
    $(".active").removeClass("active");
    $(".news_container:first").addClass("active");
    $(".active").fadeIn();
}

function goLast() {
    $("#news_count").html('5');
    $(".news_container").hide();
    $(".active").removeClass("active");
    $(".news_container:last").addClass("active");
    $(".active").fadeIn();
}
