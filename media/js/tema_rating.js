function rating_updated() {
    jQuery.get(rating_url,function(data){$("#themeitem_middle_stars_text").text(data);});
}
$(document).ready(function() {
    $(".rating").rating(rating_url, {maxvalue:5,curvalue:rating,increment:.5});
});
