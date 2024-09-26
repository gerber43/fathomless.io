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
        $_SESSION['username'] = "Guest";
        header("Location: https://fathomless.io/engine/");
    }
    if (isset($_REQUEST['create_account'])) {
        $_SESSION['uuid'] = guidv4();
        $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $username = $_REQUEST['username'];
        $hash = password_hash($_REQUEST['password'],PASSWORD_DEFAULT);
        $result = $conn->query("INSERT INTO `users`(`user`, `hash`, `uuid`) VALUES ('".$username."','".$hash."','".$_SESSION['uuid']."')");
        $conn->close();
        header("Location: https://fathomless.io/engine/");
    }
    if (isset($_POST['login'])) {
        $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $result = $conn->query("SELECT user, hash, uuid FROM users");
        $conn->close();
        $row = $result->fetch_assoc();
        $accountText = '<p>Invalid Credentials</p>';
        if ((strtolower($row["user"]) == strtolower($_REQUEST['username'])) and password_verify($_POST['password'], $row["hash"])) {
            $_SESSION['uuid'] = $row["uuid"];
            $_SESSION['username'] = $_REQUEST['username'];
            header("Location: https://fathomless.io/engine/");
        }
        
    }
    
    if (isset($_REQUEST['login'])) {
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $username = $_REQUEST['username'];
        $hash = password_hash($_REQUEST['password'],PASSWORD_DEFAULT);
        $result = $conn->query("INSERT INTO `users`(`user`, `hash`, `uuid`) VALUES ('".$username."','".$hash."','".$_SESSION['uuid']."')");
        $conn->close();
    }
?>
<html>
    <head>
        <title>Account Management</title>
        <style>
            html, body {
                padding:0;
                border:0;
                margin:0;
            }
            form {
                width:100%;
                height:100%;
                display:flex;
                align-items:center;
                justify-content:center;
                flex-wrap:wrap;
                margin:0;
                padding:0;
                border:0;
            }
            form div {
                width:500px;
                padding:20px;
                border:2px black solid;
                border-radius:20px;
                display:flex;
                align-items:center;
                justify-content:center;
                flex-direction:column;
                
                
            }
        </style>
    </head>
    <body>
        <form method = "post" action = "">
            <div>
                <?=$accountText?>
                <input type = "text" placeholder = "Username" name = "username">
                <input type = "password" placeholder = "Password" name = "password">
                <span><button name = "login">Login</button>
                <button name = "create_account">Create Account</button></span>
            </div>
            <div>
        <button name = "guest_session">Guest</button></div>
        
        </form>
    </body>
</html>
