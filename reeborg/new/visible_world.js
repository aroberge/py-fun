

Raphael.fn.wall = function(x, y, width, height){
    this.active = false;
    return this.rect(x, y, width, height);
}

Raphael.fn.button = function(){
    return this.rect(0, 0, 20, 20);
}

function Controls(world){
    this.edit_button = world.paper.button().attr({x:10, y:0, fill:"red", title:"edit"});
    this.move_button = world.paper.button().attr({x:40, y:0, fill:"green", title:"move"});
    this.turn_left_button = world.paper.button().attr({x:70, y:0, fill:"blue", title:"turn_left"});
    this.change_robot = world.paper.button().attr({x:100, y:0, fill:"yellow", title:"change robot"});

    this.edit_button.click( function(){
        if(!this.edit){
            this.edit = true;
            for(var row=0; row < world.rows; row++){
                for(var col=0; col < world.columns; col++){
                    if(!world.east_walls[row][col].active){
                        world.east_walls[row][col].attr({fill: world.colours.inactive_edit})
                    }
                    if(!world.north_walls[row][col].active){
                        world.north_walls[row][col].attr({fill: world.colours.inactive_edit})
                    }
                }
            }
        }
        else{
            this.edit = false;
            for(var row=0; row < world.rows; row++){
                for(var col=0; col < world.columns; col++){
                    if(!world.east_walls[row][col].active){
                        world.east_walls[row][col].attr({fill: world.colours.inactive})
                    }
                    if(!world.north_walls[row][col].active){
                        world.north_walls[row][col].attr({fill: world.colours.inactive})
                    }
                }
            }
        }
    });

    this.move_button.click( function(){
        world.robot_move();
    })

    this.turn_left_button.click( function(){
        world.robot.turn_left();
    })

    this.change_robot.click( function(){
        world.robot.change_robot();
    })

}


function VisibleRobot(world){

    this.width = 22;
    this.height = 30;
    this.row = 0;
    this.column = 0;
    this.offset_x = world.margin_left + (world.narrow + world.tile_size - this.width)/2;
    this.offset_y = world.world_height - world.margin_bottom - this.height;
    this.style = "classic";
    this.angle = 0;
    this.x = 0;
    this.y = 0;

    this.robot = {
        "east": world.paper.image("../images/robot_e.png", 0, 0, this.width, this.height).hide(),
        "west": world.paper.image("../images/robot_w.png", 0, 0, this.width, this.height).hide(),
        "north": world.paper.image("../images/robot_n.png", 0, 0, this.width, this.height).hide(),
        "south": world.paper.image("../images/robot_s.png", 0, 0, this.width, this.height).hide(),
        "ellipse": world.paper.ellipse(0, 0, 15, 8).attr({'stroke-width': 0, fill: "r(0.90, 0.5)#fff-#0a3:70-#000"}).hide()
    }
    this.current = this.robot["east"];
    this.current_orientation = "east";

    this.change_robot = function(){
        if (this.style == "classic"){
            this.style = "ellipse";
            this.x += 11;
            this.y += 13;
            this.current.hide()
            this.current = this.robot["ellipse"].attr({cx:this.x, cy:this.y}).rotate(this.angle, true).show();
        }
        else{
            this.style = "classic";
            this.x -= 11;
            this.y -= 13;
            this.current.hide();
            this.current = this.robot[this.current_orientation].attr({x:this.x, y:this.y}).show();
        }
    }

    this.teleport = function(column, row){
        this.x = this.offset_x + (row-1)*world.tile_size;
        this.y = this.offset_y + (column-1)*world.tile_size;
        this.row = row;
        this.column = column;
        this.current.attr({x:this.x, y:this.y}).show();
    }

    this.move = function(del_col, del_row){
        this.column += del_col;
        this.row += del_row;
        this.x += del_col*world.tile_size;
        this.y -= del_row*world.tile_size;
        if(this.style == "classic"){
            this.current.animate({x: this.x, y: this.y}, 500);
        }
        else{
            this.current.animate({cx: this.x, cy: this.y}, 500);
        }
    }

    this.turn_left = function(){
        this.angle -= 90;
        switch(this.current_orientation){
            case "east": {
                this.current_orientation = "north";
                break;
            }
            case "north": {
                this.current_orientation = "west";
                break;
            }
            case "west": {
                this.current_orientation = "south";
                break;
            }
            case "south": {
                this.current_orientation = "east";
                break;
            }
        }
        if(this.style == "classic"){
            this.current.hide();
            this.current = this.robot[this.current_orientation].attr({x: this.x, y: this.y}).show();
        }
        else{
            this.current.animate({rotation: this.angle}, 150);
        }
    }

}


