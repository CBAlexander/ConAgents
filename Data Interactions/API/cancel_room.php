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
        isset($_POST['book_date']) &&
        isset($_POST['book_time'])
      ) {

        $db = new DbOperation();
        $res = $db->cancelRoom(
          $db->noHTML($_POST['forename']),
          $db->noHTML($_POST['surname']),
          $db->noHTML($_POST['email']),
          $db->noHTML($_POST['room_name']),
          $db->noHTML($_POST['book_date']),
          $db->noHTML($_POST['book_time'])
        );

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An unexpected error occured. Please try again later.';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = 'I couldn\'t find your room booking.';

        } else if ($res === -3) {

          $response['error'] = true;
          $response['message'] = 'This room does not exist in this building.';

        } else {

          $response['error'] = false;
          $response['message'] = 'Please complete your cancellation using this form. I have also removed your booking from our simulated database so that my test system can function on future requests.';

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
