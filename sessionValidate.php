<?php
include("session.php");
if (isset($_REQUEST['sendDirection'])) {
    echo file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=".$uuid.(($_REQUEST['sendDirection'] != "")?"&direction=".$_REQUEST['sendDirection']:""));
}


?>
