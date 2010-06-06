

Raphael.fn.wall = function(x, y, width, height){
    this.active = false;
    return this.rect(x, y, width, height);
}

Raphael.fn.edit_button = function(){
    return this.rect(0, 0, 20, 20).attr({fill:"red"});
}
function VisibleWorld(){
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
            if(that.edit_button.edit){
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
                if(that.edit_button.edit){
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
                if(that.edit_button.edit){
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
                             this.rows*this.tile_size + 2*this.narrow).attr({fill:this.colours.active});
        this.bottom_border = this.paper.rect(this.margin_left,
                               this.margin_top + this.rows*this.tile_size + this.narrow,
                               this.columns*this.tile_size + this.narrow,
                               this.narrow).attr({fill:this.colours.active});
        this.right_border = this.paper.rect(this.margin_left + this.columns*this.tile_size,
                             this.margin_top,
                             this.narrow,
                             this.rows*this.tile_size + 2*this.narrow).attr({fill:this.colours.active});
        this.top_border = this.paper.rect(this.margin_left,
                               this.margin_top,
                               this.columns*this.tile_size + this.narrow,
                               this.narrow).attr({fill:this.colours.active});
    }

    this.create_grid = function(){
        var end_x = this.columns*this.tile_size + this.margin_left;
        var end_y = this.rows*this.tile_size + this.margin_top + this.narrow;
        for(var row=0; row < this.rows; row++){
            var _y = row*this.tile_size + this.tile_size/2 + this.margin_top + this.narrow;
            this.paper.path("M" + this.margin_left +" "+ _y + "L" + end_x + " " + _y).attr({stroke: "#666", "stroke-dasharray": ". "});
            this.paper.text(this.margin_left_text, _y, row+1);
            }
        for(var col=0; col < this.columns; col++){
            var _x = col*this.tile_size + this.tile_size/2 + this.margin_left + this.narrow;
            this.paper.path("M" + _x +" "+ this.margin_top + "L" + _x + " " + end_y).attr({stroke: "#666", "stroke-dasharray": ". "});
            this.paper.text(_x, this.world_height - this.margin_bottom_text, col+1);
        }
    }

    this.render = function() {
        this.edit_button = this.paper.edit_button();
        for(var row=0; row < this.rows; row++){
            for(var col=0; col < this.columns; col++){
                this.east_walls[row][col] = this.create_wall(col, row, "east");
                this.north_walls[row][col] = this.create_wall(col, row, "north");
            }
        }
        this.create_background();
        this.edit_button.toFront();
        this.create_borders();
        this.create_grid();
        this.enable_button();
    }

    this.enable_button = function(){
        that = this;
        that.edit_button.click( function(){
            if(!this.edit){
                this.edit = true;
                for(var row=0; row < that.rows; row++){
                    for(var col=0; col < that.columns; col++){
                        if(!that.east_walls[row][col].active){
                            that.east_walls[row][col].attr({fill: that.colours.inactive_edit})
                        }
                        if(!that.north_walls[row][col].active){
                            that.north_walls[row][col].attr({fill: that.colours.inactive_edit})
                        }
                    }
                }
            }
            else{
                this.edit = false;
                for(var row=0; row < that.rows; row++){
                    for(var col=0; col < that.columns; col++){
                        if(!that.east_walls[row][col].active){
                            that.east_walls[row][col].attr({fill: that.colours.inactive})
                        }
                        if(!that.north_walls[row][col].active){
                            that.north_walls[row][col].attr({fill: that.colours.inactive})
                        }
                    }
                }
            }
        })
    }

}


$(window).load(function () {
    var visible_world = new VisibleWorld();
    visible_world.init();
    visible_world.paper = Raphael("World", visible_world.world_width, visible_world.world_height);
    visible_world.render();




    var robot_e = visible_world.paper.image("../images/robot_e.png", 185, 190, 22, 30);
    var robot_w = visible_world.paper.image("../images/robot_w.png", 225, 190, 22, 30);
    var robot_n = visible_world.paper.image("../images/robot_n.png", 265, 190, 22, 30);
    var robot_s = visible_world.paper.image("../images/robot_s.png", 305, 190, 22, 30);

});
