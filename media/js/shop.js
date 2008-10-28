var current_product = 0;
function toggleBuyPopup() {
    var height = document.body.clientHeight;
    var width = document.body.clientWidth;
    $("#buymessage").css("left", width/2-152).css("top", height/2-112).toggle("slow");
}
function addToCart() {
    $.post("/dukkan/sepet/ekle/", { product_id: current_product, quantity: $('#quantity').val(), csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val() },
            function(data) {
                if (data=='OK') {
                    $.get('/dukkan/sepet/', function(data) { $('#cart').html(data); } );
                }
            });
    toggleBuyPopup();
}
function remove(item_id) {
    $.post("/dukkan/sepet/cikar/", { csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val(), item_id: item_id },
            function(data) {
                if (data=='OK') {
                    $.get('/dukkan/sepet/', function(data) { $('#cart').html(data); } );
                }
            });
}
function buyDialog(product_id) {
    current_product = product_id;
    toggleBuyPopup();
}
function swapImage(img) {
    document.big_image.src = img.childNodes[0].src;
}
