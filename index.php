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
            #inventory,#textInput {
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
            #textInput {
                position:absolute;
                bottom:0;
                left:0;
                display:flex;
                align-items:start;
                justify-content:end;
                flex-direction:column-reverse;
            }
            #textInput textArea{
                height:5%;
                padding:0;
                margin:0;
                border:0;
                width:100vw;
                background:#222;
                color:white;
                outline: none;
                padding:0 20px 0 20px;
            }
            #textInput textArea:active {
                border:none;
                outline:none;
            }
            #alert p {
                display:flex;
                align-items:center;
                justify-content:center;
            }
            #text-display {
               display:flex;
                align-items:center;
                justify-content:center;
                flex-direction:column;
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
        <div id = "textInput"><textarea rows = "1"></textarea><div id = "text-display"></div></div>
        <script>
            const storyDialogue = JSON.parse('<?=file_get_contents("dialogue.json");?>');
            const tileObjects = JSON.parse('<?=file_get_contents("objects.json")?>');
            var playerInventory = JSON.parse('<?=file_get_contents("inventory.json");?>');
            var maps = {"level_1":JSON.parse('<?=file_get_contents("map.json");?>'),"level_2":JSON.parse('<?=file_get_contents("map2.json")?>')};
            var currentMapName = "level_1";
            var currentMap = maps[currentMapName];
            var playerCoordinates = [];
            var sizeX = sizeY = levelStep = inventoryOpened = textInputOpened = isEditMap = editRotation = previousPortal= 0;
            var editTypes = ["tile","item","obstacle","entity"];
            var textUpIndex = currentTexture = 1;
            var sfx = [new Audio('https://vintageautos.org/walking.mp3'),new Audio('https://vintageautos.org/coin.mp3'),new Audio('https://vintageautos.org/crash.mp3'),new Audio('https://vintageautos.org/walk2.mp3'), new Audio('https://vintageautos.org/woosh.mp3'), new Audio('https://vintageautos.org/dead.mp3'), new Audio('https://vintageautos.org/attack.mp3'), new Audio('https://vintageautos.org/shoot.mp3'), new Audio('https://vintageautos.org/hit.mp3'), new Audio('https://vintageautos.org/kill.mp3')];
            var arrowKeys = ["ArrowRight","ArrowUp","ArrowLeft","ArrowDown","KeyD","KeyW","KeyA","KeyS"];
            var viewSizeX = viewSizeY = 20;
            var blankTile = {"tile":{"textureIndex":8,"rotation":0},"item":{"textureIndex":8,"rotation":0},"obstacle":{"textureIndex":8,"rotation":0},"entity":{"textureIndex":"8","rotation":"0"}};
            updateMap();
            advanceStory(0,"player");
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
            function getEntityCoordinate() {
                var buffer = [];
                for (var i = 0; i < maps[currentMapName].length; i++) {
                    for (var j = 0; j < maps[currentMapName][0].length; j++) {
                        if (!maps[currentMapName][i]) {
                            console.log(i,j)
                        }
                        if (maps[currentMapName][i][j]['entity']['textureIndex'] != 8 && maps[currentMapName][i][j]['entity']['textureIndex'] != 0 && tileObjects[maps[currentMapName][i][j]['entity']['textureIndex']]['type'] != "projectile") {
                            buffer[i+","+j] = tileObjects[maps[currentMapName][i][j]['entity']['textureIndex']]['name'];
                        }
                    }
                }
                return buffer;
            }
            
            function updateMap() {
                playerCoordinates = getPlayerCoordinate();
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
                for (var i = 0;i<sizeY;i++) {
                     for (var j = 0;j<sizeX;j++) {
                        if (createTiles) {
                            document.getElementById('canvas').innerHTML += '<div onmouseout = "this.style.border = `none`" onmousedown = \'updateTexture(JSON.parse(`[`+this.id+`,\"`+currentMapName+`\"]`),editTypes[0])\' class="tile" id = "'+j+','+i+'"><div class = "entity"></div><div class = "item"></div><div class = "obstacle"></div></div>';
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
                updateInventory();
            }
            function updateTexture(coordinates,type) {if (isEditMap) {
                document.getElementById(coordinates[0]+","+coordinates[1]).style.border = "2px dashed white";}
                if (isEditMap){
                    if (currentTexture == 8 && maps[coordinates[2]][coordinates[0]][coordinates[1]][type]['textureIndex'] == 15) {
                        delete maps[coordinates[2]][coordinates[0]][coordinates[1]][type].link;
                    }
                    maps[coordinates[2]][coordinates[0]][coordinates[1]][type]['textureIndex'] = currentTexture;
                    maps[coordinates[2]][coordinates[0]][coordinates[1]][type]['rotation'] = editRotation;
                    applyTexture(type,coordinates[0]+","+coordinates[1],currentMap[coordinates[0]][coordinates[1]][type]);
                        
                        if (currentTexture == 15 && previousPortal == 0) {
                            previousPortal = coordinates
                            createMessage("dialogue","please place another portal",4);
                        } else if (currentTexture == 15 && previousPortal != 0) {
                            Object.assign(maps[coordinates[2]][coordinates[0]][coordinates[1]]['item'], { "link": previousPortal });
                            Object.assign(maps[previousPortal[2]][previousPortal[0]][previousPortal[1]]['item'], { "link": coordinates });
                            previousPortal = 0;
                        } 
                    }
             }
             function switchBrush(direction) {
                if (typeof direction == typeof -1) {
                    for (var i = 0; i<tileObjects.length;i++) {
                        currentTexture = ((currentTexture+direction % tileObjects.length) + tileObjects.length) % tileObjects.length;
                        if (tileObjects[currentTexture]["type"] == editTypes[0]) {
                            break;
                        }
                    }
                    if (document.getElementById('editBrush')) {
                    document.getElementById('editBrush').innerHTML = editTypes[0] + "<img style = 'transform:rotate("+editRotation+"deg);' src = '"+tileObjects[currentTexture]['icon']+"'>";
                 
                    }
                    } else {
                     if (editTypes[0] != "tile") {
                     currentTexture = parseInt(direction);
                     if (document.getElementById('editBrush')) {
                     document.getElementById('editBrush').innerHTML = editTypes[0]+" Delete";
                     }
                     }
                 }
             }
             var asciiMode = false;
             function toggleAscii() {
                 if (asciiMode) {
                                          document.getElementById("canvas").style.background ="";

                 } else {
                     document.getElementById("canvas").style.background ="white";
                 }
                 asciiMode = !asciiMode;
                 updateMap();
             }
            function applyTexture(type,tileId, object) {
                if (document.getElementById(tileId)) {
                var topLeftCorner = [playerCoordinates[0] - Math.floor(viewSizeX/2),playerCoordinates[1] - Math.floor(viewSizeX/2)];
                var selectedElement = (type == "tile")?document.getElementById(tileId):document.getElementById(tileId).querySelector('.'+type);
                if (object['textureIndex'] != 8) {
                    if (asciiMode) {
                        selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']]['ascii']+'")';

                    } else {
                        selectedElement.style.backgroundImage = 'url("'+tileObjects[object['textureIndex']]['icon']+'")';

                    }
                    

                    
                    selectedElement.style.display = "flex";
                    selectedElement.style.transform = (type == "entity" && object['rotation'] == 180)?('scaleX(-1)'):('rotate('+object['rotation']+'deg)');
                } else {
                    if (type != "tile") {
                        selectedElement.style.display = "none";
                    }
                    selectedElement.style.backgroundImage = 'url()';
                    selectedElement.style.transform = "rotate(0)";
                }
                }
            }
            function scaleTextures() {
                var windowMinimum = Math.min(window.innerWidth,window.innerHeight);
                var tileMinimum = Math.min(window.innerWidth/sizeX,window.innerHeight/sizeY);
                document.getElementById('canvas').style.height = tileMinimum*sizeY;
                document.getElementById('canvas').style.width = tileMinimum*sizeX;
                document.querySelectorAll('.tile').forEach((item) => {item.style.height = item.style.width = tileMinimum;});
                document.querySelectorAll('.item').forEach((item) => {item.style.height = item.style.width = tileMinimum;});
                document.querySelectorAll('.obstacle').forEach((obstacle) => {obstacle.style.height = obstacle.style.width = tileMinimum;});
                document.querySelectorAll('.entity').forEach((obstacle) => {obstacle.style.height = obstacle.style.width = tileMinimum;});
            }
            function uuidv4() {
                return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>(+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16));
            }
            function createMessage(type,message,time) {
                var uuid = uuidv4();
                const messages = document.getElementById(type).children;
                var create = true;
                for (var i = 0; i < messages.length; i++) {
                    if (messages[i].innerHTML == message) {
                       create = false;
                       break;
                    }
                }
                if (create) {
                    if (type == "alert") {
                        document.getElementById(type).innerHTML += "<p id = '"+uuid+"'>"+message+"</p>";
                    } else {
                        document.getElementById(type).innerHTML = "<p id = '"+uuid+"'>"+message+"</p>";
                    }
                    setTimeout(function() {
                        if (type == "alert") {
                            document.getElementById(uuid).remove();
                        } else {
                            document.getElementById(type).innerHTML = ""
                        }
                    }, time*1000);
                }
            }
            function advanceStory(requiredStep,type) {
                if (requiredStep == levelStep && storyDialogue[levelStep]['type'] == type) {
                    createMessage("dialogue",storyDialogue[levelStep++]['dialogue'],4);
                }
            }
            function toggleInventory() {
                document.getElementById('inventory').style.height = (inventoryOpened)?"0":"100svh";
                document.getElementById('inventory').style.fontSize = (inventoryOpened)?"0":"40px";
                inventoryOpened = !inventoryOpened;
            }
            function updateInventory() {
                var keys = Object.keys(playerInventory);
                var inventoryBuffer = "";
                for (var i = 0; i < keys.length; i++) {
                    inventoryBuffer += '<div><img src = "'+tileObjects[parseInt(keys[i])]['icon']+'"><p>'+playerInventory[parseInt(keys[i])]+'</p></div>';
                }
                document.getElementById("inventory").innerHTML = inventoryBuffer;
            }
            function stepAction(x,y,type,augmentation) {
                if (currentMap[x][y]['item']['textureIndex'] == 7 && playerCoordinates[0] == x && playerCoordinates[1] == y) {
                    advanceStory(2,type);
                    createMessage("alert",'+<img src = "'+tileObjects[currentMap[x][y]['item']['textureIndex']]['icon']+'">',1)
                    currentMap[x][y]['item']['textureIndex'] = 8;
                     var topLeftCorner = [playerCoordinates[0] - Math.floor(viewSizeX/2),playerCoordinates[1] - Math.floor(viewSizeX/2)];
                    if (Math.abs(x - playerCoordinates[0]) <= Math.floor(viewSizeX/2) && Math.abs(y - playerCoordinates[1]) <= Math.floor(viewSizeY/2)) {
                        applyTexture("entity",(x - topLeftCorner[0])+","+(y - topLeftCorner[1]),currentMap[x][y]['entity']);  
                    }
                    playerInventory["7"] += 1;
                    updateInventory();
                    playSound(1);
                }
                if (currentMap[x][y]['item']['textureIndex'] == 15 && x == playerCoordinates[0] && y == playerCoordinates[1] && augmentation != "inPortal") {
                    var target = currentMap[x][y]['item']['link'];
                    if (target[2] != currentMapName) {
                        loadMap(target[2],target);
                        playSound(4);
                    }
                    moveEntity(target[0],target[1],[x,y],type,"inPortal");
                }
                if (currentMap[x][y]['item']['textureIndex'] == 18 && x == playerCoordinates[0] && y == playerCoordinates[1] && augmentation != "inPortal") {
                    playSound(4);
                    generateMap(50,50);
                }
                
            }
            function createProjectile(start,direction,textureIndex) {
                playSound(7);
                var source = currentMap[start[0]][start[1]];
                start = [start[0] +direction[0],start[1] + direction[1]];
                if (currentMap[start[0]][start[1]]['entity']['textureIndex'] == "8"){
                currentMap[start[0]][start[1]]['entity'] = {"textureIndex": textureIndex, "rotation":(Math.atan2(direction[1], direction[0])*180)/Math.PI} ;
                updateMap();
                    
                    var projectileMotion = setInterval(function() {

                        moveDirection(direction,start[0],start[1]);
                        start = [start[0] +direction[0],start[1] + direction[1]];
                        if (start[0] < 0 || start[0] >= currentMap.length || start[1] < 0 || start[1] >= currentMap[0].length || currentMap[start[0]][start[1]]['obstacle']['textureIndex'] != "8" || (currentMap[start[0]][start[1]]['entity']['textureIndex'] != "8" && currentMap[start[0]][start[1]]['entity']['textureIndex'] != "17")) {
                            
                            if (currentMap[start[0]][start[1]]['entity']['textureIndex'] == 17) { 
                                if (Math.floor(Math.random() * 2) == 0) {
                                    currentMap[start[0]][start[1]]['entity'] = {"textureIndex":"8","rotation":"0"}
                                } else {
                                    start = [start[0] -direction[0],start[1] - direction[1]];
                                    currentMap[start[0]][start[1]]['entity'] = {"textureIndex":"8","rotation":"0"}
                                    clearInterval(projectileMotion);
                                    updateMap();
                                }
                            }
                            if (currentMap[start[0]] && currentMap[start[0]][start[1]] && currentMap[start[0]][start[1]]['entity']['textureIndex'] == "0") {
                                updateHealth(-1);
                                playSound(5);
                            } else if (currentMap[start[0]] && currentMap[start[0]][start[1]] && currentMap[start[0]][start[1]]['entity']['textureIndex'] != "8" && currentMap[start[0]][start[1]]['entity']['textureIndex'] != "0") {
                                currentMap[start[0]][start[1]]['entity']['health'] -= 1;
                                playSound(8);
                                if (currentMap[start[0]][start[1]]['entity']['health'] <= 0) {
                                    createMessage("alert","<img src ='"+tileObjects[source['entity']['textureIndex']]['icon']+"'>"+"<img src ='"+tileObjects[textureIndex]['icon']+"'>"+"<img src ='"+tileObjects[currentMap[start[0]][start[1]]['entity']['textureIndex']]['icon']+"'>",4)
                                    playSound(9);
                                currentMap[start[0]][start[1]]['entity'] = {"textureIndex": "8", "rotation":0};
                                }
                            }
                            clearInterval(projectileMotion);
                            currentMap[start[0] -direction[0]][start[1]-direction[1]]['entity'] = {"textureIndex": "8", "rotation":0} ;
                            updateMap();
                        }
                        
                        
                    }, 250);
                }
            }
            function editMap() {
                isEditMap = !isEditMap;
                if (isEditMap) {
                    document.getElementById('alert').innerHTML += "<p id = 'editBrush'>"+editTypes[0]+"<img style = 'transform:rotate("+editRotation+"deg);' src = '"+tileObjects[currentTexture]['icon']+"'>"+"</p>";
                    var keys = Object.keys(maps);
                    for (var i = 0; i < keys.length; i++) {
                        document.getElementById('alert').innerHTML += "<button style = 'pointer-events: auto;' onclick = 'loadMap(`"+keys[i]+"`,[0,0])'>"+keys[i]+"</button>";
                    }
                } else {
                    document.getElementById('editBrush').remove();
                }
            }
            function newMap(x,y) {
                var mapName = prompt("Map Name"); 
                var newMap = [];
                for (var i = 0; i < x;i++) {
                    var bufferMap = [];
                    for (var j = 0; j < y;j++) {
                        bufferMap.push({"tile":{"textureIndex":1,"rotation":0},"item":{"textureIndex":8,"rotation":0},"obstacle":{"textureIndex":8,"rotation":0},"entity":{"textureIndex":(i == 0 && j == 0)?0:8,"rotation":0}});
                    }
                    newMap.push(bufferMap);
                }
                maps[mapName] = newMap
                loadMap(mapName,[0,0])
                if (!isEditMap) {
                    editMap();
                }
            }
            function loadMap(name,playerLocation) {
                currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['textureIndex'] = "8";
                currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['rotation'] = "0";
                maps[currentMapName] = currentMap;
                playerCoordinates  = [];
                currentMap = maps[name];
                currentMap[playerLocation[0]][playerLocation[1]]['entity']['textureIndex'] = "0";
                currentMapName = name;
                updateMap();
            }
            function importMap() {
                toggleTextInput("IMPORT_MAP:");
                document.getElementById('textInput').querySelector("textarea").style.height = "100svh";
            }
            function exportMap() {
                const filename = currentMapName+".json";
                let element = document.createElement('a');
                currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['textureIndex'] = "8";
                var tempRotation = currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['rotation'];
                currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['rotation'] = "0";
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(currentMap)));
                element.setAttribute('download', filename);
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
                currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['textureIndex'] = "0";
                currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['rotation'] = tempRotation;
            }
            function moveEntity(x,y,currentCoordinates,type,augmentation) {
                if (0 <= x && x < currentMap.length && 0 <= y && y < currentMap[0].length && currentMap[x][y]['entity']['textureIndex'] == 8 && currentMap[x][y]['obstacle']['textureIndex'] == 8 && currentMap[x][y]['tile']['textureIndex'] != 8 && (currentMap[x][y]['tile']['textureIndex'] != 2 || tileObjects[currentMap[currentCoordinates[0]][currentCoordinates[1]]['entity']['textureIndex']]['type'] == "projectile")) {

                        advanceStory(1,type);

                        currentMap[currentCoordinates[0]][currentCoordinates[1]]['entity'] = [currentMap[x][y]['entity'], currentMap[x][y]['entity'] = currentMap[currentCoordinates[0]][currentCoordinates[1]]['entity']][0];

                        var topLeftCorner = [playerCoordinates[0] - Math.floor(viewSizeX/2),playerCoordinates[1] - Math.floor(viewSizeX/2)];
                    if (Math.abs(currentCoordinates[0] - playerCoordinates[0]) <= Math.floor(viewSizeX/2) && Math.abs(currentCoordinates[1] - playerCoordinates[1]) <= Math.floor(viewSizeY/2)) {
                        applyTexture("entity",(currentCoordinates[0] - topLeftCorner[0])+","+(currentCoordinates[1] - topLeftCorner[1]),currentMap[currentCoordinates[0]][currentCoordinates[1]]['entity']);  
                    
                    }
                        
                        
                        if (playerCoordinates[0] == currentCoordinates[0] && playerCoordinates[1] == currentCoordinates[1]) {
                            playerCoordinates = [x,y];
                        }
                        
                        
                    if (Math.abs(x - playerCoordinates[0]) <= Math.floor(viewSizeX/2) && Math.abs(y - playerCoordinates[1]) <= Math.floor(viewSizeY/2)) {
                        applyTexture("entity",(x - topLeftCorner[0])+","+(y - topLeftCorner[1]),currentMap[x][y]['entity']);  
                    }
                        
                        

                        return stepAction(x,y,type,augmentation);
                } 
                if (playerCoordinates[0] == currentCoordinates[0] && playerCoordinates[1] == currentCoordinates[1]) {
                    if ((0 > x || x >= maps[currentMapName].length || 0 > y || y >= maps[currentMapName][0].length)) {
                        playSound(2);
                        return createMessage("dialogue","You can't access this area yet!",4);
                    }
                    if (currentMap[x][y]['tile']['textureIndex'] == 2 ) {
                        return createMessage("dialogue","You can't swim!",4);
                    }
                    if (currentMap[x][y]['obstacle']['textureIndex'] == 6) {
                        return createMessage("dialogue","If only there was a way to break this rock.",4);
                    } 
                }
                
            }
            function moveDirection(direction,x,y) {
                var deg = Math.PI*currentMap[x][y]['entity']['rotation']/180
                if (Math.floor(Math.cos(deg)) == direction[0] && Math.floor(Math.sin(deg)) == direction[1]) {
                    moveEntity(x + direction[0],y + direction[1],[x,y],getEntityCoordinate()[x+","+y]);
                }  else {
                    currentMap[x][y]['entity']['rotation'] = (Math.atan2(direction[1], direction[0])*180)/Math.PI;
                    var topLeftCorner = [playerCoordinates[0] - Math.floor(viewSizeX/2),playerCoordinates[1] - Math.floor(viewSizeX/2)];
                    if (Math.abs(x - playerCoordinates[0]) <= Math.floor(viewSizeX/2) && Math.abs(y - playerCoordinates[1]) <= Math.floor(viewSizeY/2)) {
                        applyTexture("entity",(x - topLeftCorner[0])+","+(y - topLeftCorner[1]),currentMap[x][y]['entity']);  
                    }
                }

                if (0 <= x + direction[0] && x + direction[0] < currentMap.length && 0 <= y + direction[1] && y + direction[1] < currentMap[0].length && currentMap[x + direction[0]][y + direction[1]]['entity']['textureIndex'] == "0"  && x + direction[0] == playerCoordinates[0] && y + direction[1] == playerCoordinates[1]) {
                   
                      moveEntities();
                      
                }
                updateMap();
                
            }
            function textInput(text) {
                document.getElementById('text-display').innerHTML += "<p>"+text+"</p>";
                if (Array.from(text)[0] == "/") {
                    text = text.substring(1, text.length);
                    var commands = text.split(" ");
                    var userFunction =  commands[0];
                    commands.splice(0, 1);
                    for(var i = 0; i < commands.length;i++) {
                        if (typeof commands[i] !== 'undefined') {
                            commands[i] = JSON.parse('"'+commands[i]+'"');
                        } else {
                           commands[i] = JSON.parse(commands[i]);
                        }
                    }
                    eval(userFunction)(...commands);
                } 
                if (text.includes("IMPORT_MAP:")) {
                    text = text.replace("IMPORT_MAP:","");
                    currentMap = JSON.parse(text);
                    updateMap();
                }
                toggleTextInput("");
            }
            
            function toggleTextInput(firstKey) {
                if (!textInputOpened) {
                    document.getElementById('textInput').style.height = "100vw";
                    document.getElementById('textInput').style.fontSize = "40px";
                    document.getElementById('textInput').querySelector("textarea").style.fontSize = "40px";
                    document.getElementById('textInput').querySelector("textarea").style.height = "50px";
                    document.getElementById('textInput').querySelector("textarea").focus();
                } else {
                    document.getElementById('canvas').focus();
                    document.getElementById('textInput').querySelector("textarea").value = "";
                    document.getElementById('textInput').style.height = "0";
                    document.getElementById('textInput').style.fontSize = "0px";
                    textUpIndex = 1;
                }
                textInputOpened = !textInputOpened;
            }
            function updateHealth(increment, source = "") {
                playerInventory["16"] += increment;
                updateInventory();
                for (var i = 0; i < Math.abs(increment); i++) {
                createMessage("alert",(increment/Math.abs(increment) > 0?"+":"-")+'<img src = "'+tileObjects["16"]['icon']+'">',1)
                

                }

                if (playerInventory["16"] <= 0) {
                    playSound(5);
                    createMessage("alert","<img src ='"+tileObjects[source['entity']['textureIndex']]['icon']+"'> <img src ='"+tileObjects[currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['textureIndex']]['icon']+"'>",4)

                    createMessage("dialogue","You Died!",4);
                }
            }
            function moveEntities() {
                var tiles = Object.keys(getEntityCoordinate());
                for (var i = 0; i < tiles.length; i++) {
                    var coordinates = JSON.parse("["+tiles[i]+"]");
                    if (coordinates[0] != playerCoordinates[0] || coordinates[1] != playerCoordinates[1]) {
                        var rotation = currentMap[coordinates[0]][coordinates[1]]['entity']['rotation'];

                        if (playerCoordinates[0] != coordinates[0] && playerCoordinates[1] != coordinates[1] || rotation != Math.atan2((playerCoordinates[1]-coordinates[1]), (playerCoordinates[0]-coordinates[0]))*180/Math.PI) {
                            rotation = Math.floor(Math.random() * 4)*90;
                        } else {
                            createProjectile(coordinates,[Math.round(Math.cos(rotation*Math.PI/180))+0,Math.round(Math.sin(rotation*Math.PI/180))+0],17);
                        }
                        var direction = [Math.round(Math.cos(rotation*Math.PI/180))+0,Math.round(Math.sin(rotation*Math.PI/180))+0];

                        var x= parseInt(tiles[i].split(",")[0]);
                        var y = parseInt(tiles[i].split(",")[1]);
                            if (0 <= x + direction[0] && x + direction[0] < currentMap.length && 0 <= y + direction[1] && y + direction[1] < currentMap[0].length && (x + direction[0] != playerCoordinates[0] || y + direction[1] != playerCoordinates[1])) {

                            moveDirection(direction,x,y);
                        }
                        if ((x + direction[0] == playerCoordinates[0] && y + direction[1] == playerCoordinates[1])) {
                            updateHealth(-1, currentMap[x][y]);
                            playSound(6);
                            
                            
                        }
                        
                    }
                    
                }
            }
            function generateMap(x,y) {
                var requiredEntities = 20;
                var spawnedEntities = 0;
                var map = [];
                
                if (Math.floor(Math.random() * 2) == 1) {
                
                var perlin = generatePerlin(x,y);
                for (var i = 0; i<x; i++) {
                    var buffer = [];
                    for (var j = 0; j<y; j++) {
                        var tileTexture = 3;
                        var obstacleTexture = 8;
                        var entityHealth = 0;
                  var entityTexture = 8;
                  if (Math.floor(Math.random() * (x*y)) <= 20) {
                      entityTexture = 10;
                      spawnedEntities++;
                      entityHealth = spawnedEntities;
                  }
                  
                  
                  if (perlin[i][j] == -1) {
                      
                      tileTexture = 5;
                      
                       var top = (perlin[i - 1])?perlin[i-1][j]:8;
                        var right = (perlin[i][j+1])?perlin[i][j+1]:8;
                      var bottom = (perlin[i + 1])?perlin[i+1][j]:8;
                      var left = (perlin[i][j-1])?perlin[i][j-1]:8;
                      
                      if ((top != -1 || left != -1 || bottom != -1 || right != -1) && Math.floor(Math.random() * 10) >= 4) {
                          obstacleTexture = 6;
                      }
                  }
                  if (perlin[i][j] == -2) {
                      tileTexture = 2;
                  }
                  if (perlin[i][j] == 1) {
                      tileTexture = 12;
                      
                      
                     

                      
                  }
                        buffer.push({"tile":{"textureIndex":tileTexture,"rotation":0},"item":{"textureIndex":8,"rotation":0},"obstacle":{"textureIndex":obstacleTexture,"rotation":0},"entity":{"textureIndex":entityTexture,"rotation":"0","health":entityHealth}})
                        
                    }
                    map.push(buffer);
                }

                } else {
                    
                     for (var i = 0; i<x; i++) {
                    var buffer = [];
                    for (var j = 0; j<y; j++) {
                    var tileTexture = 3;
                     var entityTexture = 8;
                     var obstacleTexture = 8;
                  if (Math.floor(Math.random() * (x*y)) <= 20) {
                      entityTexture = 10;
                      spawnedEntities++;
                      entityHealth = spawnedEntities;
                  }
                  
                        if (x**2+y**2 < 10) {
                                                
                                                tileTexture = 2;
                        }
                                                                        buffer.push({"tile":{"textureIndex":tileTexture,"rotation":0},"item":{"textureIndex":8,"rotation":0},"obstacle":{"textureIndex":obstacleTexture,"rotation":0},"entity":{"textureIndex":entityTexture,"rotation":"0","health":entityHealth}})


                    }
                    
                                        map.push(buffer);

                     }
                    
                    
                    
                }
                
                
                
                var mapName = uuidv4();
                maps[mapName] = map;
                loadMap(mapName,[0,0]);
   
            }
            function playSound(index) {
                if (!sfx[index].pasued) {
                    sfx[index].pause();
                    sfx[index].currentTime = 0;
                }
                sfx[index].play();
            }
            document.addEventListener('keydown', (e) => {
                if (arrowKeys.indexOf(e.code) > -1 && !textInputOpened && parseInt(playerInventory["16"]) > 0) {
                    moveDirection([Math.round(Math.cos((arrowKeys.indexOf(e.code)%4)*Math.PI/2))+0,-Math.round(Math.sin((arrowKeys.indexOf(e.code)%4)*Math.PI/2))+0],playerCoordinates[0],playerCoordinates[1])
                    playSound(0);
                    
                }
                if (e.code === "Space" && !textInputOpened)  {
                    var rotation = ((Math.PI/180)*currentMap[playerCoordinates[0]][playerCoordinates[1]]['entity']['rotation']);
                    createProjectile([playerCoordinates[0],playerCoordinates[1]],[Math.floor(Math.cos(rotation)),Math.floor(Math.sin(rotation))],17)
               moveEntities();
               
                }
                if (e.code === "KeyE" && !textInputOpened)  {
                    toggleInventory();
                }
                if ((e.code === "Slash" && !textInputOpened) || (e.code === "KeyT" && !textInputOpened) || (e.code === "Escape" && textInputOpened))  {
                    toggleTextInput((e.code === "Slash")?"/":"");
                }
                if (e.code === "Enter") {
                    textInput(document.getElementById('textInput').querySelector("textarea").value);
                }
                if (e.code === "BracketLeft") {
                    switchBrush(-1);
                }
                if (e.code === "BracketRight") {
                    switchBrush(1);
                }
                if (e.code === "Backslash") {
                    editTypes.push(editTypes.shift());
                    switchBrush(1);
                }
                if (e.code === "Backspace") {
                    switchBrush("8");
                }
                if (e.code === "KeyQ") {
                    toggleAscii();
                }
                if (e.code === "ArrowUp" && textInputOpened) {
                    document.getElementById('textInput').querySelector("textarea").value = document.getElementById('text-display').children[(textUpIndex + 1 > document.getElementById('text-display').children.length)?textUpIndex:textUpIndex++].innerHTML;
                }
                if (e.code === "ArrowDown" && textInputOpened) {
                    document.getElementById('textInput').querySelector("textarea").value = document.getElementById('text-display').children[(textUpIndex  <= 0)?textUpIndex:textUpIndex--].innerHTML;
                }
                if (e.code === "KeyR" && isEditMap) {
                    editRotation = (editRotation - 90)%360;
                    document.getElementById('editBrush').innerHTML = editTypes[0] + "<img style = 'transform:rotate("+editRotation+"deg);' src = '"+tileObjects[currentTexture]['icon']+"'>";
                }
            });
            let perlin = {
    rand_vect: function(){
        let theta = Math.random() * 2 * Math.PI;
        return {x: Math.cos(theta), y: Math.sin(theta)};
    },
    dot_prod_grid: function(x, y, vx, vy){
        let g_vect;
        let d_vect = {x: x - vx, y: y - vy};
        if (this.gradients[[vx,vy]]){
            g_vect = this.gradients[[vx,vy]];
        } else {
            g_vect = this.rand_vect();
            this.gradients[[vx, vy]] = g_vect;
        }
        return d_vect.x * g_vect.x + d_vect.y * g_vect.y;
    },
    smootherstep: function(x){
        return 6*x**5 - 15*x**4 + 10*x**3;
    },
    interp: function(x, a, b){
        return a + this.smootherstep(x) * (b-a);
    },
    seed: function(){
        this.gradients = {};
        this.memory = {};
    },
    get: function(x, y) {
        if (this.memory.hasOwnProperty([x,y]))
            return this.memory[[x,y]];
        let xf = Math.floor(x);
        let yf = Math.floor(y);
        //interpolate
        let tl = this.dot_prod_grid(x, y, Math.floor(x),   Math.floor(y));
        let tr = this.dot_prod_grid(x, y, Math.floor(x)+1, Math.floor(y));
        let bl = this.dot_prod_grid(x, y, Math.floor(x),   Math.floor(y)+1);
        let br = this.dot_prod_grid(x, y, Math.floor(x)+1, Math.floor(y)+1);
        let xt = this.interp(x-Math.floor(x), tl, tr);
        let xb = this.interp(x-Math.floor(x), bl, br);
        let v = this.interp(y-Math.floor(y), xt, xb);
        this.memory[[x,y]] = v;
        return v;
    }
}
function generatePerlin(gridX,gridY) {
    
perlin.seed();

const GRID_SIZE = 4;
const RESOLUTION = (gridX>gridY)?gridX:gridY/GRID_SIZE;
const COLOR_SCALE = 250;

let num_pixels = GRID_SIZE / RESOLUTION;
var grid = [];
for (let y = 0; y < GRID_SIZE; y += num_pixels / GRID_SIZE){
    var buffer = [];
    for (let x = 0; x < GRID_SIZE; x += num_pixels / GRID_SIZE){
        buffer.push(Math.floor((parseInt(perlin.get(x, y) * COLOR_SCALE)/75)))
    }
    grid.push(buffer)
}
return grid;
}


        </script>
      
    </body>
</html>
