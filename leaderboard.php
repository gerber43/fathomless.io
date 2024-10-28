<?php
include("session.php");
        $dbParams = json_decode(file_get_contents("dbPass.pem"),true);

        $username = (isset($_REQUEST['username']))?$_REQUEST['username']:"";

        if (isset($_REQUEST['only'])) {
            $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $stmt = $conn->prepare("SELECT * FROM leaderboard WHERE user = ? ORDER BY score DESC");
        
        $stmt->bind_param("s", $_REQUEST['username']);
       
        $stmt->execute(); 
        $result = $stmt->get_result();
        $stmt->close();
        $conn ->close();
        
        
        } else {
             $conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
        $result = $conn->query("SELECT * FROM leaderboard ORDER BY score DESC");
        $conn ->close();
        date_default_timezone_get();
        date_default_timezone_set('America/Indianapolis');
        }
        
       
        echo "<table id = 'leaderboard'><tr><th>User</th><th>Score</th><th>Date</th></tr>";
        while ($row = $result->fetch_assoc()) {
            echo '<tr '.(($row['user']==$username && !isset($_REQUEST['only']))?'class="highlight"':"").'><td>'.((!isset($_REQUEST['only']) && $row['user'] != 'Guest')?'<a href = "https://fathomless.io/profile/?username='.urlencode($row['user']).'">'.$row['user'].'</a>':$row['user']).'</td><td>'.$row['score'].'</td><td>'.date("m/d/Y g:ia", $row['date']).'</td></tr>';
        }
        echo "</table>"
        
        


?>