function VisibleWorld(){
    this.margin_top = 40;
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

        this.east_walls = new Array(this.rows);
        for(var row = 0; row < this.rows; row++){
            this.east_walls[row] = new Array(this.columns)
        }

        this.north_walls = new Array(this.rows);
        for(var row = 0; row < this.rows; row++){
            this.north_walls[row] = new Array(this.columns)
        }
    }


    this.create_east_wall = function(col, row){
        x = (col+1)*this.tile_size + this.margin_left;
        y = (this.flip_rows(row)-1)*this.tile_size + this.margin_top;
        width = this.narrow;
        height = this.wide + 2*this.narrow;
        return this.paper.wall(x, y, width, height).attr({fill:this.colours.inactive, stroke:this.colours.border_inactive});
    }

    this.create_north_wall = function(col, row){
        x = col*this.tile_size + this.margin_left;
        y = (this.flip_rows(row)-1)*this.tile_size + this.margin_top;
        width = this.wide + 2*this.narrow;
        height = this.narrow;
        return this.paper.wall(x, y, width, height).attr({fill:this.colours.inactive, stroke:this.colours.border_inactive});
    }

    this.create_wall = function(col, row, orientation){
        that = this;
        if(orientation == "east"){
            this._wall = this.create_east_wall(col, row);
        }
        else{
            this._wall = this.create_north_wall(col, row);
        }
        this._wall.click( function () {
            if(that.controls.edit_button.edit){
                if(this.active){
                    this.attr({fill: that.colours.inactive_hover, stroke: that.colours.border_inactive});
                    this.active = false;
                    this.toBack();
                    that.background.toBack();
                }
                else{
                    this.attr({fill: that.colours.active, stroke: that.colours.border_active});
                    this.active = true;
                    this.toFront();
                }
            }
        });
        this._wall.hover(
            function (event) {
                if(that.controls.edit_button.edit){
                    if(this.active){
                        this.attr({fill: that.colours.active_hover})
                    }
                    else{
                        this.toFront();
                        this.attr({fill: that.colours.inactive_hover})
                    }
                }
            },
            function (event) {
                if(that.controls.edit_button.edit){
                    if(this.active){
                        this.attr({fill: that.colours.active})
                    }
                    else{
                        this.attr({fill: that.colours.inactive_edit})
                        this.toBack();
                        that.background.toBack();
                    }
                }
        });
        return this._wall;
    }

    this.create_background = function(){
        this.background = this.paper.rect(0, 0, this.world_width, this.world_height).attr({fill: this.colours.background}).toBack();
    }

    this.flip_rows = function(row){
        return this.rows - row;
    }

    this.create_borders = function(){
        this.left_border = this.paper.rect(this.margin_left,
                             this.margin_top,
                             this.narrow,
                             this.rows*this.tile_size + this.narrow).attr({fill:this.colours.active});
        this.bottom_border = this.paper.rect(this.margin_left,
                               this.margin_top + this.rows*this.tile_size,
                               this.columns*this.tile_size + this.narrow,
                               this.narrow).attr({fill:this.colours.active});
        this.right_border = this.paper.rect(this.margin_left + this.columns*this.tile_size,
                             this.margin_top,
                             this.narrow,
                             this.rows*this.tile_size + this.narrow).attr({fill:this.colours.active});
        this.top_border = this.paper.rect(this.margin_left,
                               this.margin_top,
                               this.columns*this.tile_size + this.narrow,
                               this.narrow).attr({fill:this.colours.active});
    }

    this.create_grid = function(){
        var end_x = this.columns*this.tile_size + this.margin_left;
        var end_y = this.rows*this.tile_size + this.margin_top + this.narrow/2;
        var start_y = this.margin_top + this.narrow/2;
        var start_x = this.margin_left + this.narrow/2;
        for(var row=0; row < this.rows; row++){
            var _y = row*this.tile_size + this.tile_size/2 + this.margin_top + this.narrow/2;
            this.paper.path("M" + start_x +" "+ _y + "L" + end_x + " " + _y).attr({stroke: "#666", "stroke-dasharray": ". "});
            this.paper.text(this.margin_left_text, _y, row+1);
            }
        for(var col=0; col < this.columns; col++){
            var _x = col*this.tile_size + this.tile_size/2 + this.margin_left + this.narrow/2;
            this.paper.path("M" + _x +" "+ start_y + "L" + _x + " " + end_y).attr({stroke: "#666", "stroke-dasharray": ". "});
            this.paper.text(_x, this.world_height - this.margin_bottom_text, col+1);
        }
    }

    this.render = function() {
        if(this.controls === undefined){
            this.controls = new Controls(this);
        }
        for(var row=0; row < this.rows; row++){
            for(var col=0; col < this.columns; col++){
                this.east_walls[row][col] = this.create_wall(col, row, "east");
                this.north_walls[row][col] = this.create_wall(col, row, "north");
            }
        }
        this.create_background();
        this.create_borders();
        this.create_grid();
        if(this.robot === undefined){
            this.robot = new VisibleRobot(this);
            this.robot.teleport(1, 1);
        }
    }

    this.robot_move = function(){
        switch(this.robot.current_orientation){
            case "east": {
                del_row = 0;
                del_col = 1;
                break;
            }
            case "north": {
                del_row = 1;
                del_col = 0;
                break;
            }
            case "west": {
                del_row = 0;
                del_col = -1;
                break;
            }
            case "south": {
                del_row = -1;
                del_col = 0;
                break;
            }
        }
        new_row = this.robot.row + del_row;
        new_col = this.robot.column + del_col;
        if( new_row > 0 && new_row <= this.rows &&
           new_col > 0 && new_col <= this.columns){
            this.robot.move(del_col, del_row);
        }
    }

}


$(window).load(function () {
    var visible_world = new VisibleWorld();
    visible_world.init(8, 12);
    visible_world.paper = Raphael("World", visible_world.world_width, visible_world.world_height);
    visible_world.render();




});
