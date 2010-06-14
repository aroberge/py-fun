
Raphael.fn.wall = function (x, y, width, height) {
    this.active = false;
    return this.rect(x, y, width, height);
};

Raphael.fn.button = function () {
    return this.rect(0, 0, 20, 20);
};


function Controls(world) {
    this.edit_button = world.paper.button().attr({x:10, y:0, fill:"red", title:"edit"});
    this.move_button = world.paper.button().attr({x:40, y:0, fill:"green", title:"move"});
    this.turn_left_button = world.paper.button().attr({x:70, y:0, fill:"blue", title:"turn_left"});
    this.change_robot = world.paper.button().attr({x:100, y:0, fill:"yellow", title:"change robot"});
    this.save_world = world.paper.button().attr({x:130, y:0, fill:"white", title:"save world"});

    this.edit_button.click( function () {
        var row, col;
        if(!this.edit) {
            this.edit = true;
            for(row=1; row <= world.rows; row++) {
                for(col=1; col <= world.columns; col++) {
                    if(!world.east_walls[row][col].active) {
                        world.east_walls[row][col].attr({fill: world.colours.inactive_edit});
                    }
                    if(!world.north_walls[row][col].active) {
                        world.north_walls[row][col].attr({fill: world.colours.inactive_edit});
                    }
                }
            }
        }
        else{
            this.edit = false;
            for(row=1; row <= world.rows; row++) {
                for(col=1; col <= world.columns; col++) {
                    if(!world.east_walls[row][col].active) {
                        world.east_walls[row][col].attr({fill: world.colours.inactive});
                    }
                    if(!world.north_walls[row][col].active) {
                        world.north_walls[row][col].attr({fill: world.colours.inactive});
                    }
                }
            }
        }
    });

    this.move_button.click( function () {
        world.robot_move();
    });

    this.turn_left_button.click( function () {
        world.robot.turn_left();
    });

    this.change_robot.click( function () {
        world.robot.change_robot();
    });

    this.save_world.click( function () {
        world.save();
    });

}


