<?php
include("session.php");
function guidv4($data = null) {
        $data = $data??random_bytes(16);
        assert(strlen($data) == 16);
        $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
        $data[8] = chr(ord($data[8]) & 0x3f | 0x80);
        return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));}
    if (isset($_REQUEST['guest_session'])) {
        $_SESSION['uuid'] = guidv4();
        header("Location: https://fathomless.io/engine/");
    }
?>
<html>
    <head>
        <title>Account Management</title>
    </head>
    <body>
        <form method = "post" action = "">
        <button name = "guest_session">Guest</button>
        </form>
    </body>
</html>
