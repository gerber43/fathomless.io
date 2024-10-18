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
            #inspection {
                position:absolute;
                top:0;
                left:0;
                width:0;
                height:100vh;
                background:saddlebrown;
                overflow:scroll;
                color:rgb(212,175,55);
                -ms-overflow-style: none;
                scrollbar-width: none; 
                resize:both;
                cursor: move;
                
            }
            #inspection::-webkit-scrollbar {
                display: none;
            }
            #inspection button {
                position:absolute;
                top:0;
                right:0;
                width:30px;
                height:30px;
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
                margin:20px;

            }
            #inspection > div > div {
                width:80%;
            }
            #inspection div {
                padding:20px;
                border-radius:20px;
                border:solid rgb(212,175,55) 5px;
                margin:20px;

            }
            #inspection div p {
                word-wrap: break-word;
            }
            #inspection > p {
                text-align:center;
            }
            .inspecting {
                transition:.75s;
                border:#eee dotted 2px;
            }
            hr {
            width:90%;
            height:5px;
            background:rgb(212,175,55);
            border:none;
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
        <div id = "settings">
            <button data-setting = "settings_menu">
                <img id = "gear" src = "https://icons.veryicon.com/png/o/miscellaneous/xdh-font-graphics-library/gear-setting-1.png">
            </button>
            <span id = "settings_span">
            <button data-setting = "toggleAudio">Play SFX</button>
            <button data-setting = "toggleMusic">Play Music</button>
            <button data-setting = "toggleAscii">Enable Ascii</button>
            <button data-setting = "toggleResolution">Toggle Resolution</button>
            <?=($_SESSION['username'] == "Guest")?'<button data-setting = "saveGuest">Save Progress</button>':'';?>
            </span>
        </div>
        <div id = "inspection" draggable="true"></div>
        <script>
            const username = '<?=$_SESSION['username']?>';
            const tileObjects = JSON.parse('<?=file_get_contents("https://fathomless.io/json/objects.json")?>');
            const arrowKeys = ["ArrowRight","ArrowDown","ArrowLeft","ArrowUp","KeyD","KeyS","KeyA","KeyW"];
            const defaults = {"terrain":{"textureIndex":3},"light":{"textureIndex":8,"intensity":0},"default":{"textureIndex":8}};
            var inspecting = music = playMusic = sfx = isLowResolution = start = disableMovement = playAudio = closeSetting = isSettingsOpen = currentMap = viewDiameter  = inventoryOpened = asciiMode= 0;
            var objectTypes = ["terrain","item","decor","creature","light"];
            sendDirection();
            window.mobileCheck = function() {let check = false;(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);return check;};
            if (mobileCheck()){toggleResolution()}
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
                    item.addEventListener("contextmenu", function(ev){ev.preventDefault();inspectTile(item.id)});
                });
            }
            function inspectTile(tileId){
                var coordinates = tileId.split(",");
                var tile = currentMap[coordinates[0]][coordinates[1]]
                if (inspecting != tileId && tile['terrain']['textureIndex'] != 8) {
                    document.getElementById(tileId).classList.add('inspecting');
                if (!inspecting) {
                    
                    document.getElementById('inspection').style.width = "50%";
                } else {
                    document.getElementById(inspecting).classList.remove('inspecting');
                }
                
                //alert("Temporary Tile Inspection Menu: "+JSON.stringify(currentMap[coordinates[0]][coordinates[1]]));
                document.getElementById('inspection').innerHTML = "<button onclick = 'document.getElementById(\"inspection\").style.width = 0; document.getElementById(inspecting).classList.remove(\"inspecting\");inspecting = \"\"'>X</button>";
                
                Object.keys(tile).forEach((object) => {
                    if (tile[object]['name']) {
                    attributes = "";
                    Object.keys(tile[object]).forEach((attribute) => {
                        specialFormats = ["equipment","drop_table"];
                        if (!specialFormats.includes(attribute)) {
                                
                            
                        if (attribute == "textureIndex") {
                            attributes+="<img src = '"+tileObjects[tile[object][attribute]]['icon']+"'>"
                        } else {
                            
                            attributes+="<p><span>"+attribute + "</span> : "+tile[object][attribute]+"</p>"
                        }
                        } else {
                            var attributeArray = Object.keys(tile[object][attribute]).map((key) => tile[object][attribute][key]);
                            buffer = ""
                            for (var i = 0; i < attributeArray.length; i++) {
                                if (typeof(attributeArray[i]) == "object") {
                                    objectKeys = Object.keys(attributeArray[i]);
                                    for (var j = 0; j < objectKeys.length; j++) {
                                         if (objectKeys[j] == "textureIndex") {
                            attributes+="<img src = '"+tileObjects[attributeArray[i][objectKeys[j]]]['icon']+"'>"
                        } else {
                                        buffer += "<p>"+objectKeys[j]+" : "+attributeArray[i][objectKeys[j]]+"</p>";
                        }
                                    }
                                } else {
                                    buffer += "<p>"+attributeArray[i]+"</p>";
                                }
                                
                                
                                    

                            }
                            attributes+="<div><p><span>"+attribute + "</span> : </p><hr>"+buffer+"</div>";
                        }

                        
                        
                    })
                    document.getElementById('inspection').innerHTML += "<p>"+object+"</p><div>"+attributes+"</div>";
                    
                    }
                    
                });
                inspecting = tileId;
                } else {
                    if (inspecting) {
                     document.getElementById(inspecting).classList.remove('inspecting');
                    }
                    document.getElementById('inspection').style.width = "0px";
                                    document.getElementById('inspection').innerHTML = "";
inspecting = false;
                }
                
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
                    document.getElementById('canvas').querySelectorAll(`[data-manhattan="`+i+`"]`).forEach((object) => {object.querySelector('.light').classList.add("manhattan")});
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
            function toggleResolution() {
                isLowResolution = !isLowResolution;
                updateMap();
            }
            function applyTexture(type,tileId, object) {
                var selectedElement = document.getElementById(tileId).querySelector('.'+type);
                if (!isLowResolution) {
                    selectedElement.style.background = "";
                    selectedElement.style.borderRadius = "";
                    selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']][asciiMode?"ascii":"icon"]+'")';
                } else {
                    selectedElement.style.background = tileObjects[object['textureIndex']]["color"];
                    if (type == "creature") {
                        selectedElement.style.borderRadius = "50%";
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
                        if (response["message"] == "creature has moved"){playSound(0);}
                        if (response["message"].includes("New Map")){playSound(4);}
                        if (response["message"].includes("Current HP")){playSound(8);}
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
                if (e.code === "Escape" && !inspecting)  {
                    toggleSettings();
                }
                if (e.code === "Escape" && inspecting)  {
                    document.getElementById('inspection').style.width = "0px";
                    document.getElementById('inspection').innerHTML = "";
                    document.getElementById(inspecting).classList.remove("inspecting");
                    inspecting = ""
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
                         if (sfx == 0 && playAudio) {
                            sfx = [new Audio('https://fathomless.io/assets/audio/walking.mp3'),new Audio('https://fathomless.io/assets/audio/coin.mp3'),new Audio('https://fathomless.io/assets/audio/crash.mp3'),new Audio('https://fathomless.io/assets/audio/walk2.mp3'), new Audio('https://fathomless.io/assets/audio/woosh.mp3'), new Audio('https://fathomless.io/assets/audio/dead.mp3'), new Audio('https://fathomless.io/assets/audio/attack.mp3'), new Audio('https://fathomless.io/assets/audio/shoot.mp3'), new Audio('https://fathomless.io/assets/audio/hit.mp3'), new Audio('https://fathomless.io/assets/audio/kill.mp3')];
                        }
                    }
                    if (item.dataset.setting && item.dataset.setting == "toggleMusic") {
                        item.innerHTML = (!playMusic)?"Mute Music":"Play Music"
                        playMusic = !playMusic;
                         if (music == 0 && playMusic) {
                            music = [new Audio('https://fathomless.io/assets/audio/track1.mp3')];
                        }
                        if (playMusic) {
                            music[0].loop = true;
                            music[0].play();
                        } else {
                            music[0].pause();
                            music[0].currentTime = 0;
                        }
                    }
                    if (item.dataset.setting && item.dataset.setting == "toggleAscii") {
                        item.innerHTML = (!asciiMode)?"Enable Graphics":"Enable Ascii"
                        toggleAscii();
                    }
                    if (item.dataset.setting && item.dataset.setting == "toggleResolution") {
                        toggleResolution();
                    }
                    if (item.dataset.setting && item.dataset.setting == "saveGuest") {
                        window.location.href = "https://fathomless.io/saveGuest/";
                    }
                });
            });
            document.body.onresize = function(){scaleTextures()};
        </script>
    </body>
</html>
