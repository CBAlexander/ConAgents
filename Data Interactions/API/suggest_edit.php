<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['recipient_email']) && isset($_POST['message'])) {

        $db = new DbOperation();
        $res = $db->suggestEdit($db->noHTML($_POST['recipient_email']), $db->noHTML($_POST['message']));

        $response['error'] = false;
        $response['message'] = 'Suggested Edit Sent. Make Sure To Check Your Junk Box If Mail Does Not Appear';

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
