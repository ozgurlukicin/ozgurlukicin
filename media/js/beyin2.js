function oyla(idea_id, go_to ){
        in_ajax = 1;
        $.post(go_to, function(data){
            vote_percent = data;
            yes_percent = parseInt(vote_percent/1000000.0);
            notr_percent = parseInt((vote_percent-yes_percent*1000000)/1000.0);
            no_percent = parseInt(((vote_percent-yes_percent*1000000)-notr_percent*1000));
            yes_width = yes_percent*54/100.0;
            notr_width = notr_percent*54/100.0;
            no_width = no_percent*54/100.0;
            white_bar = $('#white_bar_'+idea_id);
            green_bar = $('#green_bar_'+idea_id);
            yellow_bar = $('#yellow_bar_'+idea_id);
            red_bar = $('#red_bar_'+idea_id);

            white_bar.attr("width", "0");
            green_bar.attr("width", String(yes_width));
            yellow_bar.attr("width", String(notr_width));
            red_bar.attr("width", String(no_width));
            
                alert(data+"yes"+yes_percent+"notr"+notr_percent+"no"+no_percent);
                });
        in_ajax = 0;
}


function oylae(goto_,new_){
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
