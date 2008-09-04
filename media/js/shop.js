function addCart(product_id) {
    $.post("/dukkan/sepet/ekle/", { product_id: product_id, quantity: $('#quantity').val(), csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val() },
            function(data){
                if (data=='OK') {
                    $.get('/dukkan/sepet/', function(data) { $('#cart').html(data); } );
                }
            });
}
function remove(item_id) {
    $.post("/dukkan/sepet/cikar/", { csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val(), item_id: item_id },
            function(data) {
                if (data=='OK') {
                    $.get('/dukkan/sepet/', function(data) { $('#cart').html(data); } );
                }
            });
}
