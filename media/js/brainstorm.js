function favori(id, proc) {
    $.get("/yenifikir/ayrinti/"+id+"/favori/"+proc,
        function(data) {
            if (data == 'OK') {
                if (proc == 'ekle') {
                    $('#favoriekle' + id).hide();
                    $('#favoricikar' + id).fadeIn();
                } else {
                    $('#favoricikar' + id).hide();
                    $('#favoriekle' + id).fadeIn();
                }
            }
        });
}
function oyla(id, vote) {
    $("#vote" + id + "_" + vote).html("<img src='/media/img/new/ideas_voted_"+vote+".png' />");
    $.get("/yenifikir/oyla/" + id + "/" + vote + "/",
        function(data) {
            $('#oyla' + id).hide()
            $('#oyiptal' + id).fadeIn("slow")
            if (data.substr(0,2)=='OK') {
                data = str.replace(/OK/, "")
                $('#vote' + id).html(data);
            } else {
                document.location = '/kullanici/giris/';
            }
        });

}
function oyiptal(id) {
    $.get("/yenifikir/oyiptal/" + id,
        function(data) {
            $('#oyiptal' + id).hide()
            $('#oyla' + id).fadeIn("slow")
            $('#vote' + id).html(data);
        });
}
function duplicate(idea_id) {
    $("dup_submit").attr("disabled","disabled");
    $.get("/yenifikir/tekrar/"+ idea_id +"/"+ $("#duplicate_id").val() +"/",
        function(data) {
            if (data == 'OK') {
                $("#duplicate_form_info").html("Tekrar bildiriminiz alındı, teşekkürler.");
            } else if (data == 'YOK') {
                $("#duplicate_form_info").html("Böyle bir fikir bulunamadı.");
            }
        });
}
function changeStatus(idea_id) {
    $.get("/yenifikir/durumdegistir/" + idea_id + "/" + $("#id_status").val()  + "/",
        function(data) {
            $("#status_form_info").html("Fikir durumu değiştirildi.")
        });
}






