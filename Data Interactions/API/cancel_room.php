<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/operations/dbOperations.php';

$response = array ();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['forename']) &&
        isset($_POST['surname']) &&
        isset($_POST['email']) &&
        isset($_POST['room_name']) &&
        isset($_POST['building_name']) &&
        isset($_POST['book_date']) &&
        isset($_POST['book_time'])
      ) {

        $db = new DbOperation();
        $res = $db->cancelRoom(
          $db->noHTML($_POST['forename']),
          $db->noHTML($_POST['surname']),
          $db->noHTML($_POST['email']),
          $db->noHTML($_POST['room_name']),
          $db->noHTML($_POST['building_name']),
          $db->noHTML($_POST['book_date']),
          $db->noHTML($_POST['book_time'])
        );

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An Unexpected Error Occured';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = 'Room Booking Could Not Be Found';

        } else {

          $response['error'] = false;
          $response['message'] = 'Room Cancelled';

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
