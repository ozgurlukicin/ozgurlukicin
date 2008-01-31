window.addEvent('domready', function(){
    var szNormal = 120, szSmall  = 109, szFull   = 175;

    var kwicks = $$("#menu .menu");
    var fx = new Fx.Elements(kwicks, {wait: false, duration: 200, transition: Fx.Transitions.quadOut});

    kwicks.each(function(kwick, i) {
        kwick.addEvent("mouseenter", function(event) {
            var o = {};
            o[i] = {width: [kwick.getStyle("width").toInt(), szFull]}
            kwicks.each(function(other, j) {
                if(i != j) {
                    var w = other.getStyle("width").toInt();
                    if(w != szSmall) o[j] = {width: [w, szSmall]};
                }
            });
            fx.start(o);
        });
    });

    $("menu").addEvent("mouseleave", function(event) {
        var o = {};
        kwicks.each(function(kwick, i) {
            o[i] = {width: [kwick.getStyle("width").toInt(), szNormal]}
        });
        fx.start(o);
    });
});
