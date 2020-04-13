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
      public function cancelRoom ($forename, $surname, $email, $room, $date, $time) {

        $stmt = $this->conn->prepare ('SELECT `id` FROM `room` WHERE `room_name` = ?;');
        $stmt->bind_param ('s', $room);
        $stmt->execute ();
        $stmt->store_result();

        if ( $stmt->num_rows != 0 ) {

          $stmt = $this->conn->prepare ('SELECT `id` FROM `room_bookings` WHERE
            `forename` = ? AND
            `surname`=? AND
            `email`=? AND
            `room_id`=(SELECT `id` FROM `room` WHERE `room_name` = ?) AND
            `date_booked`=? AND
            `time_booked`=?;'
          );
          $stmt->bind_param ('ssssss', $forename, $surname, $email, $room, $date, $time);
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

        } else {

          return -3;

        }

      }

    /**
     *
     * Create A New Event For A Given Room
     *
     */
      public function bookRoom ($forename, $surname, $email, $room, $date, $time, $length, $numPeople) {

        $stmt = $this->conn->prepare('SELECT `num_people` FROM `room` WHERE `room_name` = ?;');
        $stmt->bind_param('s', $room);
        if ($stmt->execute ()) {
          $result = $stmt->get_result();
          $flag = false;

          while ($data = $result->fetch_assoc()) {

            $flag = true;

            if ( strval($data["num_people"]) >= $numPeople ) {

              if (strtotime($date.' '.'23:59:59') > time() && preg_match('/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/', $time) && preg_match('/^(19|20)\d\d[- \/.](0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])$/', $date)) {

                $stmt = $this->conn->prepare ('SELECT `id` FROM `room` WHERE `room_name` = ?;');
                $stmt->bind_param ('s', $room);
                $stmt->execute ();
                $stmt->store_result();

                if ( $stmt->num_rows != 0 ) {

                  $time_until = strtotime($time) + $length*60;
                  $stmt = $this->conn->prepare ('SELECT `id` FROM `room_bookings` WHERE
                    `room_id` = (SELECT `id` FROM `room` WHERE `room_name` = ?)
                    AND `date_booked` = ? AND
                    ? >= `time_booked` AND
                    ? <= `time_booked_until`;');
                  $stmt->bind_param ('ssss', $room, $date, $time, strftime('%H:%M:%S', $time_until));
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
                      ) VALUES ( ?, ?, ?, (SELECT `id` FROM `room` WHERE `room_name` = ?), ?, ?, ?, ? );');
                    $stmt->bind_param ('ssssssss', $surname, $forename, $email, $room, $date, $time, strftime('%H:%M:%S', $time_until), $length);

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

          if (!$flag) {

            return -6;

          }

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
      public function futureEvents ($roomName) {

        $stmt = $this->conn->prepare ('SELECT
            `date_booked`,
            `time_booked`
          FROM `room_bookings` WHERE
            `date_booked` > CURDATE() AND
            `time_booked` > CURTIME() AND
            `room_id`=(SELECT `id` FROM `room` WHERE `room_name`=?);');

        $stmt->bind_param ('s', $roomName);

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
      public function suggestEdit ($person) {

          $recipient_email = 'mf48@hw.ac.uk';
          $subject = 'Edit Suggestion';
          $headers = 'MIME-Version: 1.0' . "\r\n";
          $headers .= 'Content-type:text/html;charset=UTF-8' . "\r\n";
          $headers .= 'From: AlanaChatbot<noreply@alana.com>' . "\r\n";
          $message = "The data on ".$person." may be out of date. Please verify this information.";
          mail($recipient_email,$subject,$message,$headers);

          return true;

      }

    /**
     *
     * Check In A User
     *
     */
      public function userCheckIn ($employee, $roomName) {

          $names = explode(" ", $employee);
          if ($this->isUserExistName($names[0], $names[1])) {

            $stmt = $this->conn->prepare ('SELECT `id` FROM `room` WHERE `room_name` = ?;');
            $stmt->bind_param ('s', $roomName);
            $stmt->execute ();
            $stmt->store_result();

            if ( $stmt->num_rows > 0 ) {

              $stmt = $this->conn->prepare ('UPDATE `employees` SET
                `last_check_in_location`=(SELECT `id` FROM `room` WHERE `room_name`=?),
                `last_check_in_date`=CURDATE(),
                `last_check_in_time`=CURTIME()
              WHERE `forename`=? AND `surname`=?');
              $stmt->bind_param ('sss', $roomName, $names[0], $names[1]);

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

      /**
       *
       * Find a free room based on number of users
       *
       */
      public function findRoom ($numPeople, $date) {

        $stmt = $this->conn->prepare('SELECT `room_name` FROM `room` WHERE `num_people` >= ?;');
        $stmt->bind_param('s', $numPeople);
        if ($stmt->execute ()) {
          $result = $stmt->get_result();

          while ($data = $result->fetch_assoc()) {

            $stmt = $this->conn->prepare ('SELECT `id` FROM `room_bookings` WHERE
              `room_id` = (SELECT `id` FROM `room` WHERE `room_name` = ?)
              AND `date_booked` = ?;');
            $stmt->bind_param ('ss', $data['room_name'], $date);
            $stmt->execute ();
            $stmt->store_result();

            if ( $stmt->num_rows == 0 ) {

              return $data['room_name'];

            }

          }

          return "";

        }
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
