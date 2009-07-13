$(document).ready(function() {
    $("#id_number_of_cds,#id_reason,#id_company").parent().parent().hide();
    $("#specialform").click(function() {
        $("#id_number_of_cds,#id_reason,#id_company").parent().parent().toggle();
    });
});
