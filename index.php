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
                $stmt = $conn->prepare("SELECT user, hash, uuid FROM users WHERE user = ?");
                $stmt->bind_param("s", $_REQUEST['username']);
                $stmt->execute(); 
                $result = $stmt->get_result();
                $stmt->close();
                if (!($result ->fetch_assoc())) {
                    $_SESSION['uuid'] = guidv4();
                    $username = $_REQUEST['username'];
                    $_SESSION['difficulty'] = $_REQUEST['difficulty'];
                    $hash = password_hash($_REQUEST['password'],PASSWORD_DEFAULT);
                    $stmt = $conn->prepare("INSERT INTO users(user, hash, uuid) VALUES (?, ?, ?)");
                    $stmt->bind_param("sss", $_REQUEST['username'], $hash, $_SESSION['uuid']);
                    $stmt->execute(); 
                    $result = $stmt->get_result();
                    $stmt->close();
                    $conn ->close();
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
            $stmt = $conn->prepare("SELECT user, hash, uuid FROM users WHERE user = ?");
            $stmt->bind_param("s", $_REQUEST['username']);
            $stmt->execute(); 
            $result = $stmt->get_result();
            $row = ($result->fetch_assoc());
            $stmt->close();
            $conn ->close();
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
            margin:0;
            background:url(https://community.gamedev.tv/uploads/db2322/original/4X/b/3/b/b3bb7e4daf0a046bd4c49d762e5b15a1cf215cd9.png);
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
            input[type=text], input[type=password] {
            padding:5px;
            background:url();
            background:saddlebrown;
            cursor:text;
            }
            input[type=submit]:hover,label:hover,button:hover {
            transition:.75s;
            transform:scale(.9);
            }
            form span {
                width:100vw;
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
            input[type=radio] {
            display:none;
            }
            input[type=radio]:checked+label {
            background: rgb(212,175,55);
            color:saddlebrown;
            }
            label {
            color: 	rgb(212,175,55);
            padding:20px;
            background:saddlebrown;
            border-radius:20px;
            text-align:center;
            margin:20px;
            cursor:pointer;
            }
            .highlight {
            background:url(https://img.freepik.com/premium-vector/seamless-pattern-old-wood-wall-background_117579-47.jpg);
            }
            table {
            color:rgb(212,175,55);
            background:saddlebrown;
            text-align:center;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            width:clamp(fit-content,50vw,50vw);
            }

            td {
                background:saddlebrown;
            border:2px solid rgb(212,175,55);
            padding:20px;
            }th {
                background:saddlebrown;
            padding:20px;
            }
            td {
                background:saddlebrown;
                padding:10px;
            }
            h2, p {
            color:rgb(212,175,55);
            background:saddlebrown;text-align:center;
            padding:20px;
            border:2px solid rgb(212,175,55);
            }
            p {
                width:50vw;
            }
            a {
                color:rgb(212,175,55);
            }
            #page, form {
                width:100vw;
                display:flex;
                align-items:center;
                justify-content:center;
                flex-direction:column;
                padding:0;
                margin:0;
                border:0;
                gap:20px;
            }
            form {
                width:100vw;
                height:100svh;
                position:absolute;
                top:0;
                left:0;
                display:none;top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background:url(https://community.gamedev.tv/uploads/db2322/original/4X/b/3/b/b3bb7e4daf0a046bd4c49d762e5b15a1cf215cd9.png);
            }
            header {
                position:fixed;
                top:0;
                display:flex;
                align-items:center;
                justify-content:center;
            }
            br {display:block;
                line-height:100px;
            }
            #page > span {
                display:flex;align-items:center;
                justify-content:center;
                flex-direction:column-reverse;
                background:saddlebrown;text-align:center;
            padding:20px;
            border:2px solid rgb(212,175,55);
            border-radius:20px;
            width:clamp(20vw, 50vw, 50vw);
            }
            #page span img {
                width:50%;
            }
            form input{
                text-align:center;
                padding:20px;
            }
            
        </style>
    </head>
    <body>
        <div style = "height:80px"></div>
        <form id = "login" method = "post" action = "">
            <?=$accountText?>
            <button onclick = "toggleLogin();" type = "button">Back</button>
            <span><input type="radio" id  = "easy" name="difficulty" value="easy" checked><label for="easy">Easy</label><input type="radio" id  = "medium" name="difficulty" value="medium"><label for="medium">Medium</label><input type="radio" id  = "hard" name="difficulty" value="hard"><label for="hard">Hard</label></span>
                    
                    <input type = "text" placeholder = "Username" name = "username">
                    <input type = "password" placeholder = "Password" name = "password">
                    <input type = "submit" name = "login" value = "Login">
                    <input type = "submit" name = "create_account" value = "Create Account">
                
                    <input type = "submit" name = "guest_session" value = "Guest">
        </form>
        <div id = "page">
            <header><button onclick = "<?=(isset($_SESSION['uuid']))?"location.replace('https://fathomless.io/engine/');":"toggleLogin();"?>"><?=(isset($_SESSION['uuid']))?"Continue Game":"Play Game";?></button></header>
        <h1>Fathomless Caverns of Peril</h1>
        <hr>
        <span><p>Interesting Creatures</p><img src = "https://fathomless.io/assets/images/slide1.png"></span>
        <p>The world is dying, earthquakes ravage the land, creatures are being corrupted into twisted monstrosities, and it won't last much longer. The World Stone must be reclaimed from the clutches of evil. There is one known way down to the heart of the world, through a cave that none have ever returned from.</p>
        <span><p>Unique Interactions</p><img src = "https://fathomless.io/assets/images/slide2.png"></span>
        <span><p>Labyrinthine Terrain</p><img src = "https://fathomless.io/assets/images/slide3.png"></span>
        
        <h2>Leaderboards</h2>
        <button onclick = "updateLeaderboard()">Reload</button>
        <div id = "leaderboard"><?=file_get_contents("https://fathomless.io/leaderboard/?username=".((isset($_SESSION['username']) && $_SESSION['username'] != "Guest")?$_SESSION['username']:""));?>
            
        </div>
        </div>
        <script>
        <?=($accountText)?"toggleLogin();":"";?>
        const username = '<?=((isset($_SESSION['username']))?$_SESSION['username']:"")?>';
        
        var isLoggingIn = false;
        function toggleLogin() {
            document.getElementById("login").style.display = (isLoggingIn)?"none":"flex";
                        document.getElementById("page").style.display = (isLoggingIn)?"flex":"none";

            document.body.style.overflow =  (isLoggingIn)?"scroll":"hidden";
            if (!isLoggingIn) {
                window.scrollTo({
  top: 0,
  left: 0,
  behavior: 'smooth' // Optional for smooth scrolling
});
            }
            isLoggingIn = !isLoggingIn;
        }
        setInterval(updateLeaderboard, 30000);

            function updateLeaderboard() {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById('leaderboard').innerHTML = this.responseText;
                    }
                }
                xmlhttp.open("GET", "https://fathomless.io/leaderboard/?username="+encodeURIComponent(username), true);
                xmlhttp.send();
            }
        </script>
    </body>
</html>
