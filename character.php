<?php include("session.php");
session_required();
 if (isset($_REQUEST['submit'])) {
     file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=".$_SESSION['uuid']."&difficulty=".$_REQUEST['difficulty']."&race=".$_REQUEST['race']);

    }

if (file_exists("maps/".$_SESSION['uuid'].".pkl")) {
        header("Location: https://fathomless.io/engine/");
    }
   

?>
<html>
    <head>
        <style>
        html, body {
            border:0;
            padding:0;
            margin:0;
            background:url(https://community.gamedev.tv/uploads/db2322/original/4X/b/3/b/b3bb7e4daf0a046bd4c49d762e5b15a1cf215cd9.png);
            
        }
        #page {
             display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            width:100vw;
            height:100svh;
        }
        form {
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            width:100%;
        }
        form span{
             display:flex;
            align-items:center;
            justify-content:center;
            flex-wrap:wrap;
        }
        input, button {
            transition:.75s;
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            width:300px;
            height:60px;
            color:gold;
            font-size:20px;
            border:2px burlywood solid;
            background:saddlebrown;
            margin:20px;
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            }
        input[type=radio] {
            display:none;
            }
            input[type=radio]:checked+label {
            background: rgb(212,175,55);
            color:saddlebrown;
            }
            label {
                transition:.75s;
            color: 	rgb(212,175,55);
            padding:20px;
            background:saddlebrown;
            border-radius:20px;
            text-align:center;
            margin:20px;
            cursor:pointer;
            }
        h1, p {
            color:rgb(212,175,55);
            background:saddlebrown;text-align:center;
            padding:20px;
            border:2px solid rgb(212,175,55);
            }
            input[type=submit]:hover,label:hover,button:hover {
            transition:.75s;
            transform:scale(.9);
            }
        </style>
        
        
    </head>
    <body>
        <div id  ="page">
        <h1>Fathomless Caverns of Peril</h1>
        <form method = "post">
            
            
            <p>Choose Your Difficulty</p>
            <div id = "difficulty"><p>Information about the selected difficulty will appear here</p></div>

            <span><input type="radio" id  = "easy" name="difficulty" value="easy" checked><label for="easy">Easy</label><input type="radio" id  = "medium" name="difficulty" value="medium"><label for="medium">Medium</label><input type="radio" id  = "hard" name="difficulty" value="hard"><label for="hard">Hard</label></span>
    <p>Choose Your Character</p>
    <div id = "race"><p>Information about the selected character will appear here</p></div>

                <span><input type="radio" id  = "human" name="race" value="Human" checked><label for="human">Human</label>
                <input type="radio" id  = "elf" name="race" value="Elf" ><label for="elf">Elf</label>
                <input type="radio" id  = "dwarf" name="race" value="Dwarf" ><label for="dwarf">Dwarf</label>
                <input type="radio" id  = "gnome" name="race" value="Gnome" ><label for="gnome">Gnome</label>
                <input type="radio" id  = "orc" name="race" value="Orc" ><label for="orc">Orc</label>
                <input type="radio" id  = "halfDemon" name="race" value="HalfDemon" ><label for="halfDemon">Half Demon</label>
                </span>
            <input type = "submit" name = "submit" value = "Submit">
        </form>
        
        </div>
        
        <script>
        
        document.querySelectorAll("input[type=radio]").forEach(item => {
     item.addEventListener("input", (event) => {
  hintUpdate(event.target.getAttribute("name"), event.target.value)
});
  
  
  
});


     
        
        
        
            function hintUpdate(name, selected) {
                var hintBox = document.getElementById(name);
                if (name == "difficulty") {
                
                var mobSpawns = "x1";
                var itemSpawns = "x1";
                if (selected == "medium") {
                    mobSpawns = "x2";
                    itemSpawns = "x0.5";
                }
                if (selected == "hard") {
                    mobSpawns = "x3";
                    itemSpawns = "x0.3";
                }
                hintBox.innerHTML = "<span><p>"+mobSpawns+" as many Creatures will spawn</p><p>"+itemSpawns+" as many Creatures will appear</p></span>";
                }
                if (name == "race") {
                    hintBox.innerHTML = "<p>Selected Race: "+selected+"</p>";

                }
            }
        </script>
        
</body></html>
