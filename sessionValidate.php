<?php
include("session.php");

if (isset($_REQUEST['sendDirection'])) {
    echo file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?direction=".urlencode($_REQUEST['sendDirection'])."&uuid".urlencode($uuid));
}


?>
