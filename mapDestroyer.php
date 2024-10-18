<?php
$maps = scandir("maps");

$dbParams = json_decode(file_get_contents("dbPass.pem"),true);
$conn = new mysqli($dbParams[0],$dbParams[1],$dbParams[2],$dbParams[3]);
$result = $conn->query("SELECT uuid FROM users");
$conn->close();
$uuids = [];
while ($row = $result->fetch_assoc()) {
    array_push($uuids,$row['uuid']);
}
foreach ($maps as $map) {
    $currentTime = time();
    if (str_contains($map,".pkl")) {
        if (!in_array(str_replace(".pkl","",$map),$uuids) && $currentTime - filemtime("maps/".$map) >= 3600) {
            unlink("maps/".$map);
        }
    }
}
?>
