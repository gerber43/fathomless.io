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
    <head></head>
    <body>
        
        <form method = "post">
            
            
            
            <span><input type="radio" id  = "easy" name="difficulty" value="easy" checked><label for="easy">Easy</label><input type="radio" id  = "medium" name="difficulty" value="medium"><label for="medium">Medium</label><input type="radio" id  = "hard" name="difficulty" value="hard"><label for="hard">Hard</label></span>

    
                <span><input type="radio" id  = "human" name="race" value="Human" checked><label for="human">Human</label>
                <input type="radio" id  = "elf" name="race" value="Elf" ><label for="elf">Elf</label>
                <input type="radio" id  = "dwarf" name="race" value="Dwarf" ><label for="dwarf">Dwarf</label>
                <input type="radio" id  = "gnome" name="race" value="Gnome" ><label for="gnome">Gnome</label>
                <input type="radio" id  = "orc" name="race" value="Orc" ><label for="orc">Orc</label>
                <input type="radio" id  = "halfDemon" name="race" value="HalfDemon" ><label for="halfDemon">Half Demon</label>
                </span>
            <input type = "submit" name = "submit" value = "Submit">
        </form>
        
        
        
</body></html>
