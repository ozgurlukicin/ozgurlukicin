var intval=""
$(function() {
    intval = setInterval(function () {
        change_news(1);
    }, 10000)
});
var current_news = 0;
var news_count = 5;
$(document).ready(function() {
    news_count = $(".news_container").length;
});
function select_news(i) {
    $("#news_count>img").attr("src", "/media/img/new/news_progress.png");
    $("#news_count>img:eq("+i+")").attr("src", "/media/img/new/news_progress_selected.png");
};
function change_news(direction) {
    $("#news_" + current_news).hide();
    current_news = (current_news+direction) % news_count;
    $("#news_" + current_news).fadeIn();
    select_news(current_news);
}
function direct_select(i) {
    $("#news_" + current_news).hide();
    current_news = i;
    $("#news_" + current_news).fadeIn();
    select_news(current_news);
}
