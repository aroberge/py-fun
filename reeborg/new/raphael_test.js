var world = Object();
world.width = 640;
world.height = 480;

$(window).load(function () {
    var R = Raphael("World", world.width+1, world.height+1);
    R.rect(0, 0, world.width, world.height).attr({stroke: "black"});
    var walls = []
    for (i=0; i <= 10; i++){
        x = i*10;
        y = i*10;
        width = 8;
        height = 8;
        walls.push(R.rect(x, y, width, height).attr({stroke: "red"}));
        };
});
