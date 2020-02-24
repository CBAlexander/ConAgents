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
        isset($_POST['book_time']) &&
        isset($_POST['length_min'])
      ) {

        $db = new DbOperation();
        $res = $db->bookRoom(
          $db->noHTML($_POST['forename']),
          $db->noHTML($_POST['surname']),
          $db->noHTML($_POST['email']),
          $db->noHTML($_POST['room_name']),
          $db->noHTML($_POST['building_name']),
          $db->noHTML($_POST['book_date']),
          $db->noHTML($_POST['book_time']),
          $db->noHTML($_POST['length_min'])
        );

        if ($res === -1) {

          $response['error'] = true;
          $response['message'] = 'An Unexpected Error Occured';

        } else if ($res === -2) {

          $response['error'] = true;
          $response['message'] = 'You Have Another Room Booked For This Time. Please Cancel This Room And Try Again';

        } else if ($res === -3) {

          $response['error'] = true;
          $response['message'] = 'This Room Is Already Booked During This Time';

        } else if ($res === -4) {

          $response['error'] = true;
          $response['message'] = 'Room Does Not Exist In Given Building';

        } else if ($res === -5) {

          $response['error'] = true;
          $response['message'] = 'Date Or Time Not Formatted Correctly. Refer To Documents';

        } else {

          $response['error'] = false;
          $response['message'] = 'Room Booked';

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
