var rating_loaded = false;
function submit_rating(value, link) {
    if (rating_loaded) $("#ratingform").submit();
}
$(document).ready(function() {
    $(".auto-submit-star").rating({callback: submit_rating});
    $(".auto-submit-star").rating("select", rating);
    $(".auto-submit-star").rating("readOnly", !is_authenticated);
    rating_loaded = true;
});
