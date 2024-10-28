<?php

if (isset($_REQUEST['uuid']) && file_exists("logs/".$_REQUEST['uuid'].".txt")) {
    $gameLog = file_get_contents("logs/".$_REQUEST['uuid'].".txt");
    if (str_contains($gameLog,"Game Over. Final Score: ")) {
        $score = substr($gameLog,strpos($gameLog,"Game Over. Final Score: ")+strlen("Game Over. Final Score: "));
        $dbParams = json_decode(file_get_contents("dbPass.pem"),true);
        
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $stmt = $conn->prepare("SELECT user FROM users WHERE uuid = ?");
        $stmt->bind_param("s", $_REQUEST['uuid']);
        $stmt->execute(); 
        $result = $stmt->get_result();
        $stmt->close();
        $username = ($result ->fetch_assoc());
        $username = ($username['user'])?$username['user']:"Guest";

        
        
        $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $stmt = $conn->prepare("INSERT INTO leaderboard(uuid, user, score, date) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("ssss", $_REQUEST['uuid'],$username,$score,time());
        $stmt->execute(); 
        $stmt->close();
        $conn ->close();
        unlink("logs/".$_REQUEST['uuid'].".txt");
        unlink("maps/".$_REQUEST['uuid'].".pkl");
        echo $gameLog;
        
    } 
    
}



?>
