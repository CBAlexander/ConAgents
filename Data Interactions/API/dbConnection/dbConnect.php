<?php

class dbConnect {

    private $conn;

    function __construct() { }

    function connect() {

        require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/dbConnection/constants.php';

        $this->conn = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

        if (mysqli_connect_errno()) {

            die("Failed To Connect To MySQL: " . mysqli_connect_error());

        }

        return $this->conn;

    }

}

?>
