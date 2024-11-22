<?php include("session.php");


if (isset($_REQUEST['test'])) {
    $_SESSION['uuid'] = "Test";
    $_SESSION['username'] = "Test";
    $_SESSION['difficulty'] = "Test";
    if (file_exists("logs/Test.txt")) {
    unlink("logs/Test.txt");
}
if (file_exists("maps/Test.pkl")) {
    unlink("maps/Test.pkl");
}
file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=Test&difficulty=difficulty&race=Human&name=Test");

} else {
    session_required();
    if (!file_exists("maps/".$_SESSION['uuid'].".pkl")) {
        header("Location: https://fathomless.io/character/");
    }
}




?>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.cdnfonts.com/css/8bit-wonder');
            * {
            font-family: '8BIT WONDER', sans-serif;
            }
            html, body {
            margin:0;
            padding:0;
            touch-action: manipulation;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: moz-none;
            -ms-user-select: none;
            -o-user-select: none;
            user-select: none;
            overflow-x:none;
            background:black;
            }
            #page {
            width:100vw;
            height:100svh;
            }
            #page,#canvas .tile,#inventory, #keyBind {
            display:flex;
            align-items:center;
            justify-content:center;
            background-size: contain;
            box-sizing: border-box;
            position:relative;
            }
            #canvas {
            display: grid;
            }
            .tile div {
            position:absolute;
            background-repeat: no-repeat;  
            background-size: cover;
            background-position: center;
            width:100%;
            height:100%;
            }
            
            #inventory, #keyBind {
            transition:.75s;
            height:0;
            width:100vw;
            position:absolute;
            flex-direction:column;
            font-size:0;
            color:white;
            }
            
            
            #dialogue, #alert {
                
            display:flex;
            align-items:center;
            position:absolute;
            text-align:center;
            color:white;
            justify-content:center;
            font-size:30px;
            background-size: contain;
            z-index:1;
            }
            #dialogue, #inventory, #keyBind {
            bottom:0;
            left:0;
            width:100vw;
            }
            #alert {
            padding:20px 0 20px 0;
            pointer-events: none;
            top:0;
            left:20;
            font-size:40px;
            justify-content:end;
            gap:20px;
            height:40px;
            }
            #alert img {
            width:50px;
            height:50px;
            }
            #alert p {
            display:flex;
            align-items:center;
            justify-content:center;
            }
            @keyframes fadeSettings {
            0%   {opacity:1;}
            75% {opacity:1;}
            100% {opacity:.25;}
            }
            #settings:not(:hover){
            animation-name: fadeSettings;
            animation-duration: 4s;
            }
            #settings {
    
            transition:4s;
            position:absolute;
            top:0;
            right:0;
            height:100px;
            display:flex;
            align-items:center;
            justify-content:end;
            flex-direction:row-reverse;
            width:0px;
            background:saddlebrown;
            border-radius:20px;
            opacity:.25;
            font-size:0;
            
            }
            #settings button {
            filter: brightness(0) invert(1);
            }
            #settings:hover {
            transition:.75s;
            opacity:1;
            }
            #settings button{
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            display:flex;
            align-items:center;
            justify-content:center;
            }
            #settings input[type="range"] {
                margin:0;
                padding:0;
                height:20px;
                display:none;
                -webkit-appearance: none;  /* Override default CSS styles */
  appearance: none;
  width: 100%; /* Full-width */
  height: 25px; /* Specified height */
  background: saddlebrown; /* Grey background */
  outline: none; /* Remove outline */
  opacity: 0.7; /* Set transparency (for mouse-over effects on hover) */
  -webkit-transition: .2s; /* 0.2 seconds transition on hover */
  transition: opacity .2s;
  border:2px solid rgb(212,175,55);
  border-radius:20px;
                
            }
            
            /* Mouse-over effects */
#settings input[type="range"]:hover {
  opacity: 1; /* Fully shown on mouse-over */
}

/* The slider handle (use -webkit- (Chrome, Opera, Safari, Edge) and -moz- (Firefox) to override default look) */
#settings input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none; /* Override default look */
  appearance: none;
  width: 25px; /* Set a specific slider handle width */
  height: 25px; /* Slider handle height */
  border-radius:50%;
  background: white; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

