<?php session_start();
    $uuid = $_SESSION['uuid']??null;
    $username = $_SESSION['username']??null;
    /*Only use session variables to create access rules*/
    function session_required() {
        if (!isset($_SESSION['uuid'])) {
            header("Location: https://fathomless.io/");
        }
    }
?>
