<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['person'])) {

        $db = new DbOperation();
        $res = $db->suggestEdit($db->noHTML($_POST['person']));

        $response['error'] = false;

    } else {

        $response['error'] = true;
        $response['message'] = "Request Invalid";

    }

} else {

    $response['error'] = true;
    $response['message'] = "Request Not Allowed";

}

echo json_encode($response);

?>
