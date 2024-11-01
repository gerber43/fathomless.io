<?php
    include("session.php");
    if (!isset($_REQUEST['username'])) {
        header("Location: https://fathomless.io");
    } else {
        $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $stmt = $conn->prepare("SELECT * FROM users WHERE user = ?");
        $stmt->bind_param("s", $_REQUEST['username']);
        $stmt->execute(); 
        $result = $stmt->get_result();
        $stmt->close();
        $username = $result ->fetch_assoc();
        $conn ->close();
        if (!$username && $_REQUEST['username'] != "Test") {
            header("Location: https://fathomless.io");
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
            flex-direction:column;
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
            background:saddlebrown;text-align:center;
            }
            td {
            border:2px solid rgb(212,175,55);
            padding:20px;
            }th {
            padding:20px;
            }
            h2, p {
            color:rgb(212,175,55);
            background:saddlebrown;text-align:center;
            padding:20px;
            border:2px solid rgb(212,175,55);
            }
            a {
                color:rgb(212,175,55);
            }
        </style>
    </head>
    <body>
        <h1>Fathomless Caverns of Peril</h1>
        <h2>User: <?=$_REQUEST['username'];?></h2>
        <hr>
        <p>Highscore: <span id = "highScore"></span> Average Score: <span id = "averageScore"></span> Games Played: <span id = "gamesPlayed"></span></p>
        <button onclick = "updateLeaderboard()">Reload</button>
        <div id = "leaderboardDiv"><?=file_get_contents("https://fathomless.io/leaderboard/?only&username=".((isset($_REQUEST['username']))?$_REQUEST['username']:""));?>
        </div>
        <script>
            const username = '<?=$_REQUEST['username'];?>';
            const average = array => array.reduce((a, b) => a + b) / array.length;
            updateLeaderboard();
            
            function updateLeaderboard() {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById('leaderboardDiv').innerHTML = this.responseText;
                        const leaderboard = document.getElementById('leaderboard').rows;
                        var scores = [];
                        for (var i = 1;i<leaderboard.length;i++) {
                            scores.push(parseInt(leaderboard[i].cells[1].innerHTML));
                        }
                        document.getElementById('highScore').innerHTML = scores[0];
                        document.getElementById('averageScore').innerHTML = Math.round(average(scores));
                        document.getElementById('gamesPlayed').innerHTML = scores.length;
                    }
                }
                xmlhttp.open("GET", "https://fathomless.io/leaderboard/?only&username="+encodeURIComponent(username), true);
                xmlhttp.send();
            }
            setInterval(updateLeaderboard, 30000);
        </script>
    </body>
</html>
