<?php
include("session.php");
if (isset($_REQUEST['sendDirection']) && isset($uuid)) {
    echo file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=".$uuid.(($_REQUEST['sendDirection'] != "")?"&direction=".$_REQUEST['sendDirection']:"").(($_SESSION['difficulty'] != "")?"&difficulty=".$_SESSION['difficulty']:""));
}
if (isset($_REQUEST['getMap']) && isset($uuid)) {
    echo file_get_contents("https://fathomless.io/cgi-bin/map.py?getMap=".$uuid);
}


?>
