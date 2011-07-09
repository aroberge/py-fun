<!DOCTYPE html>
<!--
TODO implement pausing game
TODO implement stopping/quitting game
TODO add sound
TODO explore css sprites to reduce loading time
TODO translate in French
TODO upload to website (Tony's or Sainte-Anne?)
todo add background image at the end
todo add "you win" or "you lose!"
todo ask confirm to quit
todo add score
todo add second level
todo save high score with html storage
-->
<html>

<head> 

  <meta charset=utf-8>
  <title>Canvas Tutorial - ${title}</title>

  <script src="../js/edit_area/edit_area_full.js"></script>
  <script src="${jquery}"></script>
  <script src="${jquery_ui}"></script>
  <link rel="stylesheet" href="../css/jquery-ui.css" media="screen">
  <link rel="stylesheet" href="../css/custom.css">

  <script>
    <%include file="js_header_script.js"/>
  </script>

 </head>

  <body>
    % if hidden_code:
       <textarea id="hidden_code" style="display:none">${hidden_code}</textarea>
    % endif

    % if fullgame:
       <textarea id="hidden_code" style="display:none"><%include file="game_en.js"/></textarea>
    % endif


    <div id="header">
     <h1>Canvas Tutorial: Breakout!</h1>
    </div>


    <audio id="paddle_sound" preload>
      <source src="../sounds/kick11.wav" type="audio/x-wav">
      <source src="../sounds/kick11.ogg" type="application/ogg">
      <source src="../sounds/kick11.mp3" type="audio/mpeg">
    </audio> 

    <audio id="brick_sound" preload>
      <source src="../sounds/snare01.wav" type="audio/x-wav">
      <source src="../sounds/snare01.ogg" type="application/ogg">
      <source src="../sounds/snare01.mp3" type="audio/mpeg">
    </audio> 

    <audio id="wall_sound" preload>
      <source src="../sounds/kick6.wav" type="audio/x-wav">
      <source src="../sounds/kick6.ogg" type="application/ogg">
      <source src="../sounds/kick6.mp3" type="audio/mpeg">
    </audio> 

    <div id="canvascontainer">
         <canvas id="canvas" width="300" height="300"></canvas>
         <div id="controlIcons" style="text-align:center">
          <a id="play" href="#">
            <img src="../images/black_play.png" 
                 alt="run code" style="height:64px; border:none;"/>
          </a>
            <a id="pause" href="#">
            <img src="../images/black_pause.png" 
                 alt="pause" style="height:64px; border:none;"/>
          </a>
            <a id="stop" href="#">
            <img src="../images/black_stop.png" 
                 alt="stop" style="height:64px; border:none;"/>
          </a>
            <a id="sound" href="#">
            <img src="../images/black_speaker.png" 
                 alt="sound" style="height:64px; border:none;"/>
          </a>
             <!--<img class="runCode" src="../images/black_play.png" height="64px" onClick="runCode();"/> -->
         </div>
    </div>

    <div id="textcontainer">
      <h1 id="title">
        % if prev:
            <a href="${prev}.html" class="prevLink">
              <img src="../images/black_back.png" 
               alt="previous page" style="width:64px; border:none;"/>
            </a>
        % endif
        ${title}
        % if next:
            <a href="${next}.html" class="nextLink">
              <img src="../images/black_forward.png" 
               alt="next page" style="width:64px; border:none;"/>
            </a>
        % endif
      </h1>
      
      <ul>
          <li class="ui-tabs-nav-item"><a href="#toc"><span>Contents</span></a></li>
          <li class="ui-tabs-nav-item"><a href="#explain"><span>Code</span></a></li>
          <li class="ui-tabs-nav-item"><a href="#libraryContainer"><span>Library</span></a></li>
          <li class="ui-tabs-nav-item"><a href="#comments"><span>Comments</span></a></li>
      </ul>

      <div id="toc">
        % if toc:
        <ol>
           % for pagetitle, link in toc:
               <li><a href="${link}">${pagetitle}</a></li>
           % endfor
         </ol>
        % endif
      </div>

      <div id="explain">${explain_before}
          % if js_code:
               <div id="codebox">
               <textarea id="code" rows=${max(min(js_code.count("\n")+1, 20), 12)} cols=80>${js_code}</textarea>
               </div>
               <p>${explain_after}</p>
          % endif

          % if experiment:
            <div id="experiment">
            <h2>Experiment!</h2>
            ${experiment}
            </div>
          % endif
          
          % if prev:
              <a href="${prev}.html" class="prevLink">
                <img src="../images/black_back.png" 
                 alt="previous page" style="height:64px; border:none;"/>
              </a>
          % endif
          
          % if next:
              <a href="${next}.html" class="nextLink">
                <img src="../images/black_forward.png" 
                 alt="next page" style="height:64px; border:none;"/>
              </a>
          % endif
          </br> <!-- leave room for next link image on first page -->
          <p style="font-size: 6px; color: gray;">Tutorial by Andr&eacute; Roberge</p>
      </div>
     
      <div id="libraryContainer">
          % if library:
              <div id="libraryBox">
                  <textarea id="library" rows=${max(min(library.count("\n"), 20), 10)}
                            cols=80>${library}</textarea>
              </div>
          % endif
      </div>

      <div id="comments">
      Nothing here yet
      </div>
    </div>

  </body>
</html>
