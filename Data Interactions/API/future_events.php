<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['room_name']) && isset($_POST['building_name'])) {

        $db = new DbOperation();
        $res = $db->futureEvents($db->noHTML($_POST['room_name']), $db->noHTML($_POST['building_name']));

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An Unexpected Error Occured';

        } else {

          $response['error'] = false;
          $response['message'] = $res;

        }

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
