<?php
include("session.php");
if (isset($_REQUEST['sendAttack']) && isset($uuid)) {
    echo file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=".$uuid."&attack=".urlencode($_REQUEST['sendAttack']).(isset($_REQUEST['selected'])?"&selected=".urlencode($_REQUEST['selected']):""));

    
    
}  else if (isset($_REQUEST['levelUp']) && isset($uuid)) {
    echo file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=".$uuid.(isset($_REQUEST['cunning'])?"&levelUp=levelUp&cunning=".urlencode($_REQUEST['cunning']):"").(isset($_REQUEST['magic'])?"&magic=".urlencode($_REQUEST['magic']):"").(isset($_REQUEST['fitness'])?"&fitness=".urlencode($_REQUEST['fitness']):""));

}
else if(!isset($_REQUEST['sendAttack']) && isset($uuid)) {
    echo file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=".$uuid);
} 
if (!isset($uuid)) {
    echo "Timed Out";
}

?>
