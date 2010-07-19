function oyla(idea_id, vote, go_to ){
        in_ajax = 1;
        $.post(go_to, function(data){
            /*
            if (data > 1000000000000000){
                data2 = data - 1000000000000000;
                vote_value = parseInt(data2/1000000000.0);
                data_work = data2 - (vote_value)*1000000000;
                vote_value = -1* vote_value;
            }
            else {
                vote_value = parseInt(data/1000000000.0);
                data_work = data - vote_value*1000000000;
            }*/
            data_list = data.split("_");
            vote_value = data_list[0];
            data_work = data_list[1];
            vote_percent = data_work;
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
            vote_count = $('#vote_count_'+idea_id);

            white_bar.attr("width", "0");
            green_bar.attr("width", String(yes_width));
            yellow_bar.attr("width", String(notr_width));
            red_bar.attr("width", String(no_width));

            vote_show = Math.round(vote_value/10.0);
            vote_count.text(vote_show);
            
            yes_arrow = $('#vote_yes_'+idea_id);
            yes_arrow_de = $('#vote_yes_'+idea_id+'_de');
            notr_arrow = $('#vote_notr_'+idea_id);
            notr_arrow_de = $('#vote_notr_'+idea_id+'_de');
            no_arrow = $('#vote_no_'+idea_id);
            no_arrow_de = $('#vote_no_'+idea_id+'_de');

            if ( vote == 1 ){
                yes_arrow_de.show();
                notr_arrow.show();
                no_arrow.show();
                
                yes_arrow.hide();
                notr_arrow_de.hide();
                no_arrow_de.hide();
                }
            if ( vote == 0 ){
                yes_arrow.show();
                notr_arrow_de.show();
                no_arrow.show();

                yes_arrow_de.hide();
                notr_arrow.hide();
                no_arrow_de.hide();
                }
            if ( vote == 2){
                yes_arrow.show();
                notr_arrow.show();
                no_arrow_de.show();

                yes_arrow_de.hide();
                notr_arrow_de.hide();
                no_arrow.hide();
                }

               // alert("data :"+data+"\ndata2 :"+data2+"\ndata_work :"+data_work+"\nvote_value"+vote_value+"\nyes    :"+yes_percent+"\nnotr    :"+notr_percent+"\nno    :"+no_percent);
                });
        in_ajax = 0;
}

function yonetim(go_to, idea_id, func_to_do, from){
    in_ajax = 1;
        if (func_to_do == "mark_duplicate" ){
            original_idea_id = prompt("please enter the original ideas id number");
            $.post(go_to, { dupple_number: original_idea_id}, function(data){
                header = $('#header_'+idea_id);
                div_left = $('#div_left_'+idea_id);
                div_middle = $('#div_middle_'+idea_id);
                div_right = $('#div_right_'+idea_id);
                header.text("THIS IDEA IS MARKED DUPLICATE");
                div_left.hide("slow");
                div_right.hide("slow");
                div_middle.hide("slow");
                if (from == "detail" ){
                    window.location = "/beyin2/"
                    }
                });
        }
        else if ( func_to_do == "edit_idea" ){
            window.location = go_to
        }
        else if ( func_to_do == "delete_idea" ){
            is_confirmed = confirm('Bu fikri silmek istediğinizden emin misiniz?');
            if ( is_confirmed ){
                $.post(go_to, function(data){
                    header = $('#header_'+idea_id);
                    div_left = $('#div_left_'+idea_id);
                    div_middle = $('#div_middle_'+idea_id);
                    div_right = $('#div_right_'+idea_id);
                    header.text("THIS IDEA IS REMOVED");
                    div_left.hide("slow");
                    div_right.hide("slow");
                    div_middle.hide("slow");
                if (from == "detail" ){
                    window.location = "/beyin2/"
                    }
                });
            }
        }
        else if ( func_to_do == "category_change" ){
            category = $('#category_'+idea_id);
            $.post(go_to,{ category : category.val()}, function(data){
                    current_category = $('#current_category_'+idea_id);
                    current_category.text(category.val());
                    });
        }
        else if ( func_to_do == "status_change" ){
            status = $('#status_'+idea_id);
            $.post(go_to,{ status : status.val()}, function(data){
                    current_status = $('#current_status_'+idea_id);
                    current_status.text(status.val());
                    });
        }
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
