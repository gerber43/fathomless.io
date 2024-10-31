<p>The First Row Is The Spawn List For Each Level</p>
<style>
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
