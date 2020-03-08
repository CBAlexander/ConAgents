<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['employee_email']) && isset($_POST['room_name']) && isset($_POST['building_name'])) {

        $db = new DbOperation();
        $res = $db->userCheckIn($db->noHTML($_POST['employee_email']), $db->noHTML($_POST['room_name']), $db->noHTML($_POST['building_name']));

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An Unexpected Error Occured';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = 'Room Does Not Exist In Given Building';

        } else if ($res === -3) {

          $response['error'] = true;
          $response['message'] = 'Given Email Is Not A Registered Employee';

        } else {

          $response['error'] = false;
          $response['message'] = 'User Checked In';

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