function VisibleRobot(world) {

    this.width = 22;
    this.height = 30;
    this.row = 0;
    this.column = 0;
    this.offset_x = world.margin_left + (world.narrow + world.tile_size - this.width)/2;
    this.offset_y = world.world_height - world.margin_bottom - this.height;
    this.style = "classic";
    this.angle = 0;
    this.x = undefined;
    this.y = undefined;
    this.path_x = undefined;
    this.path_y = undefined;
    this.path_history = undefined;

    this.robot = {
        "east": world.paper.image("../images/robot_e.png", 0, 0, this.width, this.height).hide(),
        "west": world.paper.image("../images/robot_w.png", 0, 0, this.width, this.height).hide(),
        "north": world.paper.image("../images/robot_n.png", 0, 0, this.width, this.height).hide(),
        "south": world.paper.image("../images/robot_s.png", 0, 0, this.width, this.height).hide(),
        "ellipse": world.paper.ellipse(0, 0, 15, 8).attr({'stroke-width': 0, fill: "r(0.90, 0.5)#fff-#0a3:70-#000"}).hide()
    };
    this.current = this.robot.east;
    this.current_orientation = "east";

    this.change_robot = function () {
        if (this.style === "classic") {
            this.style = "ellipse";
            this.x += 11;
            this.y += 13;
            this.current.hide();
            this.current = this.robot.ellipse.attr({cx:this.x, cy:this.y}).rotate(this.angle, true).show().toFront();
        }
        else{
            this.style = "classic";
            this.x -= 11;
            this.y -= 13;
            this.current.hide();
            this.current = this.robot[this.current_orientation].attr({x:this.x, y:this.y}).show().toFront();
        }
    };

    this.teleport = function (column, row) {
        this.x = this.offset_x + (row-1)*world.tile_size;
        this.y = this.offset_y + (column-1)*world.tile_size;
        this.path_x = this.x + 14;
        this.path_y = this.y + 17;
        this.path_history = [[this.path_x, this.path_y]];
        this.row = row;
        this.column = column;
        this.current.attr({x:this.x, y:this.y}).show();
    };

    this.move = function (delta_col, delta_row) {
        // previous_path will represent the full path up until this point;
        // begin_path is a single "dot" located at the end of previous_path;
        // end_path is the path from the beginning of the move to the end.
        this.column += delta_col;
        this.row += delta_row;
        this.x += delta_col*world.tile_size;
        this.y -= delta_row*world.tile_size;

        this.path_x += delta_col*world.tile_size;
        this.path_y -= delta_row*world.tile_size;

        this.path_history.push([this.path_x, this.path_y]);

        this.draw_path(500);
        if(this.style === "classic") {
            this.current.animate({x: this.x, y: this.y}, 500).toFront();
        }
        else{
            this.current.animate({cx: this.x, cy: this.y}, 500).toFront();
        }
    };

    this.draw_path = function (delay) {
        var x1, x2, y1, y2, length_, begin_path, end_path, previous_path, i;
        length_ = this.path_history.length;

        previous_path = "M" + this.path_history[0][0] + " " + this.path_history[0][1];
        for(i = 1; i < this.path_history.length-1; i++){
            previous_path += "L" + this.path_history[i][0] + " " + this.path_history[i][1];
        }
        if(this.trace !== undefined){
            this.trace.remove();
        }
        if(this.end_trace !== undefined){
            this.end_trace.remove();
        }
        this.trace = world.paper.path(previous_path);
        x1 = this.path_history[length_-2][0];
        y1 = this.path_history[length_-2][1];
        x2 = this.path_history[length_-1][0];
        y2 = this.path_history[length_-1][1]
        begin_path = "M" + x1 + " " + y1 + "L" + x1 + " " + y1;
        end_path = {path: "M" + x1 + " " + y1 + "L" + x2 + " " + y2};

        this.end_trace = world.paper.path(begin_path);
        this.end_trace.animate(end_path, delay);
    }

    this.turn_left = function () {
        this.angle -= 90;
        switch(this.current_orientation) {
            case "east":
                this.current_orientation = "north";
                this.path_y -= 6;
                break;
            case "north":
                this.current_orientation = "west";
                this.path_x -= 6;
                break;
            case "west":
                this.current_orientation = "south";
                this.path_y += 6;
                break;
            case "south":
                this.current_orientation = "east";
                this.path_x += 6;
                break;
        }
        this.path_history.push([this.path_x, this.path_y]);
        this.draw_path(500);

        if(this.style === "classic") {
            this.current.hide();
            this.current = this.robot[this.current_orientation].attr({x: this.x, y: this.y}).show().toFront();
        }
        else{
            // update the position in case we are in the middle of an animation
            this.current.attr({cx: this.x, cy: this.y});
            this.current.animate({rotation: this.angle}, 150).toFront();
        }
    };

}

