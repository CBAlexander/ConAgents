SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS room_bookings;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS buildings;
SET FOREIGN_KEY_CHECKS=1;

/* DATABASE STRUCTURE */

CREATE TABLE IF NOT EXISTS buildings (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  sudo_name VARCHAR(20) NOT NULL,
  surname_contact VARCHAR(50),
  forename_contact VARCHAR(50),
  email_contact VARCHAR(50) NOT NULL
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS room (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  room_name VARCHAR(50) NOT NULL UNIQUE,
  building_id INT(11) NOT NULL,
  num_people INT(11) NOT NULL,
  num_computers INT(11),
  hireable TINYINT(1),
  FOREIGN KEY (building_id) REFERENCES buildings(id)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS employees (
  id VARCHAR(40) NOT NULL PRIMARY KEY,
  surname VARCHAR(50),
  forename VARCHAR(50),
  email VARCHAR(50) NOT NULL UNIQUE,
  room_id INT(11) UNIQUE,
  last_check_in_date DATE,
  last_check_in_time TIME,
  FOREIGN KEY (room_id) REFERENCES room(id)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS classes (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  class_name VARCHAR(100) NOT NULL,
  class_code VARCHAR(100) NOT NULL UNIQUE,
  lecturer VARCHAR(40) NOT NULL,
  FOREIGN KEY (lecturer) REFERENCES employees(id)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS room_bookings (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  surname VARCHAR(50),
  forename VARCHAR(50),
  email VARCHAR(50) NOT NULL,
  room_id INT(11) NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL,
  FOREIGN KEY (room_id) REFERENCES room(id)
) ENGINE = INNODB;

/* INSERT STATEMENTS - Exemplar Data With Fixed UUID */

INSERT INTO `buildings` (`name`, `sudo_name`, `surname_contact`, `forename_contact`, `email_contact`) VALUES
('Global Research, Innovation and Discovery Building', 'GRID', 'Smith', 'John', 'jsmith@hw.ac.uk'),
('Centre for Robotics', 'Robotarium', 'Baker', 'Adam', 'abaker@hw.ac.uk'),
('Earl Mountbatten', 'EM', 'Davis', 'Frank', 'fdavis@hw.ac.uk');

INSERT INTO `room` (`id`, `room_name`, `building_id`, `num_people`, `num_computers`, `hireable`) VALUES
(1, '1.45', 3, 1, 1, 0),
(2, '1.44', 3, 1, 1, 0),
(3, '1.43', 3, 1, 1, 0),
(4, '1.42', 3, 1, 1, 0),
(5, '1.41', 3, 1, 1, 0),
(6, '1.21', 3, 1, 1, 0),
(7, '1.22', 3, 1, 1, 0),
(8, '1.23', 3, 1, 1, 0),
(9, 'Research Room', 1, 20, 10, 1),
(10, 'Robotics Room', 2, 7, 3, 1);

INSERT INTO `employees` (`id`, `surname`, `forename`, `email`, `room_id`, `last_check_in_date`, `last_check_in_time`) VALUES
('23e50bb7-4f83-11ea-8240-001a4a05014a', 'Bartie', 'Phil', 'pbartie@hw.ac.uk', 1, '2020-02-14', '22:28:43'),
('23e51ad6-4f83-11ea-8240-001a4a05014a', 'Berg', 'Tessa', 'tberg@hw.ac.uk', 2, '2020-02-05', '10:28:10'),
('23e52864-4f83-11ea-8240-001a4a05014a', 'Kenwright', 'Benjamin', 'bjenwright@hw.ac.uk', 3, NULL, NULL),
('23e535ea-4f83-11ea-8240-001a4a05014a', 'Lemon', 'Oliver', 'olemon@hw.ac.uk', 4, '2020-02-04', '10:28:10'),
('23e54437-4f83-11ea-8240-001a4a05014a', 'Chumbe', 'Santiago', 'schumbe@hw.ac.uk', 5, NULL, NULL),
('23e55659-4f83-11ea-8240-001a4a05014a', 'Chantler', 'Mike', 'mchantler@hw.ac.uk', 6, '2020-02-18', '10:28:10'),
('23e56790-4f83-11ea-8240-001a4a05014a', 'Baillie', 'Lynne', 'lbaillie@hw.ac.uk', 7, NULL, NULL),
('23e578be-4f83-11ea-8240-001a4a05014a', 'Stewart', 'Rob', 'rstewart@hw.ac.uk', 8, NULL, NULL);

INSERT INTO `classes` (`class_name`, `class_code`, `lecturer`) VALUES
('Big Data Management', 'F20BD', '23e50bb7-4f83-11ea-8240-001a4a05014a'),
('Computing in the Classroom', 'F20CL', '23e51ad6-4f83-11ea-8240-001a4a05014a'),
('Computer Games Programming', 'F20GP', '23e52864-4f83-11ea-8240-001a4a05014a'),
('Conversational Agents & Spoken Language Processing', 'F20CA', '23e535ea-4f83-11ea-8240-001a4a05014a'),
('e-Commerce Technology', 'F20EC', '23e54437-4f83-11ea-8240-001a4a05014a'),
('Data Visualisation Analytics', 'F20DV', '23e55659-4f83-11ea-8240-001a4a05014a'),
('Advanced Interaction Design', 'F20AD', '23e56790-4f83-11ea-8240-001a4a05014a'),
('Distributed & Parallel Tech', 'F20DP', '23e578be-4f83-11ea-8240-001a4a05014a');

INSERT INTO `room_bookings` (`surname`, `forename`, `email`, `room_id`, `date`, `time`) VALUES ('Student', 'Generic', 'gstudent@hw.ac.uk', '9', '2020-02-15', '12:43:46');

/* EVENTS */

DROP EVENT IF EXISTS `delete-checkin`;
CREATE EVENT `delete-checkin`
  ON SCHEDULE EVERY 1 HOUR
  STARTS '2020-02-01 00:00:00'
  ON COMPLETION PRESERVE
DO
  UPDATE `employees` SET `room_id` = NULL, `last_check_in_date` = NULL, `last_check_in_time` = NULL;
