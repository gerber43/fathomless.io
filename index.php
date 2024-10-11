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
        $_SESSION['difficulty'] = $_REQUEST['difficulty'];
        header("Location: https://fathomless.io/engine/");
    }
    if (isset($_REQUEST['create_account'])) {
        if (strlen($_REQUEST['username']) >= 3) {
            
            
        
            $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
            $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
            $result = $conn->query("SELECT * FROM `users` WHERE user = '".$_REQUEST['username']."'");
            $conn->close();
            if (!($result ->fetch_assoc())) {
                $_SESSION['uuid'] = guidv4();
                $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
                $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
                $username = $_REQUEST['username'];
                $_SESSION['difficulty'] = $_REQUEST['difficulty'];
                $hash = password_hash($_REQUEST['password'],PASSWORD_DEFAULT);
                $result = $conn->query("INSERT INTO `users`(`user`, `hash`, `uuid`) VALUES ('".$username."','".$hash."','".$_SESSION['uuid']."')");
                $conn->close();
                header("Location: https://fathomless.io/engine/");
            } else {
                $accountText = '<p>Username In Use</p>';
            }
        } else {
            $accountText = '<p>Username Too Short</p>';
        }
        

    }
    if (isset($_POST['login'])) {
        $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $result = $conn->query("SELECT user, hash, uuid FROM users");
        $conn->close();
        $row = $result->fetch_assoc();
        $accountText = '<p>Invalid Credentials</p>';
        if (($row["user"] == $_REQUEST['username']) and password_verify($_POST['password'], $row["hash"])) {
            $_SESSION['uuid'] = $row["uuid"];
            $_SESSION['username'] = $_REQUEST['username'];
            header("Location: https://fathomless.io/engine/");
        }
        
    }
?>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fathomless Caverns of Peril</title>
        <style>
        @import url('https://fonts.cdnfonts.com/css/8bit-wonder');
            * {
            font-family: '8BIT WONDER', sans-serif;
            }
            html, body {
                padding:0;
                border:0;
                margin:0;
                background:url(https://community.gamedev.tv/uploads/db2322/original/4X/b/3/b/b3bb7e4daf0a046bd4c49d762e5b15a1cf215cd9.png);
            }
            body {
                display:flex;
                align-items:center;
                justify-content:center;
                flex-direction:column;
                gap:20px;
            }
            form {
                width:100%;
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
                border-radius:20px;
                display:flex;
                align-items:center;
                justify-content:center;
                flex-direction:column;

                
            }
            input {
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
            input[type=text], input[type=password] {
                padding:5px;
                                background:url();
                background:saddlebrown;
                cursor:text;

            }
            input[type=submit]:hover {
                transition:.75s;
                transform:scale(.9);

            }
            form div span {
                display:flex;
                align-items:center;
                justify-content:center;
                flex-wrap:wrap;
            }
            ::placeholder {
                color: 	rgb(212,175,55);
            opacity: 1; /* Firefox */
            }

            ::-ms-input-placeholder { /* Edge 12 -18 */
                color: 	rgb(212,175,55);
                }
                h1 {
                    color: 	rgb(212,175,55);
                    padding:20px;
                    background:saddlebrown;
                    border-radius:20px;
                    text-align:center;
                }
            hr {
                width:90%;
                height:5px;
                background:saddlebrown;
                border:none;
            }
            
        </style>
    </head>
    <body>
        <h1>Fathomless Caverns of Peril</h1>
        <hr>
        
        <form method = "post" action = "">
            <span><input type="radio" id  = "easy" name="difficulty" value="easy" checked><label for="easy">Easy</label><input type="radio" id  = "medium" name="difficulty" value="medium"><label for="medium">Medium</label><input type="radio" id  = "hard" name="difficulty" value="hard"><label for="hard">Hard</label></span>
            <div>
                <?=$accountText?>
                <span><input type = "text" placeholder = "Username" name = "username">
                <input type = "password" placeholder = "Password" name = "password"></span>
                <span><input type = "submit" name = "login" value = "Login">
                <input type = "submit" name = "create_account" value = "Create Account"></span>
            </div>
            <div>
        <input type = "submit" name = "guest_session" value = "Guest"></div>
        
        </form>
    </body>
</html>
