

var world = {rows:10, columns:12};
var margins = {top:20, bottom:50, left:50, right:30, left_text:35, bottom_text:25};

var dimensions = {narrow:6, wide:34};
dimensions.tile_size = dimensions.narrow + dimensions.wide;
dimensions.width = (world.columns+1) * dimensions.tile_size + margins.left + margins.right;
dimensions.height = world.rows * dimensions.tile_size + margins.top + margins.bottom;

var colours = {inactive: "white",
               inactive_edit: "#eef",
               active: "brown",
               active_hover: "black",
               inactive_hover: "grey",
               border_active: "black",
               border_inactive: "white"
               }

var flip_rows = function(row){
    return world.rows - row;
}

Raphael.fn.east_wall = function(col, row){
    this.active = false;
    this.x = (col+1)*dimensions.tile_size + margins.left;
    this.y = (flip_rows(row)-1)*dimensions.tile_size + margins.top;
    this.width = dimensions.narrow;
    this.height = dimensions.wide + 2*dimensions.narrow;
    return this.rect(this.x, this.y, this.width, this.height).attr({fill:colours.inactive, stroke:colours.border_inactive});
}

Raphael.fn.north_wall = function(col, row){
    this.active = false;
    this.x = col*dimensions.tile_size + margins.left;
    this.y = (flip_rows(row)-1)*dimensions.tile_size + margins.top;
    this.width = dimensions.wide + 2*dimensions.narrow;
    this.height = dimensions.narrow;
    return this.rect(this.x, this.y, this.width, this.height).attr({fill:colours.inactive, stroke:colours.border_inactive});
}


var EastWalls = new Array(world.rows);
for(var row = 0; row < world.rows; row++){
    EastWalls[row] = new Array(world.columns)
}

var NorthWalls = new Array(world.rows);
for(var row = 0; row < world.rows; row++){
    NorthWalls[row] = new Array(world.columns)
}


Raphael.fn.edit_button = function(){
    return this.rect(0, 0, 20, 20).attr({fill:"red"});
}


$(window).load(function () {
    var R = Raphael("World", dimensions.width, dimensions.height);

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
                    this.attr({fill: colours.inactive_hover, stroke: colours.border_inactive});
                    this.active = false;
                    this.toBack();
                }
                else{
                    this.attr({fill: colours.active, stroke: colours.border_active});
                    this.active = true;
                    this.toFront();
                }
            }
        });
        this.square.hover( function (event) {
                            if(edit_button.edit){
                                if(this.active){
                                    this.attr({fill: colours.active_hover})
                                }
                                else{
                                    this.toFront();
                                    this.attr({fill: colours.inactive_hover})
                                }
                            }
                        },
                        function (event) {
                            if(edit_button.edit){
                                if(this.active){
                                    this.attr({fill: colours.active})
                                }
                                else{
                                    this.attr({fill: colours.inactive_edit})
                                    this.toBack();
                                }
                            }
                        }
                    );
        return this.square;
    }
    for(var row=0; row < world.rows; row++){
        for(var col=0; col < world.columns; col++){
            EastWalls[row][col] = create_wall(col, row, "east");
            NorthWalls[row][col] = create_wall(col, row, "north");
        }
    }

    edit_button.click( function(){
        if(!this.edit){
            this.edit = true;
            for(var row=0; row < world.rows; row++){
                for(var col=0; col < world.columns; col++){
                    if(!EastWalls[row][col].active){
                        EastWalls[row][col].attr({fill: colours.inactive_edit})
                    }
                    if(!NorthWalls[row][col].active){
                        NorthWalls[row][col].attr({fill: colours.inactive_edit})
                    }
                }
            }
        }
        else{
            this.edit = false;
            for(var row=0; row < world.rows; row++){
                for(var col=0; col < world.columns; col++){
                    if(!EastWalls[row][col].active){
                        EastWalls[row][col].attr({fill: colours.inactive})
                    }
                    if(!NorthWalls[row][col].active){
                        NorthWalls[row][col].attr({fill: colours.inactive})
                    }
                }
            }
        }
    })


    // grid lines and borders drawn last so that they supercede the other walls
    var end_x = world.columns*dimensions.tile_size + margins.left;
    var end_y = world.rows*dimensions.tile_size + margins.top + dimensions.narrow;
    for(var row=0; row < world.rows; row++){
        var _y = row*dimensions.tile_size + dimensions.tile_size/2 + margins.top + dimensions.narrow;
        R.path("M" + margins.left +" "+ _y + "L" + end_x + " " + _y).attr({stroke: "#666", "stroke-dasharray": ". "});
        R.text(margins.left_text, _y, row+1);
        }
    for(var col=0; col < world.columns; col++){
        var _x = col*dimensions.tile_size + dimensions.tile_size/2 + margins.left + dimensions.narrow;
        R.path("M" + _x +" "+ margins.top + "L" + _x + " " + end_y).attr({stroke: "#666", "stroke-dasharray": ". "});
        R.text(_x, dimensions.height - margins.bottom_text, col+1);
    }

    var left_border = R.rect(margins.left,
                             margins.top,
                             dimensions.narrow,
                             world.rows*dimensions.tile_size + 2*dimensions.narrow).attr({fill:colours.active});
    var bottom_border = R.rect(margins.left,
                               margins.top + world.rows*dimensions.tile_size + dimensions.narrow,
                               world.columns*dimensions.tile_size + dimensions.narrow,
                               dimensions.narrow).attr({fill:colours.active});
    var right_border = R.rect(margins.left + world.columns*dimensions.tile_size,
                             margins.top,
                             dimensions.narrow,
                             world.rows*dimensions.tile_size + 2*dimensions.narrow).attr({fill:colours.active});
    var top_border = R.rect(margins.left,
                               margins.top,
                               world.columns*dimensions.tile_size + dimensions.narrow,
                               dimensions.narrow).attr({fill:colours.active});


});
