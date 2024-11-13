<?php session_start();
    $uuid = $_SESSION['uuid']??null;
    $username = $_SESSION['username']??null;
    function session_required() {
        if (!$uuid) {
            header("Location: https://fathomless.io/");
        }
    }
?>
