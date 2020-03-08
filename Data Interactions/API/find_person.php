<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['employee_forename']) && isset($_POST['employee_surname'])) {

        $db = new DbOperation();
        $res = $db->findPerson($db->noHTML($_POST['employee_forename']), $db->noHTML($_POST['employee_surname']));

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An Unexpected Error Occured';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = $_POST['employee_forename'].' '.$_POST['employee_surname'].' Has Not Checked In Today';

        } else if ($res === -3) {

          $response['error'] = true;
          $response['message'] = $_POST['employee_forename'].' '.$_POST['employee_surname'].' Is Not A Registered Employee';

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
