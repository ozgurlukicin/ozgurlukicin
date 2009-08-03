function submit_rating(value, link) {
    alert(value);
}
$(document).ready(function() {
    $(".temastar").rating("select", rating);
    $(".temastar").rating("readOnly", !is_authenticated);
    $(".temastar").rating({callback: submit_rating});
});
