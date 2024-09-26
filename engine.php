<?php include("session.php");
if (!$uuid) {
    header("Location: https://fathomless.io/account/");
}
?>
<html>
    <head>
        <style>
            @import url('https://fonts.cdnfonts.com/css/8bit-wonder');
            * {
            font-family: '8BIT WONDER', sans-serif;
            }
            html, body {
            margin:0;
            padding:0;
            }
            #page {
            width:100vw;
            height:100svh;
            }
            #page,#canvas div,#inventory,#inventory div {
            display:flex;
            align-items:center;
            justify-content:center;
            background-size: contain;
            box-sizing: border-box;
            }
            #canvas {
            display: grid;
            }
            .item, .obstacle, .entity {
            position:absolute;
            display:none;
            background-size: contain;
            background-repeat: no-repeat;
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
        </style>
    </head>
    <body onresize="scaleTextures()">
        <div id = "page">
            <div id = "canvas"></div>
        </div>
        <div id = "dialogue"></div>
        <div id = "alert"></div>
        <div id = "inventory"></div>
        <script>
            const tileObjects = JSON.parse('<?=file_get_contents("https://fathomless.io/json/objects.json")?>');
            const sfx = [new Audio('https://fathomless.io/assets/audio//walking.mp3'),new Audio('https://fathomless.io/assets/audio//coin.mp3'),new Audio('https://fathomless.io/assets/audio//crash.mp3'),new Audio('https://fathomless.io/assets/audio//walk2.mp3'), new Audio('https://fathomless.io/assets/audio//woosh.mp3'), new Audio('https://fathomless.io/assets/audio//dead.mp3'), new Audio('https://fathomless.io/assets/audio//attack.mp3'), new Audio('https://fathomless.io/assets/audio//shoot.mp3'), new Audio('https://fathomless.io/assets/audio//hit.mp3'), new Audio('https://fathomless.io/assets/audio//kill.mp3')];
            const  arrowKeys = ["ArrowRight","ArrowUp","ArrowLeft","ArrowDown","KeyD","KeyW","KeyA","KeyS"];
            const objectTypes = ["tile","item","obstacle","entity"];
            var playerInventory = JSON.parse('<?=file_get_contents("https://fathomless.io/json/inventory.json");?>');
            var maps = {"level_1":JSON.parse('<?=file_get_contents("https://fathomless.io/cgi-bin/map.py?getMap=value");?>'),"level_2":JSON.parse('<?=file_get_contents("https://fathomless.io/json/map2.json")?>')};
            var viewSizeX = viewSizeY = playerCoordinates = currentMap = currentMapName = sizeX = sizeY = levelStep = inventoryOpened = textInputOpened = isEditMap = editRotation = previousPortal=asciiMode= 0;
            loadMap("level_1");
            setFov(5);
            function setFov(radius) {
                viewSizeX = viewSizeY = radius;
                updateMap();
            }
            function getPlayerCoordinate() {
                for (var i = 0; i < maps[currentMapName].length; i++) {
                    for (var j = 0; j < maps[currentMapName][0].length; j++) {
                        if (maps[currentMapName][i][j]['entity']['textureIndex'] == 0) {
                            return [i,j];
                        }
                    }
                }
            }
            function updateMap() {
                var createTiles = false;
                if (sizeX != viewSizeX || sizeY != viewSizeY) {
                    createTiles = true;
                    sizeX = viewSizeX;
                    sizeY = viewSizeY;
                    document.getElementById('canvas').style.gridTemplateColumns = "repeat("+sizeX+",minmax(0, 1fr))";
                    document.getElementById('canvas').style.gridTemplateRows = "repeat("+sizeY+",minmax(0, 1fr))";
                    document.getElementById('canvas').innerHTML = "";     
                }
                var topLeftCorner = [playerCoordinates[0] - Math.floor(viewSizeX/2),playerCoordinates[1] - Math.floor(viewSizeX/2)]
                for (var i = 0;i < sizeY; i++) {
                     for (var j = 0;j < sizeX; j++) {
                        if (createTiles) {
                            document.getElementById('canvas').innerHTML += '<div class="tile" id = "'+j+','+i+'"><div class = "entity"></div><div class = "item"></div><div class = "obstacle"></div></div>';
                        }
                        if (maps[currentMapName][topLeftCorner[0]+j] && maps[currentMapName][topLeftCorner[0]+j][topLeftCorner[1]+i]) {
                           applyTexture('tile',j+","+i,maps[currentMapName][topLeftCorner[0]+j][topLeftCorner[1]+i]['tile']);
                            applyTexture("item",j+","+i,maps[currentMapName][topLeftCorner[0]+j][topLeftCorner[1]+i]['item']);
                            applyTexture("obstacle",j+","+i,maps[currentMapName][topLeftCorner[0]+j][topLeftCorner[1]+i]['obstacle']);
                            applyTexture("entity",j+","+i,maps[currentMapName][topLeftCorner[0]+j][topLeftCorner[1]+i]['entity']);
                        } else {
                           applyTexture('tile',j+","+i,{"textureIndex":8,"rotation":0});
                            applyTexture("item",j+","+i,{"textureIndex":8,"rotation":0});
                            applyTexture("obstacle",j+","+i,{"textureIndex":8,"rotation":0});
                            applyTexture("entity",j+","+i,{"textureIndex":8,"rotation":0});
                        }
                    }
                }
                document.getElementById('dialogue').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('inventory').style.backgroundImage = 'url("'+tileObjects[12]['icon']+'")';
                document.getElementById('page').style.backgroundImage = 'url("'+tileObjects[13]['icon']+'")';
                scaleTextures();
            }
            function toggleAscii() {
                 document.getElementById("canvas").style.background = (asciiMode)?"":"white";
                 asciiMode = !asciiMode;
                 updateMap();
            }
            function applyTexture(type,tileId, object) {
                var selectedElement = (type == "tile")?document.getElementById(tileId):document.getElementById(tileId).querySelector('.'+type);
                if (object['textureIndex'] != 8) {
                     selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']][asciiMode?"ascii":"icon"]+'")';
                    selectedElement.style.transform = (type == "entity" && object['rotation'] == 180)?('scaleX(-1)'):('rotate('+object['rotation']+'deg)');
                } else {
                    selectedElement.style.backgroundImage = 'url()';
                    selectedElement.style.transform = "rotate(0)";
                }
            }
            function scaleTextures() {
                var windowMinimum = Math.min(window.innerWidth,window.innerHeight);
                var tileMinimum = Math.min(window.innerWidth/sizeX,window.innerHeight/sizeY);
                document.getElementById('canvas').style.height = tileMinimum*sizeY;
                document.getElementById('canvas').style.width = tileMinimum*sizeX;
                document.getElementById('canvas').querySelectorAll('div').forEach((item) => {item.style.height = item.style.width = tileMinimum;});
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
                
            }
            function toggleInventory() {
                document.getElementById('inventory').style.height = (inventoryOpened)?"0":"100svh";
                document.getElementById('inventory').style.fontSize = (inventoryOpened)?"0":"40px";
                inventoryOpened = !inventoryOpened;
            }
            function loadMap(name) {
                currentMapName = name;
                currentMap = maps[name];
                playerCoordinates = getPlayerCoordinate();
                updateMap();
            }
            function moveEntity(x,y,currentCoordinates,type,augmentation) {
                if (0 <= x && x < currentMap.length && 0 <= y && y < currentMap[0].length) {
                    currentMap[currentCoordinates[0]][currentCoordinates[1]]['entity'] = [currentMap[x][y]['entity'], currentMap[x][y]['entity'] = currentMap[currentCoordinates[0]][currentCoordinates[1]]['entity']][0];
                    if (playerCoordinates[0] == currentCoordinates[0] && playerCoordinates[1] == currentCoordinates[1]) {
                        playerCoordinates = [x,y];
                    }
                } 
            }
            function moveDirection(direction,x,y) {
                var deg = Math.PI*currentMap[x][y]['entity']['rotation']/180
                if (Math.floor(Math.cos(deg)) == direction[0] && Math.floor(Math.sin(deg)) == direction[1]) {
                    moveEntity(x + direction[0],y + direction[1],[x,y],currentMap[x][y]['entity']);
                }  else {
                    currentMap[x][y]['entity']['rotation'] = (Math.atan2(direction[1], direction[0])*180)/Math.PI;
                    var topLeftCorner = [playerCoordinates[0] - Math.floor(viewSizeX/2),playerCoordinates[1] - Math.floor(viewSizeX/2)];
                    if (Math.abs(x - playerCoordinates[0]) <= Math.floor(viewSizeX/2) && Math.abs(y - playerCoordinates[1]) <= Math.floor(viewSizeY/2)) {
                        applyTexture("entity",(x - topLeftCorner[0])+","+(y - topLeftCorner[1]),currentMap[x][y]['entity']);  
                    }
                }
                updateMap();
            }
            function playSound(index) {
                if (!sfx[index].pasued) {
                    sfx[index].pause();
                    sfx[index].currentTime = 0;
                }
                sfx[index].play();
            }
            function sendDirection(direction) {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        createMessage("dialogue",this.responseText,1);
                    }
                  }
                  xmlhttp.open("GET", "https://fathomless.io/sessionValidate/?sendDirection="+encodeURIComponent(direction), true);
                  xmlhttp.send();
            
            }
            document.addEventListener('keydown', (e) => {
                if (arrowKeys.indexOf(e.code) > -1) {
                    var newDirection = [Math.round(Math.cos((arrowKeys.indexOf(e.code)%4)*Math.PI/2))+0,-Math.round(Math.sin((arrowKeys.indexOf(e.code)%4)*Math.PI/2))+0];
                    sendDirection(((Math.atan2(newDirection[1], newDirection[0])*180)/Math.PI))
                    moveDirection(newDirection,playerCoordinates[0],playerCoordinates[1])
                    playSound(0);
                }
                if (e.code === "KeyE")  {
                    toggleInventory();
                }
                if (e.code === "KeyQ") {
                    toggleAscii();
                }
            });
        </script>
    </body>
</html>
