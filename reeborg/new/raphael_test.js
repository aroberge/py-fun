
function Parameters(){
    this.margin_top = 20;
    this.margin_bottom = 50;
    this.margin_left = 50;
    this.margin_right = 30;
    this.margin_left_text = 35;
    this.margin_bottom_text = 25;
    this.narrow = 6;
    this.wide = 34;
    this.tile_size = this.narrow + this.wide;

    this.colours = {inactive: "white",
                    inactive_edit: "#eef",
                    active: "brown",
                    active_hover: "black",
                    inactive_hover: "grey",
                    border_active: "black",
                    border_inactive: "white",
                    background: "white"
    }

    this.init = function(rows, columns){
        if(rows != undefined){
            this.rows = rows;
        }
        else{
            this.rows = 10;
        }
        if(columns != undefined){
            this.columns = columns;
        }
        else{
            this.columns = 10;
        }
        this.world_width = this.columns * this.tile_size + this.margin_left + this.margin_right + this.narrow;
        this.world_height = this.rows * this.tile_size + this.margin_bottom + this.margin_top;
    }
}

var params = new Parameters();
params.init();

var flip_rows = function(row){
    return params.rows - row;
}

Raphael.fn.east_wall = function(col, row){
    this.active = false;
    this.x = (col+1)*params.tile_size + params.margin_left;
    this.y = (flip_rows(row)-1)*params.tile_size + params.margin_top;
    this.width = params.narrow;
    this.height = params.wide + 2*params.narrow;
    return this.rect(this.x, this.y, this.width, this.height).attr({fill:params.colours.inactive, stroke:params.colours.border_inactive});
}
Raphael.fn.north_wall = function(col, row){
    this.active = false;
    this.x = col*params.tile_size + params.margin_left;
    this.y = (flip_rows(row)-1)*params.tile_size + params.margin_top;
    this.width = params.wide + 2*params.narrow;
    this.height = params.narrow;
    return this.rect(this.x, this.y, this.width, this.height).attr({fill:params.colours.inactive, stroke:params.colours.border_inactive});
}

var EastWalls = new Array(params.rows);
for(var row = 0; row < params.rows; row++){
    EastWalls[row] = new Array(params.columns)
}

var NorthWalls = new Array(params.rows);
for(var row = 0; row < params.rows; row++){
    NorthWalls[row] = new Array(params.columns)
}


Raphael.fn.edit_button = function(){
    return this.rect(0, 0, 20, 20).attr({fill:"red"});
}

function create_background(paper){
    return paper.rect(0, 0, params.world_width, params.world_height).attr({fill: params.colours.background});
}


$(window).load(function () {
    var R = Raphael("World", params.world_width, params.world_height);
    var background = create_background(R);

    var edit_button = R.edit_button();
    edit_button.edit = false;

    var create_wall = function(col, row, orientation){
        if(orientation == "east"){
            this.square = R.east_wall(col, row);
        }
        else{
            this.square = R.north_wall(col, row);
        }
        this.square.click( function () {
            if(edit_button.edit){
                if(this.active){
                    this.attr({fill: params.colours.inactive_hover, stroke: params.colours.border_inactive});
                    this.active = false;
                    this.toBack();
                    background.toBack();
                }
                else{
                    this.attr({fill: params.colours.active, stroke: params.colours.border_active});
                    this.active = true;
                    this.toFront();
                }
            }
        });
        this.square.hover( function (event) {
                            if(edit_button.edit){
                                if(this.active){
                                    this.attr({fill: params.colours.active_hover})
                                }
                                else{
                                    this.toFront();
                                    this.attr({fill: params.colours.inactive_hover})
                                }
                            }
                        },
                        function (event) {
                            if(edit_button.edit){
                                if(this.active){
                                    this.attr({fill: params.colours.active})
                                }
                                else{
                                    this.attr({fill: params.colours.inactive_edit})
                                    this.toBack();
                                    background.toBack();
                                }
                            }
                        }
                    );
        return this.square;
    }
    for(var row=0; row < params.rows; row++){
        for(var col=0; col < params.columns; col++){
            EastWalls[row][col] = create_wall(col, row, "east");
            NorthWalls[row][col] = create_wall(col, row, "north");
        }
    }

    edit_button.click( function(){
        if(!this.edit){
            this.edit = true;
            for(var row=0; row < params.rows; row++){
                for(var col=0; col < params.columns; col++){
                    if(!EastWalls[row][col].active){
                        EastWalls[row][col].attr({fill: params.colours.inactive_edit})
                    }
                    if(!NorthWalls[row][col].active){
                        NorthWalls[row][col].attr({fill: params.colours.inactive_edit})
                    }
                }
            }
        }
        else{
            this.edit = false;
            for(var row=0; row < params.rows; row++){
                for(var col=0; col < params.columns; col++){
                    if(!EastWalls[row][col].active){
                        EastWalls[row][col].attr({fill: params.colours.inactive})
                    }
                    if(!NorthWalls[row][col].active){
                        NorthWalls[row][col].attr({fill: params.colours.inactive})
                    }
                }
            }
        }
    })


    // grid lines and borders drawn last so that they supercede the other walls
    var end_x = params.columns*params.tile_size + params.margin_left;
    var end_y = params.rows*params.tile_size + params.margin_top + params.narrow;
    for(var row=0; row < params.rows; row++){
        var _y = row*params.tile_size + params.tile_size/2 + params.margin_top + params.narrow;
        R.path("M" + params.margin_left +" "+ _y + "L" + end_x + " " + _y).attr({stroke: "#666", "stroke-dasharray": ". "});
        R.text(params.margin_left_text, _y, row+1);
        }
    for(var col=0; col < params.columns; col++){
        var _x = col*params.tile_size + params.tile_size/2 + params.margin_left + params.narrow;
        R.path("M" + _x +" "+ params.margin_top + "L" + _x + " " + end_y).attr({stroke: "#666", "stroke-dasharray": ". "});
        R.text(_x, params.world_height - params.margin_bottom_text, col+1);
    }

    var left_border = R.rect(params.margin_left,
                             params.margin_top,
                             params.narrow,
                             params.rows*params.tile_size + 2*params.narrow).attr({fill:params.colours.active});
    var bottom_border = R.rect(params.margin_left,
                               params.margin_top + params.rows*params.tile_size + params.narrow,
                               params.columns*params.tile_size + params.narrow,
                               params.narrow).attr({fill:params.colours.active});
    var right_border = R.rect(params.margin_left + params.columns*params.tile_size,
                             params.margin_top,
                             params.narrow,
                             params.rows*params.tile_size + 2*params.narrow).attr({fill:params.colours.active});
    var top_border = R.rect(params.margin_left,
                               params.margin_top,
                               params.columns*params.tile_size + params.narrow,
                               params.narrow).attr({fill:params.colours.active});

    var robot_e = R.image("../images/robot_e.png", 185, 190, 22, 30);
    var robot_w = R.image("../images/robot_w.png", 225, 190, 22, 30);
    var robot_n = R.image("../images/robot_n.png", 265, 190, 22, 30);
    var robot_s = R.image("../images/robot_s.png", 305, 190, 22, 30);

});
