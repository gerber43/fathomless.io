
<style>
html, body {
    margin:0;
    padding:0;
}
    table, tr,td,th{
        border:solid black 2px;
    }
    
    tr:nth-child(2) {
        background:#eee;
    }
</style>

<?php 
ini_set('display_startup_errors', 1);
ini_set('display_errors', 1);
error_reporting(-1);
error_reporting(E_ERROR | E_PARSE);



$malStrings = ["username","<username>' OR 1=1--
'OR '' = '	Allows authentication without a valid username.
<username>'--
' union select 1, '<user-fieldname>', '<pass-fieldname>' 1--
'OR 1=1--",'1d3d2d231d2dd4570017" OR "570017"="570017',"1d3d2d231d2dd4570017' OR '570017'='570017","SELECT * from users where user = 'Test'",];

echo '<p>The first row demonstrates a successful, non malicious string</p>';
echo '<table><tr><th>Malicious String</th><th>HTTP Response Header</th></tr>';


foreach($malStrings as $string) {
    $url = 'https://fathomless.io';
$data = ['create_account' => '', 'username' => $string, 'password' => "pass", "difficulty" => "Easy"];

$options = [
    'http' => [
        'header' => "Content-type: application/x-www-form-urlencoded\r\n",
        'method' => 'POST',
        'content' => http_build_query($data),
    ],
];

$context = stream_context_create($options);
file_get_contents($url, false, $context);

echo "<tr><td>".$string."</td><td>".$http_response_header[0]."</td>";

}
echo '</table>';


echo '<p>In addition to these tests an SQL Injection attack test was performed by <a target = "_blank" href = "https://pentest-tools.com">https://pentest-tools.com</a>. The results of which are displayed here.</p>';
echo '<p>The test was performed with 27 Unique Injection Points,
across 13 URLS, with 1089 HTTP requests</p><embed style = "width:100vw;height:50vh" src = "https://fathomless.io/inject.pdf">';



echo '<p>The First Row Is The Spawn List For Each Level</p>';
function generateMap($level = 0) {
if (file_exists("logs/Test.txt")) {
    unlink("logs/Test.txt");
}
if (file_exists("maps/Test.pkl")) {
    unlink("maps/Test.pkl");
}
return file_get_contents("https://fathomless.io/cgi-bin/movement_api.py?uuid=Test&level=".$level);
}


$biomes = [
    [],
    ["Goblin", "Spider", "Bat"],             # Cave creatures
    ["Goblin", "Spider", "Bat"],             # Cave creatures
    ["Fishman", "DrownedSailor", "Pirate"],   # Cove creatures
    ["GoblinMiner", "RockWorm"],           # Mine creatures
    ["GoblinMiner", "RockWorm"],           # Mine creatures
    ["GiantSlime", "SewerCroc"],          # Sewer creatures
    ["GiantSlime", "SewerCroc"],          # Sewer creatures
    ["DiseasedScavenger", 'BloatedGuard'],  # Shantytown creatures
    ["MagmaGolem", "FireElemental"],       # Magma Core creatures
    ["DarkElf", "DarkDwarf"],              # Deep Cave creatures
   ["XotilWarrior", "XotilAbomination", "XotilHighPriest"],  # Ziggurat creatures
    ["AshGolem", "ObsidianGolem"],         # Ember creatures
    ["AshGhoul", "AshWight"],             # Columbarium creatures
    ["Skeleton", "Necromancer"],  # Catacomb creatures
     ["FleshAmalgam", "Polyp"],              # Carrion creatures
     ["Parasite", "BloodCrawler"],         # Worldeater’s Gut creatures
     ["Lich", "DeathKnight"],             # Necropolis creatures
     ["TricksterImp", "DeceitArchdemon"], # Underworld creatures
     ["AncientServant", "Apparition"],       # Ancient City creatures
    ['Cultist', "Shambler"],  # Temple of the Old One creatures
     ["VoidBeast"],                      # Cosmic Void creatures
     ["AbyssDragon"]                 # Heart of the World (Final Boss)
     ,[]
];
$levels = [];
$allCreatures = [];
array_push($allCreatures, $biomes);
for ($i = 0;$i<4;$i++) {
    $levelSet = [];
    $creatures = array_fill(0, 24, []);

    for ($j = 0; $j < 24; $j++) {
        $map = json_decode((generateMap($j)),true)['map_subset']; 
        foreach ($map as $row) {
            foreach ($row as $tile) {
                if (isset($tile['Creature'])) {
                    if (!in_array($tile['Creature']['name'],$creatures[$j]) && $tile['Creature']['name'] != "Player") {
                        array_push($creatures[$j],$tile['Creature']['name']);
                    }
                }
            }
        }
        
        array_push($levelSet, $map);
    }
    array_push($levels, $levelSet);
    array_push($allCreatures,$creatures);
     
}
echo '<table><tr>';
 for ($i = 0; $i < 24; $i++) {
     echo '<th>Level '.$i.'</th>';
 }
 echo '</tr>';
  for ($i = 0; $i < count($allCreatures); $i++) {
      echo '<tr>';
      for ($j = 0; $j < 24; $j++) {
     echo '<td>';
      for ($k = 0; $k < count($allCreatures[$i][$j]); $k++) {
          echo '<p>'.$allCreatures[$i][$j][$k]."</p>";
      }
     echo '</td>';
 }
 echo '</tr>';
 }
 echo '</table>';
?>
