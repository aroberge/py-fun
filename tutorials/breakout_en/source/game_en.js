var dx = 2;
var dy = -3;
var ctx;
var WIDTH;
var HEIGHT;

var rightDown = false;
var leftDown = false;
var canvasMinX = 0;
var canvasMaxX = 0;
var intervalId = 0;
var bricks;
var NROWS = 5;
var NCOLS = 5;
var BRICKWIDTH;
var BRICKHEIGHT = 15;
var PADDING = 1;
var paddle;
var ball;

var score;

var collision = false;

var rowcolors = ["#FF1C0A", "#FFFD0A", "#00A308", "#0008DB", "#EB0093"];
var background_colour = "#000000";

function Ball(x, y) {
  this.x = x;
  this.y = y;
  this.r = 10;
  this.colour = "#ffffff";
  this.draw = function() {
    ctx.fillStyle = this.colour;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI*2, true);
    ctx.closePath();
    ctx.fill();
  };
}

function Paddle(x) {
  this.h = 8;
  this.w = 50;
  this.x = x;
  this.colour = "#ffffff";

  this.draw = function() {
    ctx.fillStyle = this.colour;
  // see http://www.williammalone.com/briefs/how-to-draw-ellipse-html5-canvas/
    ctx.beginPath();
    ctx.moveTo(this.x, HEIGHT, this.w);
    ctx.bezierCurveTo(
      this.x, HEIGHT-this.h,
      this.x + this.w, HEIGHT-this.h,
      this.x + this.w, HEIGHT);
    ctx.closePath();
    ctx.fill();
  };

  this.keyboard_move = function(left, right) {
    if (right) {
      this.x += 5;
      if (this.x &gt; WIDTH - this.w) {
        this.x = WIDTH - this.w;
      }
    }
    else if (left) {
      this.x -= 5;
      if (this.x &lt; 0){
        this.x = 0;
      }
    }
  };
}

var isPlaying = true;
var background_image = new Image();
background_image.src = '../images/earth.jpg';

function playBeat(sound_id) {
  if (speaker_on) {
    var tmpAudio;
    tmpAudio = document.getElementById(sound_id);
    if (!tmpAudio.paused) {
      // Pause and reset it
      tmpAudio.pause();
      tmpAudio.currentTime = 0.0;
    }
    tmpAudio.play();
  };
}

function init() {
  ctx = $('#canvas')[0].getContext("2d");
  WIDTH = $("#canvas").width();
  HEIGHT = $("#canvas").height();
  BRICKWIDTH = (WIDTH/NCOLS) - 1;
  ball = new Ball(25, 250);
  paddle = new Paddle(WIDTH / 2);
  canvasMinX = $("#canvas").offset().left;
  canvasMaxX = canvasMinX + WIDTH;
  intervalId = setInterval(update, 10);
  score = 0;
  return intervalId;
}

function rect(x, y, w, h) {
  ctx.beginPath();
  ctx.rect(x,y,w,h);
  ctx.closePath();
  ctx.fill();
}

function clear() {
  ctx.fillStyle = background_colour;
  ctx.clearRect(0, 0, WIDTH, HEIGHT);
  rect(0, 0, WIDTH, HEIGHT);
}

function onKeyDown(evt) {
  if (evt.keyCode == 39) rightDown = true;
  else if (evt.keyCode == 37) leftDown = true;
}

function onKeyUp(evt) {
  if (evt.keyCode == 39) rightDown = false;
  else if (evt.keyCode == 37) leftDown = false;
}

function onMouseMove(evt) {
  paddle.x = Math.max(evt.pageX - canvasMinX - (paddle.w/2), 0);
  paddle.x = Math.min(WIDTH - paddle.w, paddle.x);
}

$(document).keydown(onKeyDown);
$(document).keyup(onKeyUp);
$(document).mousemove(onMouseMove);

function initbricks() {
    bricks = new Array(NROWS);
    for (i=0; i &lt; NROWS; i++) {
        bricks[i] = new Array(NCOLS);
        for (j=0; j &lt; NCOLS; j++) {
            bricks[i][j] = 1;
        }
    }
}

function drawbricks() {
  for (i=0; i &lt; NROWS; i++) {
    ctx.fillStyle = rowcolors[i];
    for (j=0; j &lt; NCOLS; j++) {
      if (bricks[i][j] == 1) {
        rect((j * (BRICKWIDTH + PADDING)) + PADDING, 
             (i * (BRICKHEIGHT + PADDING)) + PADDING,
             BRICKWIDTH, BRICKHEIGHT);
      }
    }
  }
}

function game_over(){
    ctx.fillStyle = 'rgba(0, 1, 1, 0.5)';
    rect(0, 0, WIDTH, HEIGHT);
    ctx.font = "40pt Helvetica";
    ctx.fillStyle = "#ff0000";
    ctx.fillText("Game Over!", 10, 100);
    ctx.font = " 15pt Helvetica";
    ctx.fillStyle = "#00ff00";
    ctx.fillText("Score: " + score, 10, 150);
    if (localStorage.highScore == null) localStorage.highScore = 0;
    ctx.fillText("Previous high score: " + localStorage.highScore, 10, 200);
    if (parseInt(localStorage.highScore) &lt; score) localStorage.highScore = score;
  clearInterval(intervalId);
}



function update() {
  if (paused){
    return;
  }
  clear();
  ctx.drawImage(background_image,0,0);
  paddle.keyboard_move(leftDown, rightDown);
  paddle.draw()
  drawbricks();
  ball.draw();

  //want to learn about real collision detection? go read
  // http://www.harveycartel.org/metanet/tutorials/tutorialA.html
  rowheight = BRICKHEIGHT + PADDING;
  colwidth = BRICKWIDTH + PADDING;
  row = Math.floor(ball.y/rowheight);
  col = Math.floor(ball.x/colwidth);
  //reverse the ball and mark the brick as broken
  if (ball.y &lt; NROWS * rowheight 
      &amp;&amp; row &gt;= 0 
      &amp;&amp; col &gt;= 0 
      &amp;&amp; bricks[row][col] == 1) {
    dy = -dy;
    bricks[row][col] = 0;
    playBeat("brick_sound");
    score += row;
  }
 

  if (ball.x + dx + ball.r &gt; WIDTH || ball.x + dx - ball.r &lt; 0) {
    collision = true;
    playBeat("wall_sound");
    dx = -dx;
    if (ball.x + dx + ball.r &gt; WIDTH){
      ball.x = WIDTH - ball.r
    }
    else if(ball.x + dx - ball.r &lt; 0) {
      ball.x = ball.r;
    }
  }

  
  if (ball.y + dy - ball.r &lt; 0){
    collision = true;
    playBeat("wall_sound");
    dy = -dy;
    ball.y = ball.r;
  }
  else if (ball.y + dy + ball.r &gt; HEIGHT - paddle.h) {
    if (ball.x + (ball.r/2) &gt; paddle.x 
        &amp;&amp; ball.x - (ball.r/2) &lt; paddle.x + paddle.w) {
      //move the ball differently based on where it hit the paddle
      collision = true;
      playBeat("paddle_sound");
      dx = 4 * ((ball.x-(paddle.x+paddle.w/2))/paddle.w);
      dy = -dy;
      ball.y = HEIGHT - paddle.h - ball.r;
    }
    else if (ball.y + dy + ball.r &gt; HEIGHT)
      game_over();
  }
 
 if (collision)  collision = false;  // show the collision before reversing course
 else {
    ball.x += dx;
    ball.y += dy;
  }
}

initbricks();
init();
