$(window).load(function () {
    var hldr = $("#holder");
    var text = $("p", hldr).html();
    hldr.html("");
    var R = Raphael("holder", 640, 480);
    var txt = [];
    var attr = {font: '50px Fontin-Sans, Arial', opacity: 0.5};
    txt[0] = R.text(320, 240, text).attr(attr).attr({fill: "#0f0"});
    txt[1] = R.text(320, 240, text).attr(attr).attr({fill: "#f00"});
    txt[2] = R.text(320, 240, text).attr(attr).attr({fill: "#00f"});
    var mouse = null, rot = 0;
    $(document).mousemove(function (e) {
        if (mouse === null) {
            mouse = e.pageX;
            return;
        }
        rot += e.pageX - mouse;
        txt[0].rotate(rot, true);
        txt[1].rotate(rot / 1.5, true);
        txt[2].rotate(rot / 2, true);
        mouse = e.pageX;
        R.safari();
    });
});