#settings input[type="range"]::-moz-range-thumb {
  width: 25px; /* Set a specific slider handle width */
  height: 25px; /* Slider handle height */
  background: white; /* Green background */
  cursor: pointer; /* Cursor on hover */
  border-radius:50%;
}
            .gearRotate {
            -webkit-animation-name: gearRotation;
            -webkit-animation-duration: 1s;
            -webkit-animation-timing-function: ease-in-out;
            transform:rotate(360deg);
            }
            @-webkit-keyframes gearRotation {
            from {
            transform:rotate(0deg);
            }
            to {
            transform:rotate(360deg);
            }
            }
            #settings button img {
            transition:1s;
            animation-timing-function: ease-in-out;
            transform:scale(0deg);
            width:100px;
            }
            #settings span {
            height:100%;
            width:100%;
            display:flex;
            align-items:center;
            justify-content:space-around;
            }
            #settings span * {
            height:100%;
            width:0px;
            padding:0;
            margin:0;
            font-size:inherit;
            }
            button, input {
            transition:.75s;
            }
            button, input[type=submit]:hover {
            transition:.75s;
            transform:scale(.9);
            }
            .manhattan:hover, .selected .Top{
            background: purple;
            opacity:.3;
            cursor:pointer;
            }
            #cover {
            position:absolute;
            top:0;
            left:0;
            width:100vw;
            height:100vh;
            cursor:wait;
            }
            #inspection {
            position:absolute;
            top:0;
            left:0;
            width:0;
            height:100svh;
            background:saddlebrown;
            overflow:scroll;
            color:rgb(212,175,55);
            -ms-overflow-style: none;
            scrollbar-width: none; 
            resize:both;
            display:flex;
            align-items:center;
            justify-content:start;
            flex-direction:column;
            }
            
            #inspection::-webkit-scrollbar {
            display: none;
            }
            #inspection .close {
                position:absolute;
            top:0;
            right:0;
            width:30px;
            height:30px;
            }
            #inspection button {
            
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            }
            #inspection img {
            width:75px;
            max-height:75px;
            float:right;
            }
            #inspection > div > div {
            width:90%;
            }
            #inspection div {
            border-radius:20px;
            border:solid rgb(212,175,55) 5px;
            width:90%;
            padding:5px;
            }
            
            #inspection div p {
            word-wrap: break-word;
            }
            #inspection p.center {
                padding-top:20px;
            text-align:center;
            }
            #inspection > div {
                border:none;
            } 
            
            .inspecting, .selected {
            transition:.75s;
            border:#eee dotted 2px;
            }
            .selected {
                transition:.0s;
            }
            hr {
            width:90%;
            height:5px;
            background:rgb(212,175,55);
            border:none;
            }
            #keyBind {
            background:saddlebrown;
            }
            #keyBind button {
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            color:rgb(212,175,55);
            }
            @keyframes inspectionLoad {
            from {opacity:1;}
            to {opacity:0;}
            }
            .inspectionLoad {
            animation-name: inspectionLoad;
            animation-duration: 1s;
            }
            .Creature, .Terrain, .Decor {
                text-align:center;
                font-size:10px;
                color:white;
                -webkit-text-fill-color: white;
  -webkit-text-stroke-width: .5px;
  -webkit-text-stroke-color: black;
                
            }
        .modal {
            position:absolute;
            top:0;
            left:0;
            width:100vw;
            height:100vh;
            color:rgb(212,175,55);
            
        }
        .modal div .close{
            width:100%;
            height:50px;
            display:flex;
            align-items:center;
            justify-content:end;
           
            font-size:20px;
            
            
        }
        #modal {
            text-align:center;
        }
        #modal .x {
            position:absolute;
            top:0;
           right:0;
           width:fit-content;
            background:none;
            padding:0;
            border:0;
            margin:0;
            
        }
        .modal .shop span{
            display:flex;
            align-items:center;
            justify-content:center;
            width:100%;
            
        }
        .modal .shop {
            overflow:scroll;
            height:clamp(300px,50svh,600px);
        }
        .modal div .close button{
                padding:20px;
                height:20px;
                background:none;
                border:none;
                -webkit-appearance: none;  /* Override default CSS styles */
  appearance: none;
  outline: none; /* Remove outline */
  color:rgb(212,175,55);
        }
        .modal > div {
            margin: 0;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:start;
            width:50vw;
            height:clamp(fit-content,50svh,50svh);
            background:saddlebrown;
            gap:20px;
            border:rgb(212,175,55) 2px solid;
            height:fit-content;

        }
        .modal > div img {
            width:50px;
        }
        .modal > div .log {
            padding:20px;
            height:200px;
            overflow:scroll;
            display:flex;
            align-items:start;
            justify-content:start;
            flex-direction:column;
            text-align:left;
        }
        .modal button {
            transition:.75s;
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            width:75%;
            height:fit-content;
            color:gold;
            font-size:20px;
            border:2px burlywood solid;
            background:saddlebrown;
            padding:20px;
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            
        }
        
        #levelUpMenu div {
            width:100%;
            display:flex;
            align-items:center;
            justify-content:center;
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            gap:0;

        }
        #levelUpMenu span{
            padding:0;
            margin:0;
            height:600px;
            overflow:scroll;
            height:clamp(300px,50svh,600px);
        }
        #levelUpMenu div button {
           
            width:50px;
            height:100%;
            padding:0;
            margin:0;
            outline:0;
            border:0;
            font-size:30px;
                        background:none;

        }
        #inventory span * {
            padding:0;
            margin:0;
        }
        #inventory span {
            padding:20px;
        }
        #inventory > span {
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            width:100%;
            height:fit-content;
            font-size:20px;
            text-align:center;
             border:rgb(212,175,55) 2px solid;
            background:saddlebrown;
            color:rgb(212,175,55);
            gap:0px;
            
            
        }#inventory > span > span {
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:row;
            flex-wrap:wrap;
            width:100%;
            height:fit-content;
            

        }
        
        #inventory > span > span > span {
            display:flex;
            align-items:center;
            justify-content:space-between;
            flex-direction:column;
            width:fit-content;
            height:fit-content;
             border:rgb(212,175,55) 2px solid;
             font-size:15px;
             width:200px;
             height:200px;
             gap:20px
        }
        #inventory > span > span > span p {
            height:30px;
        }
         
        
        #inventory img {
            height:50px;
            }
            #inventory {
                flex-direction:row;
                flex-wrap:wrap;
                gap:20px
            }
          
            .tile .Light {
                z-index:2;
                background:#000;
            }
            .tile .Top {
                z-index:3;
            }
            #dialogue {
                z-index:5;
            }
            #inventory, #settings, #alert, #keyBind, #modal, #inspection, #action {
                z-index:4;
            }
            #action {
                transition:.75s;
                display:flex;
                align-items:center;
                justify-content:center;
                width:100%;
                gap:20px;
                position:absolute;
                top:0;
                left:0;
                background:#eee;
                border:rgb(212,175,55) 2px solid;
            background:saddlebrown;
            color:rgb(212,175,55);
            height:0;
            margin:0;
            padding:0;
            box-sizing: border-box;
            }
            #action {
                border:none;
            }
            #action button {
                transition:.75s;
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            width:75%;
            height:fit-content;
            color:gold;
            border:2px burlywood solid;
            background:saddlebrown;
            padding:20px;
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            
            }
            #inventory button, #inspection div button, #inventory > span > span > span button {
                transition:.75s;
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            width:fit-content;
            height:fit-content;
            color:gold;
            font-size:20px;
            border:2px burlywood solid;
            background:saddlebrown;
            padding:20px;
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            text-align:center;
            }
            #inventory button:nth-child(1) {
                position:absolute;
                top:0;
                left:0;
            }
            #inspection div button {
                width:100%;
            }
           
            
        </style>
    </head>
    <body>
        <div id = "page">
            <div id = "canvas"></div>
        </div>
        <div id = "dialogue"></div>
        <div id = "alert"></div>
        <div id = "inventory"></div>
        <div id = "keyBind"></div>
        <div id = "settings">
            <button data-setting = "settings_menu">
            <img id = "gear" src = "https://icons.veryicon.com/png/o/miscellaneous/xdh-font-graphics-library/gear-setting-1.png">
            </button>
            <span id = "settings_span">
                
                
                <button id = "sfxVolume">SFX Volume: 0%</button>
                <input  id = "sfxSlider" class = "slider" data-setting = "sfxVolume" type = "range" min = "0" max = "100" value = "0">
                <button id = "musicVolume">Music Volume: 0%</button>
                <input id = "musicSlider" class = "slider"  data-setting = "musicVolume" type = "range" min = "0" max = "100" value = "0">
                <button id = "fovLevel">Current Fov: 11</button>
                <input id = "fovSlider" class = "slider"  data-setting = "fovSlider" type = "range" min = "3" max = "11" value = "11">
                <button data-setting = "toggleAscii">Enable Ascii</button>
                <button data-setting = "toggleResolution">Toggle Resolution</button>
                <button data-setting = "keyBind">Key Binds</button>
                <button data-setting = "keyboardOnly">Keyboard Only</button>
                <?=($_SESSION['username'] == "Guest")?'<button data-setting = "saveGuest">Save Progress</button>':'<button data-setting = "logout">Logout</button>';?>
            </span>
        </div>
        <div id = "inspection"></div>
        <div id = "action"></div>
        <script>
            const username = '<?=$_SESSION['username']?>';
            const tileObjects = JSON.parse('<?=file_get_contents("https://fathomless.io/json/objects.json")?>');
            const defaults = {"default":{"textureIndex":8,"intensity":0},"Bottom":{"textureIndex":1}};
            var inspectingPlayer = activeTile = isAction = songPosition = sfxVolume = musicVolume = currentLevel = playerDirection = viewRadius = keyBindOpened = inspecting = music = playMusic = sfx = isLowResolution = start = disableMovement = playAudio = closeSetting = isSettingsOpen = currentMap = viewDiameter  = inventoryOpened = asciiMode= 0;
            var objectTypes = ["Bottom","Terrain","Item","Decor","Creature","Light","Top"];
            var keyBinds = (!localStorage.getItem("keyBinds"))?{"Inventory":"KeyE","Select":"Enter","Settings":"Escape","Attack":"Space","Movement":["ArrowRight","ArrowDown","ArrowLeft","ArrowUp","KeyD","KeyS","KeyA","KeyW"]}:(JSON.parse(localStorage.getItem("keyBinds")));
            var fov = (localStorage.getItem("fov"))?localStorage.getItem("fov"):11;
            document.getElementById('fovLevel').innerHTML = "Current Fov: "+fov;
            document.getElementById('fovSlider').value = fov;
            if (localStorage.getItem("soundSettings")) {
                var soundSettings = JSON.parse(localStorage.getItem("soundSettings"));
            playMusic = soundSettings[0];
            
            musicVolume =  soundSettings[1]
            
            
            playAudio = soundSettings[2];
          if (playAudio) {
                     sfx = [new Audio('https://fathomless.io/assets/audio/walking.mp3'),new Audio('https://fathomless.io/assets/audio/coin.mp3'),new Audio('https://fathomless.io/assets/audio/crash.mp3'),new Audio('https://fathomless.io/assets/audio/walk2.mp3'), new Audio('https://fathomless.io/assets/audio/woosh.mp3'), new Audio('https://fathomless.io/assets/audio/dead.mp3'), new Audio('https://fathomless.io/assets/audio/attack.mp3'), new Audio('https://fathomless.io/assets/audio/shoot.mp3'), new Audio('https://fathomless.io/assets/audio/hit.mp3'), new Audio('https://fathomless.io/assets/audio/kill.mp3')];

          }
            sfxVolume =  parseInt(soundSettings[3])
            songPosition = parseInt(soundSettings[4])
                                document.getElementById('musicVolume').innerHTML = "Music Volume: "+(musicVolume)+"%";

            document.getElementById("musicSlider").value = musicVolume;
                    document.getElementById('sfxVolume').innerHTML = "SFX Volume: "+(sfxVolume)+"%";

                document.getElementById("sfxSlider").value = sfxVolume;
            }

            sendRequest();
            window.mobileCheck = function() {let check = false;(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);return check;};
            //if (mobileCheck()){toggleResolution()}
            
            function inspectPlayer() {
                if (inspectingPlayer) {
                    
                } else {
                    
                }
                inspectingPlayer = !inspectingPlayer;
            }
            function toggleActions(tileId) {
                var coordinates = tileId.split(",");
                if (tileId == viewRadius+","+viewRadius && !inventoryOpened) {
                    toggleInventory();
                    return;
                }
                if (tileId == viewRadius+","+viewRadius && inspecting == tileId) {
                    inspectTile(tileId)
                    return;
                }
                if (document.getElementById(activeTile)) {
                    document.getElementById(activeTile).classList.remove('inspecting');
                }
                
                if ((!isAction || tileId != activeTile) && currentMap[coordinates[0]][coordinates[1]]['Bottom']['textureIndex'] != 8 && (Object.keys(currentMap[coordinates[0]][coordinates[1]]).length > 2)) {
                    document.getElementById("action").style.height = "100px";
                     document.getElementById("action").style.fontSize = "20px";
                     document.getElementById("action").style.border = "rgb(212,175,55) 2px solid";
                    var selectedTile = currentMap[coordinates[0]][coordinates[1]];
                    document.getElementById(tileId).classList.add('inspecting');
                    var inspectButton = "<button onclick = 'inspectTile(activeTile);'>Inspect</button>";
                    var attackButton = "<button onclick = 'directionHandler([parseInt(activeTile.split(`,`)[0]),parseInt(activeTile.split(`,`)[1])]);toggleActions(activeTile);'>Attack</button>";
                    var moveButton = "<button onclick = 'directionHandler([parseInt(activeTile.split(`,`)[0]),parseInt(activeTile.split(`,`)[1])]);toggleActions(activeTile);'>"+((currentMap[coordinates[0]][coordinates[1]]['Terrain'])?"Destroy":"Move")+"</button>";
                    var interactButton = "<button onclick = 'sendRequest(`?interact=`+(parseInt(activeTile.split(`,`)[0]))+`,`+(parseInt(activeTile.split(`,`)[1])));toggleActions(activeTile);'>Interact</button>";

                    if (currentMap[coordinates[0]][coordinates[1]]['Bottom']['textureIndex'] != 8) {
                    document.getElementById('action').innerHTML = inspectButton;
                        if (document.getElementById(tileId).dataset.manhattan == 1) {
                            document.getElementById('action').innerHTML += moveButton;
                            if (currentMap[coordinates[0]][coordinates[1]]['Decor']) {
                             document.getElementById('action').innerHTML += interactButton;
                        }
                        }
                        
                       
                    }

                    activeTile = tileId;
                    isAction = true;
                    
                    

                    
                } else {
                    document.getElementById("action").style.height = "0px";
                    document.getElementById("action").style.fontSize = "0px";
                    document.getElementById('action').style.border = "";
                     document.getElementById('action').innerHTML = "";
                    activeTile = 0;
                    isAction = false;
                }
                
               
            }
            
            
            function createModal(content, id = "") {
                disableMovement = true;
                if (document.getElementById(`modal`)) {
                document.getElementById(`modal`).remove();
                }
                var modal = Object.assign(document.createElement('div'),{classList:"modal",id:"modal"});
                      var innerDiv = "";
                       innerDiv +=  content;
                       modal.innerHTML = "<div id = '"+id+"'>"+innerDiv+"</div>";
                        document.body.appendChild(modal);
                        
                        modal.querySelector('button').focus();

            }
            
            function createLine(start, end) {
                var dx = start[0]- end[0];
                var dy =  start[1] - end[1];
                var m = dy/dx;
                for (var x = start[0]; x < end[0]; x++) {
                    var y = m*(x - start[0]) + start[1];
                    y = Math.floor(y)
                    
                    

                    if ( (currentMap[x][y] && currentMap[x][y]["Bottom"]['textureIndex'] == "6")) {
                        return false;
                    }
                }
                return true;
                
            }
            function createLight(tileId,brightness) {
                var light = document.getElementById(tileId).querySelector(".Light");
                light.style.background = "#000";
                light.style.opacity = 1-brightness;
            }
            function lightSource(source,brightness) {
                source = source.split(",");
                for (var i = 0; i < currentMap.length; i++) {
                   for (var j = 0; j < currentMap[0].length; j++) {
                        var distance = (i!=source[0] || j!=source[1])?((((source[0]-i)**2+(source[1]-j)**2))**.5):.5;
                        
                        if (currentMap[i][j]["Bottom"]['textureIndex'] != 8) {
                            var isBright = true;
                            /*
                             var isBright = false;
                            if (i < source[0]) {
                                isBright = createLine([i,j],source)
                            }
                            if (i >= source[0]) {
                                isBright = createLine(source,[i,j])
                            }
                            */
                          
                          if (isBright) {
                              createLight(i+","+j,brightness/(distance+1)**1)
                          } else {
                              createLight(i+","+j,0);
                          }
                            
                            
                            
                        
                        }
                        
                        
                }
                }
            }
            
            function toggleSettings() {
                
                document.getElementById('settings').style.width=(isSettingsOpen?"0px":"100vw");
                document.getElementById('settings').style.fontSize=(isSettingsOpen?"0px":"10px");
                document.getElementById('settings').style.border=(isSettingsOpen?"":"solid rgb(212,175,55) 5px");
                document.getElementById('settings_span').querySelectorAll('input').forEach((Item) => {Item.style.display=(!isSettingsOpen)?"flex":"none";Item.style.width=(!isSettingsOpen)?"80px":"0px";Item.style.height=(!isSettingsOpen)?"20px":"0px";});
                document.getElementById('gear').classList.toggle('gearRotate');
                isSettingsOpen = !isSettingsOpen;
            }
            function initializeMap() {
                document.getElementById('canvas').style.gridTemplate = "repeat("+viewDiameter+",minmax(0, 1fr)) / repeat("+viewDiameter+",minmax(0, 1fr))";
                document.getElementById('canvas').innerHTML = "";  
                for (var i = 0; i < viewDiameter; i++) {
                    for (var j = 0; j < viewDiameter; j++) {
                        var tile = Object.assign(document.createElement('div'),{id:(j+","+i),classList:"tile"});
                        tile.dataset.manhattan = Math.abs(j - viewRadius) + Math.abs(i - viewRadius);
                        objectTypes.forEach((object) => {tile.appendChild(Object.assign(document.createElement('div'),{classList:object}))});
                        document.getElementById('canvas').appendChild(tile);
                    }
                }
                document.getElementById('dialogue').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('inventory').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                //document.getElementById('page').style.backgroundImage = 'url("'+tileObjects[13]['icon']+'")';
                scaleTextures();
                document.getElementById("canvas").querySelectorAll('.tile').forEach((Item) => {
                    Item.addEventListener("click", () => {clickTile(Item.id);Item.blur();});
                    Item.addEventListener("touchstart", () => {document.getElementById(Item.id).classList.add("inspectionLoad");this.touchStart = event.touches[0];clearTimeout(this.longPressTimeout);this.longPressTimeout = setTimeout(() => {toggleActions(Item.id);document.getElementById(Item.id).classList.remove("inspectionLoad");}, 1000);});
                    Item.addEventListener("touchend", () => {document.getElementById(Item.id).classList.remove("inspectionLoad");clearTimeout(this.longPressTimeout)});
                    Item.addEventListener("contextmenu", function(ev){ev.preventDefault();toggleActions(Item.id)});
                });
            }
            var confirmationCoordinates = 0;
            function isValidMove(coordinates) {
                var target = currentMap[coordinates[0]][coordinates[1]];

                    var range = currentMap[viewRadius][viewRadius]["Creature"]["equipment"][0]?(currentMap[viewRadius][viewRadius]["Creature"]["equipment"][0]['range']):1;
                    if ((target["Bottom"]["textureIndex"] != 8) && ((document.getElementById(coordinates[0]+","+coordinates[1]).dataset.manhattan <= range && target["Creature"] !== undefined) || document.getElementById(coordinates[0]+","+coordinates[1]).dataset.manhattan <= 1)) {
                    if (target["Terrain"] && target["Terrain"]["warning"] != "" && target["Creature"] === undefined) {
                         createModal("<p>"+target["Terrain"]["warning"]+"</p><button onclick = 'this.parentElement.parentElement.remove();sendRequest(`?sendAttack=`+encodeURIComponent(confirmationCoordinates));'>Yes</button><button onclick = 'this.parentElement.parentElement.remove();disableMovement=false;'>No</button>");
confirmationCoordinates = coordinates;
                        return false
                    }
                    if (target["Decor"] && target["Decor"]["warn"] == "Yes"  && target["Creature"] === undefined) {
                         createModal("<p>"+target["Decor"]["warning"]+"</p><button onclick = 'this.parentElement.parentElement.remove();sendRequest(`?sendAttack=`+encodeURIComponent(confirmationCoordinates));'>Yes</button><button onclick = 'this.parentElement.parentElement.remove();disableMovement=false;'>No</button>");
confirmationCoordinates = coordinates;

                        return false
                        
                    }
                        
                        
                        
                        if ((!target["Terrain"] && target["Bottom"]['textureIndex'] != "8") || (target["Terrain"] && !target["Terrain"]["passable"] && target["Decor"]) || target["Terrain"]) {
                            return true
                        }
                    }
                
                return false
            }
            function toggleInspect(tileId, dontOpen = ""){
                if (tileId == viewRadius+","+viewRadius && !inspecting) {
                    toggleInventory();
                    if (inventoryOpened) {
                    return;
                    }
                }
                var tile = currentMap[tileId.split(",")[0]][tileId.split(",")[1]]
                if (inspecting) {
                    document.getElementById(inspecting).classList.remove('inspecting');
                }
                if (inspecting == tileId || tile['Bottom']['textureIndex'] == 8 || !tileId) {
                    document.getElementById('inspection').style.width = "0px";
                    document.getElementById('inspection').innerHTML = "";
                    inspecting = false;
                } else {
                    document.getElementById('inspection').style.width = "50%";
                    document.getElementById(tileId).classList.add('inspecting');
                    inspecting  = tileId;
                }
                return tile;
            }                                           
            function inspectObject(tileArray,tileId) {
                var buffer = "";
                var outerDiv = false;
                if (tileArray !=null && typeof tileArray != "string") {
                    Object.keys(tileArray).forEach((object) => {
                        if (object == "Bottom") {
                            return
                        }
                        outerDiv = (object == "Creature" || object == "Item" || object == "Terrain" || object == "Decor");
                        if (outerDiv) {
                            buffer += "<div>";
                        }
                        if ((!Array.isArray(tileArray[object]) && typeof tileArray[object] != "object")|| (Array.isArray(tileArray[object]) && tileArray[object].length)){
                            if (object != "textureIndex") {
                                buffer += "<p>"+object+": "+tileArray[object]+"</p>";
                            } else {
                                if (tileArray[object] != "8") {
                                    buffer += "<img src = '"+tileObjects[tileArray[object]]['icon']+"'>";
                                }
                            }     
                            
                        } else if (typeof tileArray[object] == "object" && tileArray[object] != null && tileArray[object] != "") {
                            buffer  += "<p class = 'center'>"+object+"</p>";
                        } else {
                            buffer  += "<p>"+object+": None</p>";
                        }
                        buffer+= "<div>"
                        if (tileArray[object] !=null && typeof tileArray[object] != "string" && typeof tileArray[object] != "number")  {
                            Object.keys(tileArray[object]).forEach((attribute) => {
                                if (typeof tileArray[object][attribute] == "object" && !Array.isArray(tileArray[object][attribute]) && tileArray[object][attribute] != null) {
                                        buffer  += inspectObject(tileArray[object][attribute],tileId);
                                } else if (Array.isArray(tileArray[object][attribute]) && tileArray[object][attribute] != null && tileArray[object][attribute].length > 0 && parseInt(attribute) !=0)  {
                                    if (typeof tileArray[object][attribute][0] != "object") {
                                        buffer += "<p>"+attribute+": "+tileArray[object][attribute]+"</p>";
                                    } else {
                                        buffer += "<p class = 'center'>"+attribute+"</p>";
                                    }
                                    for (var i = 0; i < tileArray[object][attribute].length; i++) {
                                         if (attribute == "abilities" || attribute == "inventory" && tileArray[object][attribute][i]['name'] != "Gold") {
                                            buffer += "<div>"+inspectObject(tileArray[object][attribute][i],tileId)+"<button class = 'use' onclick = 'selectedItem = `"+attribute+":"+i+"`;toggleInspect(`"+tileId+"`);createMessage(`dialogue`,`Click On A Target`,2);'>Use</button></div>";
                                        } else {
                                            buffer += "<div>"+inspectObject(tileArray[object][attribute][i],tileId)+"</div>";

                                        }
                                    }
                                } else if (!parseInt(attribute) && attribute != 0) {
                                    if (attribute != "textureIndex") {
                                        buffer += "<p>"+attribute+": "+tileArray[object][attribute]+"</p>";
                                    } else {
                                        if (tileArray[object][attribute] != "8") {
                                        buffer += "<img src = '"+tileObjects[tileArray[object][attribute]]['icon']+"'>";
                                        }
                                    }
                                }
                            });
                        }
                        buffer+= "</div>"
                    });
                    if (outerDiv) {
                            buffer += "</div>";
                        }
                } 
                return buffer.replace(/<[^/>][^>]*><\/[^>]+>/gim, "")
            }
            function inspectTile(tileId){
                document.getElementById("action").style.height = "0px";
                    document.getElementById("action").style.fontSize = "0px";
                     document.getElementById('action').innerHTML = "";
                    activeTile = 0;
                    isAction = false;
                var tile = toggleInspect(tileId);
                document.getElementById('inspection').innerHTML = "<button class = 'close' onclick = 'toggleInspect(`"+tileId+"`)'>X</button>";
                document.getElementById('inspection').innerHTML += inspectObject(tile, tileId);
            }
            function clickTile(tileId) {
                var coordinates = tileId.split(",");
                if (inspecting) {
                    toggleInspect(inspecting);
                } else {
                    directionHandler(coordinates)
                }
            }
            function displayManhattan(distance) {
                document.getElementById('canvas').querySelectorAll('.manhattan').forEach((object) => {object.classList.remove("manhattan")});
                for (var i = 0; i <= distance; i++){
                    document.getElementById('canvas').querySelectorAll(`[data-manhattan="`+i+`"]`).forEach((object) => {
                        var coordinates = object.id.split(",");
                        if (currentMap[coordinates[0]][coordinates[1]]['Bottom']['textureIndex'] != "8") {
                            object.querySelector('.Top').classList.add("manhattan")
                        }
                        
                        
                        
                    });
                }
            }
            function updateMap() {
                moveObject(document.getElementById('canvas'),0,0);
                for (var i = 0; i < viewDiameter; i++) {
                    for (var j = 0; j < viewDiameter; j++) {
                        objectTypes.forEach((object) => {

                            applyTexture(object,j+","+i,(currentMap[j][i] && object in currentMap[j][i])?currentMap[j][i][object]:defaults["default"]);});
                    }
                }
                //lightSource(viewRadius+","+viewRadius,1);
            }
            function toggleAscii() {
                 document.getElementById("canvas").style.background = (asciiMode)?"":"white";
                 asciiMode = !asciiMode;
                 updateMap();
            }
            function toggleResolution() {
                isLowResolution = !isLowResolution;
                updateMap();
            }
            function applyTexture(type,tileId, object) {
                var selectedElement = document.getElementById(tileId).querySelector('.'+type);
                selectedElement.innerHTML = "";
                moveObject(selectedElement,0,0);
                if (type == "Light") {
                    createLight(tileId,object['intensity'])
                }
                
                if (!isLowResolution) {
                    selectedElement.style.background = "";
                    selectedElement.style.borderRadius = "";
                    selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']][asciiMode?"ascii":"icon"]+'")';
                } else {
                    selectedElement.style.background = tileObjects[object['textureIndex']]["color"];
                    if (type == "Creature") {
                        selectedElement.style.borderRadius = "50%";
                    }
                } 
                if (type == "Creature" && object['textureIndex'] != "8") {
                    selectedElement.innerHTML = currentMap[tileId.split(",")[0]][tileId.split(",")[1]]['Creature']['hp'];
                }
                if (type == "Terrain" && object['textureIndex'] != "8" && currentMap[tileId.split(",")[0]][tileId.split(",")[1]]['Terrain']['damaged']) {
                    selectedElement.innerHTML = currentMap[tileId.split(",")[0]][tileId.split(",")[1]]['Terrain']['hp'];
                }
                if (type == "Decor" && object['textureIndex'] != "8") {
                    var decor = currentMap[tileId.split(",")[0]][tileId.split(",")[1]]['Decor'];
                    if ((decor['name']).includes("Shop")) {
                    selectedElement.innerHTML = decor['hp'];
                    }
                    if (typeof(decor['hp']) == typeof("") && decor['hp'].includes(",") && currentLevel == 0){
                        selectedElement.innerHTML = currentMap[tileId.split(",")[0]][tileId.split(",")[1]]['Decor']['hp'].split(",")[1];
                    }
                }
            }
            function scaleTextures() {
                document.getElementById('canvas').style.height = document.getElementById('canvas').style.width = Math.min(window.innerWidth,window.innerHeight);
            }
            function uuidv4() {
                return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>(+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16));
            }
            function createMessage(type,message,time,uuid = uuidv4()) {
                if (!document.getElementById(type).innerHTML.includes(message)) {
                    document.getElementById(type).innerHTML = ((type == "alert")?document.getElementById(type).innerHTML:"")+"<p id = '"+uuid+"'>"+message+"</p>";
                    setTimeout(function() {if (document.getElementById(uuid)){document.getElementById(uuid).remove()}}, time*1000);
                }
                return uuid;
            }
            var selectedItem = 0;
            function toggleInventory() {
                document.getElementById('inspection').style.width = "0px";
                    document.getElementById('inspection').innerHTML = "";
                    inspecting = false;
                if (!inventoryOpened) {
                    
                   if (activeTile) {
                    document.getElementById("action").style.height = "0px";
                     document.getElementById('action').innerHTML = "";
                    activeTile = 0;
                    isAction = false;
                }
                    
                    var player =  currentMap[viewRadius][viewRadius]["Creature"];
                    var inventory = currentMap[viewRadius][viewRadius]["Creature"]["inventory"];
                    
                    var inventoryBuffer = "";
                    if (inventory.length > 0) {
                    inventoryBuffer = "<br><p>Inventory</p><span>";
                    
                    for (var i = 0; i < inventory.length; i++) {
                        item = inventory[i];
                        var useButton = (item['name'] != "Gold")?"<button class = 'use' onclick = 'selectedItem = `Inventory:"+i+"`;toggleInventory();createMessage(`dialogue`,`Click On A Target`,2);'>Use</button>":"";
                         inventoryBuffer += "<span><p>"+item['name']+"</p><img src = '"+tileObjects[item['textureIndex']]['icon']+"'><p>"+item['amount']+"</p>"+useButton+"</span>";

                    }
                    inventoryBuffer += "</span>";
                    }
                     var equipmentBuffer = "";
                    if (player['equipment'].length > 0) {
                    equipmentBuffer = "<br><p>Equipment</p><span>";
                    
                    for (var i = 0; i < player['equipment'].length; i++) {
                            var useButton = "<button class = 'use' onclick = 'selectedItem = `Equipment:"+i+"`;toggleInventory();createMessage(`dialogue`,`Click On A Target`,2);'>Unequip</button>";

                         equipmentBuffer += "<span><p>"+player['equipment'][i]['name']+"</p><img src = '"+tileObjects[player['equipment'][i]['textureIndex']]['icon']+"'><p>"+player['equipment'][i]['slot']+" | "+player['equipment'][i]['type']+"</p>"+useButton+"</span>";

                    }
                    equipmentBuffer += "</span>";
                    }
                    
                    var abilityBuffer = "";
                    if (player['abilities'].length > 0) {
                    abilityBuffer = "<br><p>Abilities</p><span>";
                    
                    for (var i = 0; i < player['abilities'].length; i++) {
                         abilityBuffer += "<span><p>"+player['abilities'][i]['name']+"</p><img src = '"+tileObjects[player['abilities'][i]['textureIndex']]['icon']+"'><button class = 'use' onclick = 'selectedItem = `abilities:"+i+"`;toggleInventory();createMessage(`dialogue`,`Click On A Target`,2);'>Use</button></span>";

                    }
                    abilityBuffer += "</span>";
                    }
                    
                    var statusBuffer = "";
                    if (player['status_effects'].length > 0) {
                        statusBuffer += "<p id = 'status_effects'>" 
                    for (var i = 0; i < player['status_effects'].length; i++) {
                         statusBuffer += player['status_effects'][i]['status_type'];
                    }
                    statusBuffer += "</p><br>" 
                    }
                    
                    
                    
                     var buffer = statusBuffer+'<p>'+player['name']+' | '+player['race']+'</p>';

                    
                    buffer += "<img src = '"+tileObjects[player['textureIndex']]['icon']+"'>";

                     buffer += '<p>Score: '+player['score']+' LVL: '+player['level']+' XP: '+player['xp']+'/'+player['level']*20+'</p>';
                     buffer += '<br><p>Cunning: '+player['cunning']+' Fitness: '+player['fitness']+' Magic: '+player['magic']+'</p>';
                   document.getElementById('inventory').innerHTML += '<span id = "playerCard"><button onclick = "toggleInventory();">X</button>'+buffer+abilityBuffer+inventoryBuffer+equipmentBuffer+'<button onclick = "inspectTile(viewRadius+`,`+viewRadius, true);">Show More</button></span>';
                }  else {
                     document.getElementById('inventory').innerHTML = "";
                }
                document.getElementById('inventory').style.height = (inventoryOpened)?"0":"100svh";
                document.getElementById('inventory').style.fontSize = (inventoryOpened)?"0":"40px";
                inventoryOpened = !inventoryOpened;
            }
            var keyFunction = "";
            function changeKeyBind(key) {
                if (!keyFunction.includes("Movement")) {
                keyBinds[keyFunction] = key;
                document.getElementById(keyFunction+"Button").innerHTML = key;
                } else {
                    var movementIndex = parseInt(keyFunction.split(",")[1])
                    keyBinds[keyFunction.split(",")[0]][parseInt(keyFunction.split(",")[1])] = key;
                    document.getElementById((keyFunction.split(",")[0])+"Button"+keyFunction.split(",")[1]).innerHTML = key;
                }
                keyFunction = false;
                localStorage.setItem("keyBinds",JSON.stringify(keyBinds));
            }
            function toggleKeyBind() {
                document.getElementById('keyBind').style.height = (keyBindOpened)?"0":"100svh";
                document.getElementById('keyBind').style.fontSize = (keyBindOpened)?"0":"20px";
                document.getElementById('keyBind').style.border = (keyBindOpened)?"0":"solid rgb(212,175,55) 5px";
                if (!keyBindOpened) {
                    toggleSettings();
                    document.getElementById('keyBind').innerHTML = "<button onclick = 'toggleKeyBind()'>X</button>";
                    Object.keys(keyBinds).forEach((keyFunction) => {
                        if (keyFunction != "Movement") {
                        document.getElementById('keyBind').innerHTML += "<p>"+keyFunction+"</p><button id = '"+keyFunction+"Button' onclick = 'keyFunction = `"+keyFunction+"`'>"+keyBinds[keyFunction]+"</button>";
                        
                        } else {
                             document.getElementById('keyBind').innerHTML += "<p>"+keyFunction+"</p>";
                             for (var i = 0; i < keyBinds[keyFunction].length; i++) {
                                 document.getElementById('keyBind').innerHTML += "<button id = '"+keyFunction+"Button"+i+"' onclick = 'keyFunction = `"+keyFunction+","+i+"`'>"+keyBinds[keyFunction][i]+"</button>";
                            }
                        }
                    });
                    document.getElementById('keyBind').innerHTML += "<button onclick = 'resetKeyBinds();keyBindOpened=false;toggleKeyBind();'>Reset</button>";
                } else {
                    document.getElementById('keyBind').innerHTML = "";
                }
                keyBindOpened = !keyBindOpened;
            }
            function resetKeyBinds() {
                keyBinds = {"Inventory":"KeyE","Settings":"Escape","Attack":"Space","Movement":["ArrowRight","ArrowDown","ArrowLeft","ArrowUp","KeyD","KeyS","KeyA","KeyW"]};
                localStorage.removeItem("keyBinds");
            }
            function playSound(index) {
                if (playAudio) {
                    if (!sfx[index].pasued) {
                        sfx[index].pause();
                        sfx[index].currentTime = 0;
                    }
                    sfx[index].volume = sfxVolume/100;
                    sfx[index].play();
                }
            }
            function applyEffects(target, type, duration) {
                if (type == "damaged") {
                    target.style.backgroundImage = "url('https://8bitdogsol.dog/images/f121eab4be5ed47f5a67b9ee8ba2c7ca.gif')";
                }
                
                if (type == "ability") {
                    
                    target.style.backgroundImage = "url('https://fathomless.io/assets/images/ability.gif')";
                }
            }
            function loadTrack() {
                if (playMusic) {
                    if (music) {
                 music.pause();
                    }
                 music = new Audio('https://fathomless.io/assets/audio/track'+currentLevel+'.mp3');
                 music.volume = musicVolume/100;
                            music.loop = true;
                            
                            music.currentTime = (songPosition)?songPosition:0;
                            music.play();
                }
            }
                            var statusPoints = {"cunning":0,"fitness":0,"magic":0,"total":0};
                            var skills = ['One-Handed Blades', 'One-Handed Axes', 'One-Handed Maces', 'Two-Handed Blades', 'Two-Handed Axes', 'Two-Handed Maces', 'Polearms', 'Slings', 'Bows', 'Elementalism', 'Cursing', 'Enhancement', 'Transmutation', 'Summoning', 'Dual-Wielding', 'Memory', 'Search', 'Hide', 'Lockpicking', 'Disarm Trap'];
                                
                            
            
            var race = "";
            var totalSkillPoints = 0;
            
            function updateLevelUp(status, direction) {
                    var pointsUsed = statusPoints['cunning'] + statusPoints["fitness"] + statusPoints["magic"];

                    if (status == "cunning" || status == "fitness" || status == "magic") {
                        statusPoints[status] += (statusPoints[status] + direction >= 0 && pointsUsed + direction <= 1)?direction:0;
                        document.getElementById(status).innerHTML = statusPoints[status];
                        document.getElementById('remaining_points').innerHTML = 1 - (statusPoints['cunning'] + statusPoints["fitness"] + statusPoints["magic"]);
                        
                    } else if (status != "submit") {
                        if (totalSkillPoints + direction <= statusPoints['total'] && totalSkillPoints + direction >= 0 && parseInt(document.getElementById(status).innerHTML) + direction >= 0) {
                            totalSkillPoints += direction;
                            document.getElementById(status).innerHTML = parseInt(document.getElementById(status).innerHTML) + direction;
                        
                            document.getElementById('remaining_skill_points').innerHTML = statusPoints["total"] - totalSkillPoints;
                        }
                            
                            
                            
                        
                    } else {
                          
                        var skillSend = "";
                        for (var i = 0; i < skills.length; i++) {
                            skillSend += document.getElementById(skills[i]).innerHTML;
                            if (i != skills.length - 1) {
                                skillSend += ",";
                            }
                        }
                                                
                        sendRequest("?levelUp&cunning="+encodeURIComponent(statusPoints['cunning'])+"&fitness="+encodeURIComponent(statusPoints['fitness'])+"&magic="+encodeURIComponent(statusPoints['magic'])+"&skills="+encodeURIComponent(skillSend));
                    document.getElementById('modal').remove();
statusPoints = {"cunning":0,"fitness":0,"magic":0,"total":0};
                                                      totalSkillPoints = 0;
                        
                    }
                }
            function receiveMap(response) {
                console.log(`Time taken: `+(performance.now() - start)+` milliseconds`);
                if (response != "Timed Out") {
                    response = JSON.parse(response);
                } else {
                    createModal("<p>Timed Out</p><button onclick = 'location.href = `https://fathomless.io`'>Home</button>")
                }
                
                if (response['map_subset'].length != viewDiameter) {
                    viewDiameter = response['map_subset'].length;
                    viewRadius = Math.floor(viewDiameter/2)
                    initializeMap();
                }
                currentMap = response["map_subset"];
                var moved = [];
                var playerDamage = 0;
                var gameOver = 0

                response["turn_log"].forEach((update) => {
                    
                    if (update['type'] && update['type'] == "ability" && update['after'] && update['before']) {
                        applyEffects(document.getElementById((update['after'][0]+playerDirection[0])+","+(update['after'][1]+playerDirection[1])).querySelector(".Top"),"ability",.2)
                    }
                    if (update['type'] == "attack" &&update['after'] && update['before']) {
                        applyEffects(document.getElementById((update['after'][0]+playerDirection[0])+","+(update['after'][1]+playerDirection[1])).querySelector(".Top"),"damaged",.2)
                        if (update['after'][0] == viewRadius && update['after'][1] == viewRadius) {
                            playerDamage -= update['amount'];
                        }
                    }
                    if (update['race']) {
                        if (race != update['race']) {
                            race = update['race'];
                        }
                    }
                   
                    if (update['shop']) {
                        var shopContents = "<p>Buy:</p><hr>";
                        var contents = currentMap[viewRadius][viewRadius]['Decor']['inventory'];
                        for (var i = 0; i < contents.length; i++) {
                            var item = contents[i];
                            if (item['name'] != "Gold") {
                            shopContents += "<div><span><p>"+item['name']+"</p><img src = '"+tileObjects[item['textureIndex']]['icon']+"'></span><span><p>Cost: "+item['price']+"</p></span><button onclick = 'sendRequest(`?buy="+i+"`)'>Buy</button></div>"
                            }
                                
                            }
                        
                        playerInventory = currentMap[viewRadius][viewRadius]['Creature']['inventory'];
                        if (playerInventory.length > 1) {
                            shopContents += "<p>Sell:</p><hr>";
                        for (var i = 0; i < playerInventory.length; i++) {
                            var item = playerInventory[i];
                            if (item['name'] != "Gold") {
                            shopContents += "<div><span><p>"+item['name']+"</p><img src = '"+tileObjects[item['textureIndex']]['icon']+"'></span><span><p>Cost: "+item['price']+"</p></span><button onclick = 'sendRequest(`?sell="+i+"`)'>Sell</button></div>"
                            }
                                
                            }
                        }
                        
                        createModal("<p>"+currentMap[viewRadius][viewRadius]['Decor']['name']+"</p><div class = 'shop'>"+shopContents+"</div><button class = 'x' onclick = 'document.getElementById(`modal`).remove();'>X</button>");
                    }
                    if (update['level_up_menu']) {statusPoints
                        statusPoints['total'] = update['level_up_menu']['points'];
                        var levelUpMenu = "<p>New Level: "+update['level_up_menu']['level']+"</p>";
                        levelUpMenu += "<p>Remaining Status Points <span id = 'remaining_points'>"+(1-statusPoints['cunning']-statusPoints['fitness']-statusPoints['magic'])+"</span></p>";
                        levelUpMenu += "<p>Remaining Skill Points <span id = 'remaining_skill_points'>"+statusPoints['total']+"</span></p>";
                        levelUpMenu += "<button onclick = 'updateLevelUp(`submit`, 0);'>Submit</button>";
                        levelUpMenu += "<hr><span><p>Statuses</p><p>Current Cunning: "+currentMap[viewRadius][viewRadius]['Creature']['cunning']+"</p>";
                        levelUpMenu += "<div><button onclick = 'updateLevelUp(`cunning`, -1);'>-</button><p>Cunning <span id = 'cunning'>"+statusPoints['cunning']+"</span></p><button onclick = 'updateLevelUp(`cunning`, 1);'>+</button></div>";
                        levelUpMenu += "<p>Current Fitness: "+currentMap[viewRadius][viewRadius]['Creature']['fitness']+"</p>";
                        levelUpMenu += "<div><button onclick = 'updateLevelUp(`fitness`, -1);'>-</button><p>Fitness <span id = 'fitness'>"+statusPoints['fitness']+"</span></p><button onclick = 'updateLevelUp(`fitness`, 1);'>+</button></div>";
                        levelUpMenu += "<p>Current Magic: "+currentMap[viewRadius][viewRadius]['Creature']['magic']+"</p>";
                        levelUpMenu += "<div><button onclick = 'updateLevelUp(`magic`, -1);'>-</button><p>Magic <span id = 'magic'>"+statusPoints['magic']+"</span></p><button onclick = 'updateLevelUp(`magic`, 1);'>+</button></div>";
                        levelUpMenu += "<hr><p>Skills</p>";
                        for (var i = 0; i < skills.length; i++) {
                            levelUpMenu += "<p>Current "+skills[i]+": "+currentMap[viewRadius][viewRadius]['Creature']['skills'][i]+"</p>";
                            levelUpMenu += "<div><button onclick = 'updateLevelUp(`"+skills[i]+"`, -1);'>-</button><p>"+skills[i]+" <span id = '"+skills[i]+"'>0</span></p><button onclick = 'updateLevelUp(`"+skills[i]+"`, 1);'>+</button></div>";

                        }
                        
                        
                        
                        createModal(levelUpMenu+"</span>","levelUpMenu");
                    }
                    if (update['level_up']) {
                        if (document.getElementById('modal')) {
                            document.getElementById('modal').remove();
                        }
                        statusPoints = {"cunning":0,"fitness":0,"magic":0,"total":0};
                        playSound(9)
                    }
                    if (update['level']) {
                        currentLevel = update['level'].split(",");
                    currentLevel = parseInt(currentLevel[0].split(".")[0]);
                    }
                    if (update['type'] == "game_over") {
                        gameOver = update['game_log'];
                     }
                    
                    if (update['type'] == "movement" && update['before'] && update['after']) {
                        var tileId = (update['before'][0]+playerDirection[0])+","+(update['before'][1]+playerDirection[1]);
                        if (document.getElementById(tileId)) {
                        var direction = [update['after'][0] - update['before'][0],update['after'][1] - update['before'][1]];                    
                        var creature = document.getElementById(tileId).querySelector(".Creature");
                        
                        moveObject(creature,direction[0],direction[1])
                        moved.push(creature);
                    }
                    }
                });
                if (playerDamage) {
                    createMessage("alert",(playerDamage)+"<img src = '"+tileObjects[16]['icon']+"'>",1);
                }
                setTimeout(function(){ 
                    updateMap();
                    if (!document.getElementById('levelUpMenu')) {
                        disableMovement = false;
                    }
                    if (gameOver) {
                        var endMessage = (currentLevel == 23)?"Congratulations, You Win!":"Game Over!";
                        if (currentLevel != 23) {
                            playSound(5)
                        }
                        createModal("<p>"+endMessage+"</p><p>Score "+currentMap[viewRadius][viewRadius]['Creature']['xp']+"</p><button onclick = 'location.href = `https://fathomless.io/character/`;'>Play Again</button><span class = 'log'>Game Log: "+ gameOver+"</span>");
                    }
                }, (moved)?100:0);
                createMessage("dialogue",response["message"],1);
                if (response['message'] == "target hit") {
                    playSound(7);
                }
                if (response['message'] == "target killed") {
                    playSound(1);
                }
                
                if (response["message"] == "Creature has moved"){playSound(0);}
                if (response["message"].includes("New Map")){playSound(4);

                 if (playMusic) {
                        music.pause();
                 }
                    currentLevel = response["message"].replace("New Map: Level ","").split(",");
                    currentLevel = parseInt(currentLevel[0].split(".")[0]);
                    
                     if (playMusic) {
                      music = new Audio('https://fathomless.io/assets/audio/track'+currentLevel+'.mp3');
                      music.volume = musicVolume/100;
                    music.loop = true;
                    music.play();
                    }
                    
                }
                if (response["message"].includes("Current HP")){playSound(8);}
                if (document.getElementById("cover")){
                    document.getElementById("cover").remove()
                }
                player = currentMap[viewRadius][viewRadius]["Creature"];
                displayManhattan((player.equipment[0])?player.equipment[0].range:1)
                if (inspecting) {
                    toggleInspect(inspecting)
                }
            }
            function playerUpdates(oldPlayer, newPlayer) {
                var healthChange = newPlayer.hp - oldPlayer.hp;
                if (healthChange){
                    createMessage("alert",(healthChange)+"<img src = '"+tileObjects[16]['icon']+"'>",1);
                }
            }
            
            function sendRequest(uri = "") {
                start = performance.now();
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        receiveMap(this.responseText);
                    }
                }
                if (uri == "") {
                    uri = "?fov="+encodeURIComponent(fov);
                } else {
                     uri += "&fov="+encodeURIComponent(fov);
                }
                xmlhttp.open("GET", "https://fathomless.io/sessionValidate/"+uri, true);
                xmlhttp.send();
            }
            function moveObject(gameObject,x,y) {
                var offset = document.getElementById("0,0").getBoundingClientRect().width;
                gameObject.style.zIndex = (x != 0 || y != 0)?1:"";
                gameObject.style.transition = (x != 0 || y != 0)?((gameObject.parentElement.id == viewRadius+","+viewRadius || gameObject.id == "canvas")?".2s":".1s"):"0s";
                gameObject.style.transitionTimingFunction = (x != 0 || y != 0)?"ease-in-out":"";
                gameObject.style.transform = (x != 0 || y != 0)?"translate("+(offset*x)+"px, "+(offset*y)+"px)":"";
            }
            function directionHandler(tileCoordinates) {
                if (playMusic && !music) {
                loadTrack();
            }
                if (isValidMove(tileCoordinates)){
                    if (document.getElementById("modal")) {
                    document.getElementById("modal").remove();}
                    if (!disableMovement) {
                        displayManhattan(-1);
                        sendRequest("?sendAttack="+encodeURIComponent(tileCoordinates)+(selectedItem?("&selected="+encodeURIComponent(selectedItem)):""));
                        
                        selectedItem = false;
                        disableMovement = true;
                        var player = document.getElementById(viewRadius+","+viewRadius).querySelector(".Creature");
                        var direction  = [(tileCoordinates[0]-viewRadius),(tileCoordinates[1]-viewRadius)];
                        
                        if (direction[0] == 0 && direction[1] == -1) {
                                player.style.backgroundImage = 'url("'+tileObjects[36]['icon']+'")';
                            } else if (direction[0] == 1 && direction[1] == 0) {
                                player.style.backgroundImage = 'url("'+tileObjects[37]['icon']+'")';
                            } else if (direction[0] == 0 && direction[1] == 1) {
                                player.style.backgroundImage = 'url("'+tileObjects[38]['icon']+'")';
                            } else if (direction[0] == -1 && direction[1] == 0) {
                                player.style.backgroundImage = 'url("'+tileObjects[39]['icon']+'")';
                            }
                        playerDirection = [0,0]
                        if (!currentMap[tileCoordinates[0]][tileCoordinates[1]]["Creature"] && (!currentMap[tileCoordinates[0]][tileCoordinates[1]]["Terrain"] || (currentMap[tileCoordinates[0]][tileCoordinates[1]]["Terrain"] && currentMap[tileCoordinates[0]][tileCoordinates[1]]["Terrain"]['passable'])) && (!currentMap[tileCoordinates[0]][tileCoordinates[1]]["Decor"] || (currentMap[tileCoordinates[0]][tileCoordinates[1]]["Decor"] && currentMap[tileCoordinates[0]][tileCoordinates[1]]["Decor"]["passable"]))) {
                            
                            

                            playerDirection = direction;
                            moveObject(player,direction[0],direction[1]);
                            moveObject(document.getElementById('canvas'),-direction[0],-direction[1]);
                            //setTimeout(() => {lightSource(tileCoordinates[0]+","+tileCoordinates[1],1);}, 100);
                            
                        }
                        document.body.appendChild(Object.assign(document.createElement('div'),{id:("cover")}));
                    } 
                }
            }
            var keyboardOnly = false;
            function toggleKeyboardOnly() {
                if (keyboardOnly) {
                    document.getElementById(keyboardOnly).classList.remove("selected");
                    keyboardOnly = false
                } else {
                    toggleSettings();
                    document.getElementById(viewRadius+","+viewRadius).classList.add("selected");
                    document.getElementById(viewRadius+","+viewRadius).focus();
                    keyboardOnly = viewRadius+","+viewRadius;
                }
                

            }
            document.addEventListener('keydown', (e) => {
                if (keyFunction) {
                    changeKeyBind(e.code);
                } else {
                    if (keyBinds["Movement"].indexOf(e.code) > -1 && !keyboardOnly && !disableMovement) {
                        var deg = (keyBinds["Movement"].indexOf(e.code)%4)*Math.PI/2;
                        target = [viewRadius+Math.round(Math.cos(deg)),viewRadius+Math.round(Math.sin(deg))]
                        directionHandler(target);
                    } else if (keyBinds["Movement"].indexOf(e.code) > -1 && keyboardOnly && !disableMovement) {
                        var deg = (keyBinds["Movement"].indexOf(e.code)%4)*Math.PI/2;
                        var currentSelect = keyboardOnly.split(',');
                        target = [parseInt(currentSelect[0])+Math.round(Math.cos(deg)),parseInt(currentSelect[1])+Math.round(Math.sin(deg))]
                        
                       if (document.getElementById(target[0]+","+target[1]).dataset.manhattan > currentMap[viewRadius][viewRadius]['Creature']['equipment'][0]['range']) {
                            deg = (keyBinds["Movement"].indexOf(e.code)%4)*90;
                                if (deg == 0) {
                                    target = [parseInt(currentSelect[0]) + 1,parseInt(currentSelect[1])+1];
                                    if (document.getElementById(target[0]+","+target[1]).dataset.manhattan > currentMap[viewRadius][viewRadius]['Creature']['equipment'][0]['range']) {
                                        target = [parseInt(currentSelect[0]) + 1,parseInt(currentSelect[1])-1];
                                    }

                                }
                                
                                if (deg == 90) {
                                    target = [parseInt(currentSelect[0]) + 1,parseInt(currentSelect[1])+1];
                                    if (document.getElementById(target[0]+","+target[1]).dataset.manhattan > currentMap[viewRadius][viewRadius]['Creature']['equipment'][0]['range']) {
                                        target = [parseInt(currentSelect[0]) - 1,parseInt(currentSelect[1])+1];
                                    }
                                    

                                }
                                if (deg == 180) {
                                    target = [parseInt(currentSelect[0]) - 1,parseInt(currentSelect[1])-1];
                                    if (document.getElementById(target[0]+","+target[1]).dataset.manhattan > currentMap[viewRadius][viewRadius]['Creature']['equipment'][0]['range']) {
                                        target = [parseInt(currentSelect[0]) - 1,parseInt(currentSelect[1])+1];
                                    }

                                }
                                if (deg == 270) {
                                    target = [parseInt(currentSelect[0]) - 1,parseInt(currentSelect[1])-1];
                                    if (document.getElementById(target[0]+","+target[1]).dataset.manhattan > currentMap[viewRadius][viewRadius]['Creature']['equipment'][0]['range']) {
                                        target = [parseInt(currentSelect[0]) + 1,parseInt(currentSelect[1])-1];
                                    }

                                }
                                
                                
                            }
                       
                       
                       
                        if (currentMap[target[0]][target[1]]["Bottom"]['textureIndex'] != "8" && (document.getElementById(target[0]+","+target[1]).dataset.manhattan <= currentMap[viewRadius][viewRadius]['Creature']['equipment'][0]['range'])) {
                            
                            
                            
                            document.getElementById(keyboardOnly).classList.remove("selected");
                            document.getElementById(target[0]+","+target[1]).classList.add("selected");
                            document.getElementById(target[0]+","+target[1]).focus();
                            keyboardOnly = target[0]+","+target[1];
                            
                            
                            
                            
                            
                            
                        }
                        
                        
                    }
                    if (e.code === keyBinds['Select'] && keyboardOnly)  {
                        
                        var target = keyboardOnly.split(",");
                        directionHandler(target);
                    }
                    if (e.code === keyBinds['Inventory'])  {
                        toggleInventory();
                    }
                    if (e.code === keyBinds['Settings'] && !inspecting && !keyBindOpened)  {
                        toggleSettings();
                    }
                    if (e.code === keyBinds['Settings'] && keyBindOpened)  {
                        toggleKeyBind();
                    }
                    if (e.code === keyBinds['Settings'] && inspecting)  {
                        document.getElementById('inspection').style.width = "0px";
                        document.getElementById('inspection').innerHTML = "";
                        document.getElementById(inspecting).classList.remove("inspecting");
                        inspecting = ""
                    }
                }
            });
            document.getElementById('settings').addEventListener('mouseenter', (e) => {clearTimeout(closeSetting);});
            document.getElementById('settings').addEventListener('mouseleave', (e) => {
                if (isSettingsOpen){
                    closeSetting = setTimeout(toggleSettings, 3000);
                }
            });
            document.querySelectorAll('input[type="range"]').forEach((Item) => {
                
                Item.addEventListener("input", () => {
                    if (Item.dataset.setting && Item.dataset.setting == "fovSlider") {
                        Item.value = (Item.value%2)?Item.value:Item.value-1;
                        if (Item.value != fov) {
                            fov = Item.value;
                            document.getElementById('fovLevel').innerHTML = "Current Fov: "+fov;
                            sendRequest();
                            localStorage.setItem("fov", fov)
                        }
                    }
                    
                    if (Item.dataset.setting && Item.dataset.setting == "sfxVolume") {
                        sfxVolume = Item.value;
                        document.getElementById('sfxVolume').innerHTML = "SFX Volume: "+(Item.value)+"%";
                         playAudio = !playAudio;
                         if (!sfx) {
                            sfx = [new Audio('https://fathomless.io/assets/audio/walking.mp3'),new Audio('https://fathomless.io/assets/audio/coin.mp3'),new Audio('https://fathomless.io/assets/audio/crash.mp3'),new Audio('https://fathomless.io/assets/audio/walk2.mp3'), new Audio('https://fathomless.io/assets/audio/woosh.mp3'), new Audio('https://fathomless.io/assets/audio/dead.mp3'), new Audio('https://fathomless.io/assets/audio/attack.mp3'), new Audio('https://fathomless.io/assets/audio/shoot.mp3'), new Audio('https://fathomless.io/assets/audio/hit.mp3'), new Audio('https://fathomless.io/assets/audio/kill.mp3')];
                            playAudio = true;
                             
                         }
                         if (sfx && sfxVolume == "0") {
                             playAudio = false;
                         }
                         if (sfx && sfxVolume != "0") {
                             playAudio = true;
                         }

                    }
                    
                    if (Item.dataset.setting && Item.dataset.setting == "musicVolume") {
                        musicVolume = Item.value;
                        document.getElementById('musicVolume').innerHTML = "Music Volume: "+(Item.value)+"%"
                        if (!music) {
                            music = new Audio('https://fathomless.io/assets/audio/track'+currentLevel+'.mp3');
                            music.loop = true;
                            music.play();
                            playMusic = true;
                            

                        }
                        if (music && musicVolume == "0") {
                            music.pause();
                            playMusic = false;
                        }
                        if (music && musicVolume != "0") {
                            music.play();
                            playMusic = true;
                        }
                        
                        music.volume = musicVolume/100;
                    }
                    
                })
                
                
                
            });
            
            setInterval(function () {localStorage.setItem("soundSettings",JSON.stringify([playMusic,musicVolume,playAudio,sfxVolume,(music)?music.currentTime:0]));}, 1000);
                                     

            document.querySelectorAll('button').forEach((Item) => {
                
                Item.addEventListener("click", () => {
                    Item.blur()
                    if (Item.dataset.setting && Item.dataset.setting == "settings_menu") {
                        toggleSettings();
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "toggleAudio") {
                        Item.innerHTML = (!playAudio)?"Mute SFX":"Play SFX"
                        playAudio = !playAudio;
                         if (sfx == 0 && playAudio) {
                            sfx = [new Audio('https://fathomless.io/assets/audio/walking.mp3'),new Audio('https://fathomless.io/assets/audio/coin.mp3'),new Audio('https://fathomless.io/assets/audio/crash.mp3'),new Audio('https://fathomless.io/assets/audio/walk2.mp3'), new Audio('https://fathomless.io/assets/audio/woosh.mp3'), new Audio('https://fathomless.io/assets/audio/dead.mp3'), new Audio('https://fathomless.io/assets/audio/attack.mp3'), new Audio('https://fathomless.io/assets/audio/shoot.mp3'), new Audio('https://fathomless.io/assets/audio/hit.mp3'), new Audio('https://fathomless.io/assets/audio/kill.mp3')];
                        }
                    }
                    
                    if (Item.dataset.setting && Item.dataset.setting == "toggleMusic") {
                        Item.innerHTML = (!playMusic)?"Mute Music":"Play Music"
                        playMusic = !playMusic;
                         if (!music && playMusic) {
                            music = new Audio('https://fathomless.io/assets/audio/track'+currentLevel+'.mp3');
                            music.volume = musicVolume/100;
                        }
                        if (playMusic) {
                            music.loop = true;
                            music.play();
                        } else {
                            music.pause();
                            music.currentTime = 0;
                        }
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "toggleAscii") {
                        Item.innerHTML = (!asciiMode)?"Enable Graphics":"Enable Ascii"
                        toggleAscii();
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "toggleResolution") {
                        toggleResolution();
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "saveGuest") {
                        window.location.href = "https://fathomless.io/saveGuest/";
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "keyBind") {
                        toggleKeyBind();
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "keyboardOnly") {
                        toggleKeyboardOnly();
                    }
                    if (Item.dataset.setting && Item.dataset.setting == "logout") {
                        window.location.replace("https://fathomless.io/logout/");
                    }
                });
            });
            document.body.onresize = function(){scaleTextures()};
        </script>
    </body>
</html>
