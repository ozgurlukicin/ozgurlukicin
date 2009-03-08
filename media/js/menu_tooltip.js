//
// Js for tooltip on everypage, see menu.html
//

$(function(){
        $("#menu a").tooltip({
            delay: 500,
            track: true,
            showURL: false,
            fade: 350
        });
    // Tooltip for forum
        $(".topic_title a").tooltip({
            delay: 0,
            track: true,
            showURL: false,
            extraClass: "pretty",
            fade: 330,
            left: 20,
            top: -10
        });
    });
