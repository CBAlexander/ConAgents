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
        isset($_POST['book_time']) &&
        isset($_POST['length_min']) &&
        isset($_POST['num_people'])
      ) {

        $db = new DbOperation();
        $res = $db->bookRoom(
          $db->noHTML($_POST['forename']),
          $db->noHTML($_POST['surname']),
          $db->noHTML($_POST['email']),
          $db->noHTML($_POST['room_name']),
          $db->noHTML($_POST['book_date']),
          $db->noHTML($_POST['book_time']),
          $db->noHTML($_POST['length_min']),
          $db->noHTML($_POST['num_people'])
        );

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An unexpected error occured. Please try again later.';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = 'This room is already booked.';

        } else if ($res === -3) {

          $response['error'] = true;
          $response['message'] = 'You have supplied an incorrect room number. Please try again later.';

        } else if ($res === -4) {

          $response['error'] = true;
          $response['message'] = 'You have supplied an incorrect date. Please try again later.';

        } else if ($res === -5) {

          $response['error'] = true;
          $response['message'] = "Room '".$_POST['room_name']."' does not have a sufficient capacity for ".$_POST['num_people']." people.";

        } else if ($res === -6) {

          $response['error'] = true;
          $response['message'] = "Room '".$_POST['room_name']."' does not exist.";

        } else {

          $response['error'] = false;
          $response['message'] = 'Please complete your booking using this form. I will also store your booking in our simulated database so that my test system can function on future requests.';

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
