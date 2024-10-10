<?php include("session.php");session_required();?>
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
            }
            #page {
            width:100vw;
            height:100svh;
            }
            #page,#canvas .tile,#inventory,#inventory div {
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
            #inventory {
            transition:.75s;
            height:0;
            width:100vw;
            position:absolute;
            flex-direction:column;
            font-size:0;
            color:white;
            }
            #inventory div {
            height:10%;
            width:100%;
            }
            #inventory div img {
            height:100%;
            margin:20px;
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
            #dialogue, #inventory {
            bottom:0;
            left:0;
            width:100vw;
            }
            #alert {
            padding:20px 0 20px 0;
            pointer-events: none;
            top:0;
            right:0;
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
            background:#333;
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
            width:100px;
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
            .manhattan {
                background: purple;
                opacity:.3;
            }
            .tile[data-manhattan="1"]:hover .light{
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
        </style>
    </head>
    <body onresize="scaleTextures()">
        <div id = "page">
            <div id = "canvas"></div>
        </div>
        <div id = "dialogue"></div>
        <div id = "alert"></div>
        <div id = "inventory"></div>
        <div id = "settings">
            <button data-setting = "settings_menu">
                <img id = "gear" src = "https://icons.veryicon.com/png/o/miscellaneous/xdh-font-graphics-library/gear-setting-1.png">
                </button>
            <span id = "settings_span">
                <button data-setting = "toggleAudio">Play SFX</button>
                <button data-setting = "toggleAscii">Enable Ascii</button>
            </span>
        </div>
        <script>
            const tileObjects = JSON.parse('<?=file_get_contents("https://fathomless.io/json/objects.json")?>');
            const sfx = [new Audio('https://fathomless.io/assets/audio//walking.mp3'),new Audio('https://fathomless.io/assets/audio//coin.mp3'),new Audio('https://fathomless.io/assets/audio//crash.mp3'),new Audio('https://fathomless.io/assets/audio//walk2.mp3'), new Audio('https://fathomless.io/assets/audio//woosh.mp3'), new Audio('https://fathomless.io/assets/audio//dead.mp3'), new Audio('https://fathomless.io/assets/audio//attack.mp3'), new Audio('https://fathomless.io/assets/audio//shoot.mp3'), new Audio('https://fathomless.io/assets/audio//hit.mp3'), new Audio('https://fathomless.io/assets/audio//kill.mp3')];
            const arrowKeys = ["ArrowRight","ArrowDown","ArrowLeft","ArrowUp","KeyD","KeyS","KeyA","KeyW"];
            const defaults = {"terrain":{"textureIndex":3},"light":{"textureIndex":8,"intensity":0},"default":{"textureIndex":8}};
            var playerInventory = JSON.parse('<?=file_get_contents("https://fathomless.io/json/inventory.json");?>');
            var start = disableMovement = playAudio = closeSetting = isSettingsOpen = currentMap = viewDiameter = levelStep = inventoryOpened = textInputOpened = isEditMap = editRotation = previousPortal=asciiMode= 0;
            var objectTypes = ["terrain","item","decor","entity","light"];
            sendDirection();
            function toggleSettings() {
                document.getElementById('settings').style.width=(isSettingsOpen?"0px":"100vw");
                document.getElementById('settings').style.fontSize=(isSettingsOpen?"0px":"20px");
                document.getElementById('gear').classList.toggle('gearRotate');
                isSettingsOpen = !isSettingsOpen;
            }
            function initializeMap() {
                document.getElementById('canvas').style.gridTemplate = "repeat("+viewDiameter+",minmax(0, 1fr)) / repeat("+viewDiameter+",minmax(0, 1fr))";
                document.getElementById('canvas').innerHTML = "";  
                for (var i = 0; i < viewDiameter; i++) {
                    for (var j = 0; j < viewDiameter; j++) {
                        var tile = Object.assign(document.createElement('div'),{id:(j+","+i),classList:"tile"});
                        tile.dataset.manhattan = Math.abs(j - Math.floor(viewDiameter/2)) + Math.abs(i - Math.floor(viewDiameter/2));
                        objectTypes.forEach((object) => {tile.appendChild(Object.assign(document.createElement('div'),{classList:object}))});
                        document.getElementById('canvas').appendChild(tile);
                    }
                }
                document.getElementById('dialogue').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('inventory').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('page').style.backgroundImage = 'url("'+tileObjects[13]['icon']+'")';
                scaleTextures();
                document.getElementById("canvas").querySelectorAll('.tile').forEach((item) => {
                    item.addEventListener("click", () => {clickTile(item.id)});
                    item.addEventListener("contextmenu", function(ev){ev.preventDefault();alert(item)});
                });
            }
            function clickTile(tileId) {
                var coordinates = tileId.split(",");
                if (document.getElementById(tileId).dataset.manhattan == 1) {
                    var index = Math.atan2(coordinates[1] - Math.floor(viewDiameter/2),coordinates[0] - Math.floor(viewDiameter/2))*2/Math.PI
                    directionHandler(arrowKeys[(index != -1)?index:3])
                }
            }
            function displayManhattan(distance) {
                document.getElementById('canvas').querySelectorAll('.manhattan').forEach((object) => {object.classList.remove("manhattan")});
                for (var i = 1; i <= distance; i++){
                    document.getElementById('canvas').querySelectorAll(`[data-manhattan*="`+i+`"]`).forEach((object) => {object.querySelector('.light').classList.add("manhattan")});
                }
            }
            function updateMap() {
                for (var i = 0; i < viewDiameter; i++) {
                    for (var j = 0; j < viewDiameter; j++) {
                        objectTypes.forEach((object) => {applyTexture(object,j+","+i,(currentMap[j][i][object])?currentMap[j][i][object]:(defaults[object]?defaults[object]:defaults["default"]));});
                    }
                }
            }
            function toggleAscii() {
                 document.getElementById("canvas").style.background = (asciiMode)?"":"white";
                 asciiMode = !asciiMode;
                 updateMap();
            }
            function applyTexture(type,tileId, object) {
                var selectedElement = document.getElementById(tileId).querySelector('.'+type);
                selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']][asciiMode?"ascii":"icon"]+'")';
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
            function toggleInventory() {
                document.getElementById('inventory').style.height = (inventoryOpened)?"0":"100svh";
                document.getElementById('inventory').style.fontSize = (inventoryOpened)?"0":"40px";
                inventoryOpened = !inventoryOpened;
            }
            function playSound(index) {
                if (playAudio) {
                    if (!sfx[index].pasued) {
                        sfx[index].pause();
                        sfx[index].currentTime = 0;
                    }
                    sfx[index].play();
                }
            }
            function sendDirection(direction = "") {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        var response = JSON.parse(this.responseText);
                        if (response['map_subset'].length != viewDiameter) {
                            viewDiameter = response['map_subset'].length;
                            initializeMap();
                        }
                        currentMap = response["map_subset"];
                        updateMap();
                        createMessage("dialogue",response["message"],1);
                        disableMovement = false;
                        console.log(`Time taken: `+(performance.now() - start)+` milliseconds`);
                        displayManhattan(0);
                        playSound(0);
                        if (document.getElementById("cover")){
                            document.getElementById("cover").remove()
                        }
                    }
                  }
                  var queryString = (direction !== "")?"="+encodeURIComponent(direction):"";
                  xmlhttp.open("GET", "https://fathomless.io/sessionValidate/?sendDirection"+queryString, true);
                  xmlhttp.send();
            }
            function directionHandler(keycode) {
                if (!disableMovement) {
                    document.body.appendChild(Object.assign(document.createElement('div'),{id:("cover")}));
                    start = performance.now();
                    sendDirection((arrowKeys.indexOf(keycode)%4)*90);
                    disableMovement = true;
                } 
            }
            document.addEventListener('keyup', (e) => {
                if (arrowKeys.indexOf(e.code) > -1) {
                    directionHandler(e.code)
                }
                if (e.code === "KeyE")  {
                    toggleInventory();
                }
            });
            document.getElementById('settings').addEventListener('mouseenter', (e) => {clearTimeout(closeSetting);});
            document.getElementById('settings').addEventListener('mouseleave', (e) => {
                if (isSettingsOpen){
                    closeSetting = setTimeout(toggleSettings, 3000);
                }
            });
            document.querySelectorAll('button').forEach((item) => {
                item.addEventListener("click", () => {
                    if (item.dataset.direction && arrowKeys.includes(item.dataset.direction)){
                        directionHandler(item.dataset.direction)
                    }
                    if (item.dataset.setting && item.dataset.setting == "settings_menu") {
                        toggleSettings();
                    }
                    if (item.dataset.setting && item.dataset.setting == "toggleAudio") {
                        item.innerHTML = (!playAudio)?"Mute SFX":"Play SFX"
                        playAudio = !playAudio;
                    }
                    if (item.dataset.setting && item.dataset.setting == "toggleAscii") {
                        item.innerHTML = (!asciiMode)?"Enable Graphics":"Enable Ascii"
                        toggleAscii();
                    }
                });
            });
        </script>
    </body>
</html>
