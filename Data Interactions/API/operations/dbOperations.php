<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET');

class dbOperation {

    private $conn;

    function __construct () {

        require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/dbConnection/constants.php';
        require_once $_SERVER['DOCUMENT_ROOT'].'/conv-agents/dbConnection/dbConnect.php';

        $db = new DbConnect ();
        $this->conn = $db->connect ();

    }

    /**
     *
     * XSS Protection
     *
     */
      public function noHTML ($input, $encoding = 'UTF-8') {
          return htmlspecialchars($input, ENT_QUOTES | ENT_HTML5, $encoding);
      }

    /**
     *
     * Cancel A Room Booking
     *
     */
      public function cancelRoom ($forename, $surname, $email, $room, $building, $date, $time) {

        $stmt = $this->conn->prepare ('SELECT `id` FROM `room_bookings` WHERE
          `forename` = ? AND
          `surname`=? AND
          `email`=? AND
          `room_id`=(SELECT `id` FROM `room` WHERE `room_name` = ? AND `building_id`=(SELECT `id` FROM `buildings` WHERE `sudo_name`=?)) AND
          `date_booked`=? AND
          `time_booked`=?;'
        );
        $stmt->bind_param ('sssssss', $forename, $surname, $email, $room, $building, $date, $time);
        $stmt->execute ();
        $result = $stmt->get_result();

        if ($result->num_rows == 1) {

          $data = $result->fetch_all()[0];

          $stmt = $this->conn->prepare ('DELETE FROM `room_bookings` WHERE `id` = ?;');
          $stmt->bind_param ('s', $data[0]);

          if ($stmt->execute()) {

            return true;

          } else {

            return -1;

          }

        } else {

          return -2;

        }

      }

