function oyla( go_to ){
        in_ajax = 1;
        $.post(go_to);
        in_ajax = 0;
}


function oylae(goto_){
    if(in_ajax != 1){
        in_ajax = 1;
        if(vote == 0){ vote = -1; }
        $.post("/yenifikir/oyla/", {idea: id, vote: vote}, function(data){
            in_ajax = 0;
            if(data.substr(0,2) == "OK"){
                img_up = $('#img_' + id + '_1');
                img_down = $('#img_' + id + '_0');

                if (vote == 1){
                    img_up.attr("src", "/media/img/new/ideas_voted_1.png");
                    img_down.attr("src", "/media/img/new/ideas_vote_0.png");
                }

                if (vote == -1){
                    img_up.attr("src", "/media/img/new/ideas_vote_1.png");
                    img_down.attr("src", "/media/img/new/ideas_voted_0.png");
                }

                data = data.replace(/OK/, "")
                $('#vote'+id).html(data);
            }
        });
    }
}