function VisibleWorld() {
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
                    inactive_edit: "#dcf",
                    active: "brown",
                    active_hover: "brown",  // with different opacity below
                    inactive_hover: "grey",
                    border_active: "black",
                    border_inactive: "white",
                    background: "white"
    };

    // figures out dimensions to know how big a world is going to be
    // so that the "canvas" can be drawn with the appropriate dimensions.
    this.init = function (columns, rows) {
        var row;
        this.rows = rows;
        this.columns = columns;

        this.world_width = this.columns * this.tile_size + this.margin_left + this.margin_right + this.narrow;
        this.world_height = this.rows * this.tile_size + this.margin_bottom + this.margin_top;

        this.east_walls = new Array(this.rows+1);
        for(row = 1; row <= this.rows; row++) {
            this.east_walls[row] = new Array(this.columns+1);
        }

        this.north_walls = new Array(this.rows+1);
        for(row = 1; row <= this.rows; row++) {
            this.north_walls[row] = new Array(this.columns+1);
        }
    };


    this.create_east_wall = function (col, row) {
        var x, y, width, height;
        x = col*this.tile_size + this.margin_left;
        y = this.flip_rows(row)*this.tile_size + this.margin_top;
        width = this.narrow;
        height = this.wide + 2*this.narrow;
        return this.paper.wall(x, y, width, height).attr({fill:this.colours.inactive, stroke:this.colours.border_inactive});
    };

    this.create_north_wall = function (col, row) {
        var x, y, width, height;
        x = (col-1)*this.tile_size + this.margin_left;
        y = this.flip_rows(row)*this.tile_size + this.margin_top;
        width = this.wide + 2*this.narrow;
        height = this.narrow;
        return this.paper.wall(x, y, width, height).attr({fill:this.colours.inactive, stroke:this.colours.border_inactive});
    };

    this.create_wall = function (col, row, orientation) {
        var that = this;
        if(orientation === "east") {
            this._wall = this.create_east_wall(col, row);
        }
        else{
            this._wall = this.create_north_wall(col, row);
        }
        this._wall.click( function () {
            if(that.controls.edit_button.edit) {
                if(this.active) {
                    this.attr({fill: that.colours.inactive_hover});
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
                if(that.controls.edit_button.edit) {
                    if(this.active) {
                        this.attr({fill: that.colours.active_hover, opacity: 0.5});
                    }
                    else{
                        this.toFront();
                        this.attr({fill: that.colours.inactive_hover});
                    }
                }
            },
            function (event) {
                if(that.controls.edit_button.edit) {
                    if(this.active) {
                        this.attr({fill: that.colours.active, opacity: 1});
                    }
                    else{
                        this.attr({fill: that.colours.inactive_edit, stroke: that.colours.border_inactive});
                        this.toBack();
                        that.background.toBack();
                    }
                }
        });
        return this._wall;
    };

    this.create_background = function () {
        this.background = this.paper.rect(0, 0, this.world_width, this.world_height).attr({fill: this.colours.background}).toBack();
    };

    this.flip_rows = function (row) {
        return this.rows - row;
    };

    this.create_borders = function () {
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
    };

    this.create_grid = function () {
        var _x, _y, end_x, end_y, start_x, start_y, row, col;
        end_x = this.columns*this.tile_size + this.margin_left;
        end_y = this.rows*this.tile_size + this.margin_top + this.narrow/2;
        start_y = this.margin_top + this.narrow/2;
        start_x = this.margin_left + this.narrow/2;
        for(row=0; row < this.rows; row++) {
            _y = row*this.tile_size + this.tile_size/2 + this.margin_top + this.narrow/2;
            this.paper.path("M" + start_x +" "+ _y + "L" + end_x + " " + _y).attr({stroke: "#666", "stroke-dasharray": ". "});
            this.paper.text(this.margin_left_text, _y, this.rows-row);
            }
        for(col=0; col < this.columns; col++) {
            _x = col*this.tile_size + this.tile_size/2 + this.margin_left + this.narrow/2;
            this.paper.path("M" + _x +" "+ start_y + "L" + _x + " " + end_y).attr({stroke: "#666", "stroke-dasharray": ". "});
            this.paper.text(_x, this.world_height - this.margin_bottom_text, col+1);
        }
    };

    this.render = function (saved_world) {
        var row, col, point;
        if(this.controls === undefined) {
            this.controls = new Controls(this);
        }
        for(row=1; row <= this.rows; row++) {
            for(col=1; col <= this.columns; col++) {
                this.east_walls[row][col] = this.create_wall(col, row, "east");
                this.north_walls[row][col] = this.create_wall(col, row, "north");
            }
        }
        this.create_background();
        this.create_borders();
        this.create_grid();
        this.restore(saved_world);
        if(this.robot === undefined) {
            this.robot = new VisibleRobot(this);
            this.robot.teleport(1, 1);
        }
    };

    this.restore = function (saved_world) {
        var row, col, point;
        if(saved_world.east_walls !== undefined){
            for(point=0; point< saved_world.east_walls.length; point++){
                column = saved_world.east_walls[point][0];
                row = saved_world.east_walls[point][1];
                this.east_walls[row][column].active = true;
                this.east_walls[row][column].attr({fill: this.colours.active, stroke: this.colours.border_active});
                this.east_walls[row][column].toFront();
            }
        }
        if(saved_world.north_walls !== undefined){
            for(point=0; point< saved_world.north_walls.length; point++){
                column = saved_world.north_walls[point][0];
                row = saved_world.north_walls[point][1];
                this.north_walls[row][column].active = true;
                this.north_walls[row][column].attr({fill: this.colours.active, stroke: this.colours.border_active});
                this.north_walls[row][column].toFront();
            }
        }
    };

    this.robot_move = function () {
        var delta_row, delta_col, new_row, new_col;
        switch(this.robot.current_orientation) {
            case "east":
                delta_row = 0;
                delta_col = 1;
                break;
            case "north":
                delta_row = 1;
                delta_col = 0;
                break;
            case "west":
                delta_row = 0;
                delta_col = -1;
                break;
            case "south":
                delta_row = -1;
                delta_col = 0;
                break;
        }
        new_row = this.robot.row + delta_row;
        new_col = this.robot.column + delta_col;
        if( new_row >= 1 && new_row <= this.rows &&
           new_col >= 1 && new_col <= this.columns) {
            this.robot.move(delta_col, delta_row);
        }
    };

    this.save = function () {
        var saved_world, j, popup, active_east_walls, active_north_walls, row, col;
        active_east_walls = [];
        active_north_walls = [];
        for(row = 1; row <= this.rows; row++) {
            for(col=1; col <= this.columns; col++){
                if(this.north_walls[row][col].active){
                    active_north_walls.push([col, row]);
                }
                if(this.east_walls[row][col].active){
                    active_east_walls.push([col, row]);
                }
            }
        }

        saved_world = {
            "rows": this.rows,
            "columns": this.columns,
            "robot": [this.robot.column, this.robot.row, this.robot.current_orientation, this.robot.style],
            "east_walls": active_east_walls,
            "north_walls": active_north_walls
        };
        j = JSON.stringify(saved_world);
        popup = window.open("", "World Parameters", "width=320, height=210, scrollbars=yes");
        popup.document.write(j);
        popup.document.close();
    };

}


$(window).load(function () {

    var saved_world = '{"rows":8,"columns":12,\n"robot":[1,1,"north","ellipse"],"east_walls":[[5,3], [4,4]],"north_walls":[[5,3]]}';
    try{
        saved_world = JSON.parse(saved_world);
    }
    catch (e){
        alert("Problem with saved world; will revert to defaults.");
        saved_world = {"rows":10,
                        "columns":10,
                        "robot":[1,1,"east","classic"]};
    }
    var visible_world = new VisibleWorld();
    visible_world.init(saved_world.columns, saved_world.rows);
    visible_world.paper = Raphael("World", visible_world.world_width, visible_world.world_height);
    visible_world.render(saved_world);


    function activate_keys(e) {
            var keyCode = e.keyCode || e.which,
            arrow = {left: 37, up: 38, right: 39, down: 40 };
            switch (keyCode) {
                case arrow.left:
                    visible_world.robot.turn_left();
                break;
                case arrow.up:
                    visible_world.robot_move();
                break;
            };
    }

    $("#World").hover(
      function () {
        //entering
        visible_world.background.attr({stroke: "blue", "stroke-width": 5});
        $(document).bind('keydown', activate_keys);
      },
      function () {
        // leaving
        visible_world.background.attr({stroke: "black", "stroke-width": 2});
        $(document).unbind('keydown', activate_keys);
      }
    );



});
