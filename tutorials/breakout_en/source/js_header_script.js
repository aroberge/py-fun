// This code is meant to be automatically included in our template.

var editor = undefined;
var libEditor = undefined;
var intervalID = undefined;
var running = false;
var paused = false;
var speaker_on = false;
var user_response;

// hover states on the static widgets
$(function(){
  $('#dialog_link, ul#icons li').hover(
    function() { $(this).addClass('ui-state-hover'); }, 
    function() { $(this).removeClass('ui-state-hover'); }
  );
});

// play button controls
$(function(){
  $("#play").hover(
    function () {
      if ($(this).find("img").attr("src") == "../images/black_play.png") {
        $(this).find("img").attr({src:"../images/orange_play.png"});
      }
    }, 
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_play.png") {
        $(this).find("img").attr({src:"../images/black_play.png"});
      }
    }
  );
});

$(function(){
  $("#play").click(
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_play.png") {
        $(this).find("img").attr({src:"../images/green_play.png"});
        $("#stop").find("img").attr({src:"../images/black_stop.png"});
        running = true;
        runCode();
        return false;
      }
      if (paused){
        paused = false;
        $("#pause").find("img").attr({src:"../images/black_pause.png"});
      }
    }
  );
});

// pause button controls
$(function(){
  $("#pause").hover(
    function () {
      if (running) {
        if ($(this).find("img").attr("src") == "../images/black_pause.png") {
          $(this).find("img").attr({src:"../images/orange_pause.png"});
        }
      }
    }, 
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_pause.png") {
        $(this).find("img").attr({src:"../images/black_pause.png"});
      }
    }
  );
});

$(function(){
  $("#pause").click(
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_pause.png") {
        $(this).find("img").attr({src:"../images/green_pause.png"});
        paused = true;
      }
      else{
        paused = false;
        $(this).find("img").attr({src:"../images/black_pause.png"});
      }
      return false;
    }
  );
});

// stop button controls
$(function(){
  $("#stop").hover(
    function () {
      if (running) {
        if ($(this).find("img").attr("src") == "../images/black_stop.png") {
          $(this).find("img").attr({src:"../images/orange_stop.png"});
        }
      }
    }, 
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_stop.png") {
        $(this).find("img").attr({src:"../images/black_stop.png"});
      }
    }
  );
});

function update_buttons_after_stop(){
  // to be called by user in their own code as well as here.
  $("#play").find("img").attr({src:"../images/black_play.png"});
  $("#pause").find("img").attr({src:"../images/black_pause.png"});
  $("#stop").find("img").attr({src:"../images/red_stop.png"});
}

$(function(){
  $("#stop").click(
    function () {
      if (running) {
        if ($(this).find("img").attr("src") == "../images/orange_stop.png") {
          update_buttons_after_stop();
          clearInterval(intervalID);
          running = false;
          paused = false;
        }
        return false;
      }
    }
  );
});


// sound button controls
$(function(){
  $("#sound").hover(
    function () {
      if (speaker_on){
        $(this).find("img").attr({src:"../images/orange_speaker_on.png"});
      }
      else {
        $(this).find("img").attr({src:"../images/orange_speaker.png"});
      }
    }, 
    function () {
      if (speaker_on) {
        $(this).find("img").attr({src:"../images/green_speaker_on.png"});
      }
      else {
        $(this).find("img").attr({src:"../images/black_speaker.png"});
      }
    }
  );
});

$(function(){
  $("#sound").click(
    function () {
      if (speaker_on) {
        $(this).find("img").attr({src:"../images/black_speaker.png"});
        speaker_on = false;
      }
      else {
        $(this).find("img").attr({src:"../images/green_speaker_on.png"});
        speaker_on = true;
      }
    }
  );
});

// next link controls
$(function(){
  $(".nextLink").hover(
    function () {
      if ($(this).find("img").attr("src") == "../images/black_forward.png") {
        $(this).find("img").attr({src:"../images/orange_forward.png"});
      }
    }, 
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_forward.png") {
        $(this).find("img").attr({src:"../images/black_forward.png"});
      }
    }
  );
});

// previous link controls
$(function(){
  $(".prevLink").hover(
    function () {
      if ($(this).find("img").attr("src") == "../images/black_back.png") {
        $(this).find("img").attr({src:"../images/orange_back.png"});
      }
    }, 
    function () {
      if ($(this).find("img").attr("src") == "../images/orange_back.png") {
        $(this).find("img").attr({src:"../images/black_back.png"});
      }
    }
  );
});



function runCode() {
    if (intervalID != undefined)
        clearInterval(intervalID);
    $("#canvas")[0].getContext("2d").clearRect(0,0,
      $("#canvas")[0].width,
      $("#canvas")[0].height);

    //if there's a library defined, eval it
    if (libEditor != undefined) {
        eval(editAreaLoader.getValue("library"));
    }
    % if hidden_code: 
        intervalID = eval($("#hidden_code").val());
    % elif fullgame:
        intervalID = eval($("#hidden_code").val());
    % else:
        intervalID = eval(editAreaLoader.getValue("code"));
    % endif
};

$(document).ready(function(){
    % if js_code:
      editAreaLoader.init({
                    id : "code"
                    ,syntax: "js"      
                    ,start_highlight: true
                    ,replace_tab_by_spaces: true
                    ,font_size: "11"
                  });
    % endif
    
    % if library:
      editAreaLoader.init({
                    id : "library"
                    ,syntax: "js"      
                    ,start_highlight: true
                    ,replace_tab_by_spaces: true
                    ,display: "later"
                    ,font_size: "11"
                  });
      libEditor = true;
    % endif

    var $tabs = $('#textcontainer').tabs();
    % if not library:
        $tabs.tabs("remove", 2);
    % endif
    $tabs.tabs("select", 1);  // tab 0 is the table of contents
});