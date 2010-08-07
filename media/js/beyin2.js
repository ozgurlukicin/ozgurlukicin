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
            if(data.substr(0,3) == "you"){
            }
            else{
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
            
            white_bar.hide();
            if ( yes_width != 0 ){
                green_bar.show();
                green_bar.attr("width", String(yes_width));}
            else { green_bar.hide(); }
            if ( notr_width != 0 ){
                yellow_bar.show();
                yellow_bar.attr("width", String(notr_width));}
            else { yellow_bar.hide(); }
            if ( no_width != 0 ){
                red_bar.show();
                red_bar.attr("width", String(no_width));}
            else { red_bar.hide(); }

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
                }});
        in_ajax = 0;
}

function yonetim(go_to, idea_id, func_to_do, from){
    in_ajax = 1;
        if (func_to_do == "mark_duplicate" ){
            original_idea_id = prompt("Asıl fikrin ID'sini girin:");
            if ( idea_id == original_idea_id ) { alert("Bir fikir kendisinin tekrarı olamaz.") }
            else{
            $.post(go_to, { dupple_number: original_idea_id}, function(data){
                header = $('#header_'+idea_id);
                div_left = $('#div_left_'+idea_id);
                div_middle = $('#div_middle_'+idea_id);
                div_right = $('#div_right_'+idea_id);
                header.text("FİKİR TEKRARI OLARAK BELİRLENDİ");
                div_left.hide("slow");
                div_right.hide("slow");
                div_middle.hide("slow");
                if (from == "detail" ){
                    window.location = "/beyin2/"; }
                else{
                original_idea_report_address = "/beyin2/report_"+original_idea_id+"/";
                re_draw_vote( original_idea_id, original_idea_report_address);}
                });
        }}
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
                    header.text("SİLİNDİ");
                    div_left.hide("slow");
                    div_right.hide("slow");
                    div_middle.hide("slow");
                if (from == "detail" ){
                    window.location = "/beyin2/"
                    }
                });
            }
        }
        else if ( func_to_do == "undelete_idea" ){
            is_confirmed = confirm('Bu fikri geri getirmek istediğinizden emin misiniz?');
            if ( is_confirmed ){
                $.post(go_to, function(data){
                    header = $('#header_'+idea_id);
                    div_left = $('#div_left_'+idea_id);
                    div_middle = $('#div_middle_'+idea_id);
                    div_right = $('#div_right_'+idea_id);
                    header.text("SİLİNDİ");
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
            status = $('#status_'+idea_id);
            $.post(go_to,{ category : category.val(), status : status.val() }, function(data){
                    current_category = $('#current_category_'+idea_id);
                    current_category.text(category.val());
                    current_category.show();
                    });
        }
        else if ( func_to_do == "status_change" ){
            status = $('#status_'+idea_id);
            category = $('#category_'+idea_id);
            $.post(go_to,{ status : status.val(), category : category.val() }, function(data){
                    current_status = $('#current_status_'+idea_id);
                    current_status.text(status.val());
                    });
        }
        in_ajax = 0;
}
function search_tags(go_to){
    in_ajax = 1;
    tags_list = $('#id_tags');
    title = $('#id_title');
    if ( tags_list.val() != null ){
        if ( tags_list.val()[5] == null ){
            if (title.val() != "" ){
                hiding_div = $('#hiding_div');
                hiding_div.hide();
                search_text = $('#searching');
                search_text.show();
                search_image = $('#searching_image');
                search_image.show();
                $.post(go_to,{tags : tags_list.val(), title : title.val()},function(data){
                    if(data.substr(0,10) == "EslesmeYok"){
                        form = $('#select_tags_form');
                        form.submit();}
                    else {
                        $('#top_bar_title').text( "Eklemek istediğini fikir, aşağıdakilerle ilgili mi?");
                        search_text.hide();
                        search_image.hide();
                        results = $('#results_list');
                        results.prepend(data);
                        $('#next_button').show();}
                });}
            else{
                alert("Lütfen geçerli bir başlık yazın.");}}
        else{
            alert("En fazla 5 etiket seçebilirsiniz.");}}
    else{
        alert("Lütfen en az 1 etiket seçin.");}
    in_ajax = 0;
}
function to_search_tags( go_to, evt){
    if ( evt.keyCode==13 || evt.which==13 ){
        search_tags(go_to);}
}

function add_new_idea(go_to){
    form = $('#select_tags_form');
    form.submit();
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



function is_favorite(idea_id,go_to){
    in_ajax = 1;
    $.post(go_to, function(data){
        yes_favorite = $('#yes_favorite_'+idea_id);
        no_favorite = $
        ('#no_favorite_'+idea_id);
        if(data.substr(0,2) == "NO"){
        yes_favorite.hide();
        no_favorite.show();
        }
        else if(data.substr(0,3) == "YES"){
            yes_favorite.show();
            no_favorite.hide();
        }
    });
    in_ajax = 0;
}

function add_remove_favorite(idea_id, go_to, favorite_go_to){
    in_ajax = 1;
    $.post(go_to, function(data){
        is_favorite(idea_id,favorite_go_to);
        });

}

function hide_by_id(element_id){
    element_to_hide = $( element_id );
    element_to_hide.hide();
}


function re_draw_vote(idea_id,go_to){
    $.post(go_to, function(data){
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

            if ( yes_width != 0 ){
                green_bar.show();
                green_bar.attr("width", String(yes_width));}
            else { green_bar.hide(); }
            if ( notr_width != 0 ){
                yellow_bar.show();
                yellow_bar.attr("width", String(notr_width));}
            else { yellow_bar.hide(); }
            if ( no_width != 0 ){
                red_bar.show();
                red_bar.attr("width", String(no_width));}
            else { red_bar.hide(); }

            vote_show = Math.round(vote_value/10.0);
            vote_count.text(vote_show);

            });
}

function remove_image(image_id,go_to){
    in_ajax = 1;
    $.post(go_to, function(data){
            link = $('#link_to_image_'+image_id);
            image = $('#image_'+image_id);
            remove_button = $('#remove_image_'+image_id);
            link.hide();
            image.hide();
            remove_button.hide();
            });
    in_ajax = 0;
}

function filter_ideas( url,tag_end){
    go_to = url.substr(0,(url.length-1));
    go_to = go_to+"__"+tag_end+"/";
    window.location = go_to;
}



function control_entry( dull ){
    tags_list = $('#id_tags');
    title = $('#id_ideaform-title');
    images = 0;
    if (title.val() != "" ){
        if  ( tinyMCE.get('id_ideaform-description').getContent() != "" ) {
            if ( tags_list.val() != null ){
                if ( tags_list.val()[5] == null ){
                    form = $('#add_new_idea');
                    for (i=0;i<3;i++){
                        image = document.getElementById("id_imageform-"+i+"-image");
                        if( image.value.lastIndexOf(".jpg")!=-1 ){ 
                            images += 1;}
                        if ( image.value.lastIndexOf(".png")!=-1 ){
                            images += 1;}
                        if ( image.value.lastIndexOf(".bmp")!=-1 ){
                            images += 1;}
                        if ( image.value == ""){
                            images += 1;}
                    }
                    if ( images == 3) {
                        form.submit();}
                    else {
                        alert (" eklediğiniz resimlerin uzantısı jpg, png yada bmp olmalıdır.");}
                }
                else{ alert("En fazla 5 etiket seçebilirsiniz."); }}
            else{ alert("Lütfen en az 1 etiket seçin."); }}
        else{ alert("Lütfen geçerli bir açıklama yazın."); }}
    else{ alert("Lütfen geçerli bir başlık yazın."); }
}

function control_entry_edit( dull ){
    tags_list = $('#id_tags');
    title = $('#id_ideaform-title');
    if (title.val() != "" ){
        if  ( tinyMCE.get('id_description').getContent() != "" ) {
            if ( tags_list.val() != null ){
                if ( tags_list.val()[5] == null ){
                    form = $('#edit_idea');
                    form.submit();}
                else{ alert("En fazla 5 etiket seçebilirsiniz."); }}
            else{ alert("Lütfen en az 1 etiket seçin."); }}
        else{ alert("Lütfen geçerli bir açıklama yazın."); }}
    else{ alert("Lütfen geçerli bir başlık yazın."); }
}   
