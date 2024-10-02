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
            }
            #page {
            width:100vw;
            height:100svh;
            }
            #page,#canvas .space,#inventory,#inventory div {
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
            #darkness {
                background:#333;
                position:absolute;
                mix-blend-mode: hard-light;
                display:flex;
                align-items:center;
                justify-content:center;
                
            }
            #darkness #hole {
                position:absolute;
                width: 60%;
	            height: 60%;
	            border-radius:50%;
            	background-color: gray;
            }
            .space div {
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
            #mobile_movement {
            position:absolute;
            bottom:0;
            right:0;
            display: none;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(3, 1fr);
            grid-column-gap: 0px;
            grid-row-gap: 0px;
            opacity:.5;
            z-index:1;
            }
            #mobile_movement button {
            width:100px;
            height:100px;
            }
            #mobile_movement button:nth-child(1) {grid-area: 1 / 2 / 2 / 3;}
            #mobile_movement button:nth-child(2) {grid-area: 2 / 1 / 3 / 2;}
            #mobile_movement button:nth-child(4) {grid-area: 3 / 2 / 4 / 3;}
            #mobile_movement button:nth-child(3) {grid-area: 2 / 3 / 3 / 4;}
            button, input {
            transition:.75s;
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            color:gold;
            font-size:20px;
            border:2px burlywood solid;
            background:saddlebrown;
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            }
            button, input[type=submit]:hover {
            transition:.75s;
            transform:scale(.9);
            }
        </style>
    </head>
    <body onresize="scaleTextures()">
        <div id = "page">
            <div id = "canvas"></div>
            <div id = "darkness"><div id = "hole"></div></div>
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
                <button data-setting = "onScreenControls">On-screen Controls</button>
                <button data-setting = "toggleAscii">Enable Ascii</button><button>Setting 4</button>
            </span>
        </div>
        <div id = "mobile_movement">
            <button data-direction = "ArrowUp">Up</button>
            <button data-direction = "ArrowLeft">Left</button>
            <button data-direction = "ArrowRight">Right</button>
            <button data-direction = "ArrowDown">Down</button>
        </div>
        <script>
            const tileObjects = JSON.parse('<?=file_get_contents("https://fathomless.io/json/objects.json")?>');
            const sfx = [new Audio('https://fathomless.io/assets/audio//walking.mp3'),new Audio('https://fathomless.io/assets/audio//coin.mp3'),new Audio('https://fathomless.io/assets/audio//crash.mp3'),new Audio('https://fathomless.io/assets/audio//walk2.mp3'), new Audio('https://fathomless.io/assets/audio//woosh.mp3'), new Audio('https://fathomless.io/assets/audio//dead.mp3'), new Audio('https://fathomless.io/assets/audio//attack.mp3'), new Audio('https://fathomless.io/assets/audio//shoot.mp3'), new Audio('https://fathomless.io/assets/audio//hit.mp3'), new Audio('https://fathomless.io/assets/audio//kill.mp3')];
            const arrowKeys = ["ArrowRight","ArrowDown","ArrowLeft","ArrowUp","KeyD","KeyS","KeyA","KeyW"];
            var playerInventory = JSON.parse('<?=file_get_contents("https://fathomless.io/json/inventory.json");?>');
            var start = objectTypes = disableMovement = onScreenControls = playAudio = closeSetting = isSettingsOpen = currentMap = viewDiameter = levelStep = inventoryOpened = textInputOpened = isEditMap = editRotation = previousPortal=asciiMode= 0;
            sendDirection();
            isMobile()?toggleOnScreenControls():"";
            function isMobile() {
                return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
            }
            function toggleOnScreenControls() {
                document.getElementById('mobile_movement').style.display = onScreenControls?"none":"grid";
                onScreenControls = !onScreenControls;
            }
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
                        var space = Object.assign(document.createElement('div'),{id:(j+","+i),classList:"space"})
                        objectTypes.forEach((object) => {space.appendChild(Object.assign(document.createElement('div'),{classList:object}))});
                        document.getElementById('canvas').appendChild(space);
                    }
                }
                document.getElementById('dialogue').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('inventory').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('page').style.backgroundImage = 'url("'+tileObjects[13]['icon']+'")';
                scaleTextures();
            }
            function updateMap() {
                for (var i = 0; i < viewDiameter; i++) {
                    for (var j = 0; j < viewDiameter; j++) {
                        objectTypes.forEach((object) => {applyTexture(object,j+","+i,currentMap[j][i][object]);});
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
                if (object.length != null ) {
                    if (object.length > 1) {
                        selectedElement.style.backgroundImage = 'url("https://forums.terraria.org/index.php?attachments/rainbow-treasure-bag-terraria-new-sprite-2-gif.223687/")';
                        selectedElement.style.transform = "rotate(0)";
                        return
                    } else {
                        object = object[0];
                    }
                }
                selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']][asciiMode?"ascii":"icon"]+'")';
                selectedElement.style.transform = (type == "entity" && object['rotation'] == 180)?('scaleX(-1)'):('rotate('+object['rotation']+'deg)');
            }
            function setDarkness(diameter,intensity) {
                document.getElementById('hole').style.height = document.getElementById('hole').style.width = (100*diameter/viewDiameter)+"%";
                document.getElementById('darkness').style.background = "#"+((Math.round(parseInt("0xFFFFFF", 16)*intensity/100)).toString(16)).padStart(6,"0");
                
            }
            function scaleTextures() {
                document.getElementById('canvas').style.height = document.getElementById('canvas').style.width = Math.min(window.innerWidth,window.innerHeight);
                document.getElementById('darkness').style.height = document.getElementById('darkness').style.width = Math.min(window.innerWidth,window.innerHeight);

                
            }
            function uuidv4() {
                return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>(+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16));
            }
            function createMessage(type,message,time) {
                var uuid = uuidv4();
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
                var loaderId = createMessage("alert","<img src = 'https://cdn.svgator.com/assets/landing-pages/static/css-loader/57579327-0-Loaders-3.svg'>",10);
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        var response = JSON.parse(this.responseText);
                        if (response['map_subset'].length != viewDiameter || objectTypes != Object.keys(response['map_subset'][0][0])) {
                            objectTypes = Object.keys(response['map_subset'][0][0]);
                            viewDiameter = response['map_subset'].length;
                            initializeMap();
                        }
                        currentMap = response["map_subset"];
                        updateMap();
                        createMessage("dialogue",response["message"],1);
                        disableMovement = false;
                        document.getElementById(loaderId).remove();
                        console.log(`Time taken: `+(performance.now() - start)+` milliseconds`);
                    }
                  }
                  var queryString = (direction !== "")?"="+encodeURIComponent(direction):"";
                  xmlhttp.open("GET", "https://fathomless.io/sessionValidate/?sendDirection"+queryString, true);
                  xmlhttp.send();
            }
            function directionHandler(keycode) {
                if (!disableMovement) {
                    start = performance.now();
                    sendDirection((arrowKeys.indexOf(keycode)%4)*90);
                    playSound(0);
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
            document.getElementById('settings').addEventListener('mouseenter', (e) => {
                clearTimeout(closeSetting);
            });
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
                    if (item.dataset.setting && item.dataset.setting == "onScreenControls") {
                        toggleOnScreenControls();
                    }
                });
            });
        </script>
    </body>
</html>
