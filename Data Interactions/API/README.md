# Conv-Agents API

#### Notes

All Data Should Be Sent POST in Form-Data Format

## Book Room
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/book_room.php)

* Sudo Name Of Building From Database Rather Than Full Name
* Length of Time Is In Minutes
* Date and Time Can't Be Older Than Present Date
* Number of People are number of those who would use the room during a booking

| Key             | Exemplar       | Special Format |
| --------------- | -------------- | -------------- |
| forename        | Matthew        |                |
| surname         | Frankland      |                |
| email           | mf48@hw.ac.uk  |                |
| room_name       | 1.41           |                |
| book_date       | 2020-02-25     | YYYY-MM-DD     |
| book_time       | 00:00          | HH:MM          |
| length_min      | 20             |                |
| num_people      | 5             |                |

## Cancel Room
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/cancel_room.php)

* Sudo Name Of Building From Database Rather Than Full Name

| Key             | Exemplar       | Special Format |
| --------------- | -------------- | -------------- |
| forename        | Matthew        |                |
| surname         | Frankland      |                |
| email           | mf48@hw.ac.uk  |                |
| room_name       | 1.41           |                |
| building_name   | EM             |                |
| book_date       | 2020-02-25     | YYYY-MM-DD     |
| book_time       | 00:00          | HH:MM          |


## Find Person
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/find_person.php)

Sudo Name Of Building From Database Rather Than Full Name

| Key               | Exemplar        | Special Format |
| ----------------- | --------------- | -------------- |
| employee_forename | Matthew         |                |
| employee_surname  | Frankland       |                |

## Future Events
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/future_events.php)

Sudo Name Of Building From Database Rather Than Full Name

| Key             | Exemplar   | Special Format |
| --------------- | ---------- | -------------- |
| room_name       | 1.41       ||

## Employee Check In
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/employee_check_in.php)

Employee Must Be A Name In Employee Table Of Database
Sudo Name Of Building From Database Rather Than Full Name

| Key             | Exemplar      | Special Format |
| --------------- | ------------- | -------------- |
| employee  | Matthew Frankland ||
| room_name       | 1.41          ||

## Suggest An Edit
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/suggest_edit.php)

Suggestion that a person's details may be wrong

| Key             | Exemplar                                     | Special Format |
| --------------- | -------------------------------------------- | -------------- |
| person              | Jack Walker                               ||

## Find A Room
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/find_room.php)

Find a room name that can accomodate a certain number of people

| Key             | Exemplar                                     | Special Format |
| --------------- | -------------------------------------------- | -------------- |
| num_people              | 2                               ||
| date              | 2020-04-19                             ||