    /**
     *
     * Create A New Event For A Given Room
     *
     */
      public function bookRoom ($forename, $surname, $email, $room, $building, $date, $time, $length) {

        if (strtotime($date.' '.$time) > time() && preg_match('/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/', $time) && preg_match('/^(19|20)\d\d[- \/.](0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])$/', $date)) {

          $stmt = $this->conn->prepare ('SELECT `id` FROM `room` WHERE
            `room_name` = ? AND
            `building_id`=(SELECT `id` FROM `buildings` WHERE `sudo_name`=?);');
          $stmt->bind_param ('ss', $room, $building);
          $stmt->execute ();
          $stmt->store_result();
          $time_until = strtotime($time) + $length*60;

          if ( $stmt->num_rows > 0 ) {

            $stmt = $this->conn->prepare ('SELECT `id` FROM `room_bookings` WHERE
              `room_id` = (SELECT `id` FROM `room` WHERE `room_name` = ? AND `building_id`=(SELECT `id` FROM `buildings` WHERE `sudo_name`=?))
              AND `date_booked` = ? AND
              ? >= `time_booked` AND
              ? <= `time_booked_until`;');
            $stmt->bind_param ('sssss', $room, $building, $date, $time, strftime('%H:%M:%S', $time_until));
            $stmt->execute ();
            $stmt->store_result();

            if ( $stmt->num_rows == 0 ) {

              $stmt = $this->conn->prepare ('SELECT `id` FROM `room_bookings` WHERE `email`=? AND `date_booked` = ? AND ? >= `time_booked` AND ? <= `time_booked_until`;');
              $stmt->bind_param ('ssss', $email, $date, $time, strftime('%H:%M:%S', $time_until));
              $stmt->execute ();
              $stmt->store_result();

              if ( $stmt->num_rows == 0 ) {

                $stmt = $this->conn->prepare ('INSERT INTO
                  `room_bookings` (
                    `surname`,
                    `forename`,
                    `email`,
                    `room_id`,
                    `date_booked`,
                    `time_booked`,
                    `time_booked_until`,
                    `length_min`
                  ) VALUES ( ?, ?, ?, (SELECT `id` FROM `room` WHERE `room_name` = ? AND `building_id`=(SELECT `id` FROM `buildings` WHERE `sudo_name`=?)), ?, ?, ?, ? );');
                $stmt->bind_param ('sssssssss', $surname, $forename, $email, $room, $building, $date, $time, strftime('%H:%M:%S', $time_until), $length);

                if ($stmt->execute ()) {

                  return true;

                } else {

                  return -1;

                }

              } else {

                return -2;

              }

            } else {

              return -3;

            }

          } else {

            return -4;

          }

        } else {

          return -5;

        }

      }

    /**
     *
     * Find Last Check In For A Given Person
     *
     */
      public function findPerson ($employeeForename, $employeeSurname) {

        if ($this->isUserExistName($employeeForename, $employeeSurname)) {

          $stmt = $this->conn->prepare ('SELECT
              `forename`,
              `surname`,
              (SELECT `room_name` FROM `room` WHERE `id`=e.`room_id`) AS `office_room`,
              (SELECT `sudo_name` FROM `buildings` WHERE `id`=(SELECT `building_id` FROM `room` WHERE `id`=e.`room_id`)) AS `building`,
              (SELECT `room_name` FROM `room` WHERE `id`=e.`last_check_in_location`) AS `last_check_in_room`,
              `last_check_in_date`,
              `last_check_in_time`
            FROM `employees` e WHERE `forename`=? AND `surname`=?;');

          $stmt->bind_param ('ss', $employeeForename, $employeeSurname);

          if ($stmt->execute ()) {

            $result = $stmt->get_result();
            $res = array();

            while ($data = $result->fetch_assoc()) {

                array_push($res, $data);

            }

            if ($res[0]['last_check_in_date'] != NULL && $res[0]['last_check_in_time'] != NULL) {

              return $res;

            } else {

              return -2;

            }

          } else {

            return -1;

          }

        } else {

          return -3;

        }

      }

    /**
     *
     * Find All Future Events For A Given Event
     *
     */
      public function futureEvents ($roomName, $buildingName) {

        $stmt = $this->conn->prepare ('SELECT
            `date_booked`,
            `time_booked`
          FROM `room_bookings` WHERE
            (`date_booked` > CURDATE() OR
            (`date_booked` = CURDATE() AND `time_booked` > CURTIME())) AND
            `room_id`=(SELECT `id` FROM `room` WHERE `room_name`=? AND `building_id`=(SELECT `id` FROM `buildings` WHERE `sudo_name`=?));');

        $stmt->bind_param ('ss', $employeeEmail, $buildingName);

        if ($stmt->execute ()) {

          $result = $stmt->get_result();
          $res = array();

          while ($data = $result->fetch_assoc()) {

            array_push($res, $data);

          }

          return $res;

        } else {

          return -1;

        }

      }

    /**
     *
     * Suggest An Edit And Send To Given Recipient
     *
     */
      public function suggestEdit ($recipient_email, $message) {

          $subject = 'Edit Suggestion';
          $headers = 'MIME-Version: 1.0' . "\r\n";
          $headers .= 'Content-type:text/html;charset=UTF-8' . "\r\n";
          $headers .= 'From: AlanaChatbot<noreply@alana.com>' . "\r\n";

          mail($recipient_email,$subject,$message,$headers);

          return true;

      }

    /**
     *
     * Check In A User
     *
     */
      public function userCheckIn ($employeeEmail, $roomName, $buildingName) {

          if ($this->isUserExistEmail($employeeEmail)) {

            $stmt = $this->conn->prepare ('SELECT `id` FROM `room` WHERE `room_name` = ? AND `building_id`=(SELECT `id` FROM `buildings` WHERE `sudo_name`=?);');
            $stmt->bind_param ('ss', $roomName, $buildingName);
            $stmt->execute ();
            $stmt->store_result();

            if ( $stmt->num_rows > 0 ) {

              $stmt = $this->conn->prepare ('UPDATE `employees` SET
                `last_check_in_location`=(SELECT `id` FROM `room` WHERE `room_name`=?),
                `last_check_in_date`=CURDATE(),
                `last_check_in_time`=CURTIME()
              WHERE `email`=?');
              $stmt->bind_param ('ss', $roomName, $employeeEmail);

              if ($stmt->execute ()) {

                return true;

              } else {

                return -1;

              }

            } else {

              return -2;

            }

          } else {

            return -3;

          }

      }

      private function isUserExistEmail ($email) {

        $stmt = $this->conn->prepare('SELECT `id` FROM `employees` WHERE `email` = ?;');
        $stmt->bind_param('s', $email);
        $stmt->execute();
        $stmt->store_result();
        return $stmt->num_rows > 0;

      }

      private function isUserExistName ($forename, $surname) {

        $stmt = $this->conn->prepare('SELECT `id` FROM `employees` WHERE `forename` = ? AND `surname` = ?;');
        $stmt->bind_param('ss', $forename, $surname);
        $stmt->execute();
        $stmt->store_result();
        return $stmt->num_rows > 0;

      }

}

?>
