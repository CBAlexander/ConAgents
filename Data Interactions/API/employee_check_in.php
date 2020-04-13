<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['employee']) && isset($_POST['room_name'])) {

        $db = new DbOperation();
        $res = $db->userCheckIn($db->noHTML($_POST['employee']), $db->noHTML($_POST['room_name']));

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An unexpected error occured.';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = 'Given employee is not registered in this institution.';

        } else {

          $response['error'] = false;
          $response['message'] = 'Check in successful.';

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
