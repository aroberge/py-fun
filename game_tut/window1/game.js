var game_window;

function init_game(){
    init_window();  // creates class and instantiates
    run()
}

function init_window(){
    // Mimic Pyglet's pyglet.window.Window()
    function GameWindow(){
        this.canvas = document.getElementById("game_canvas");
        this._window = this.canvas.getContext("2d");
        this.width = this.canvas.width;
        this.height = this.canvas.height;
    }
    game_window = new GameWindow();

    // add methods - only one for now
    function clear(){
        // default color is black
        this._window.fillRect(0, 0, this.width, this.height);
    }
    GameWindow.prototype.clear = clear;
}

// similar to python method
function on_draw(){
    game_window.clear();
}

function run(){   // the game loop will be here
    on_draw();
}