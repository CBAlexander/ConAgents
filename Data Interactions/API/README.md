# Conv-Agents API

#### Notes

All Data Should Be Sent POST in Form-Data Format

## Book Room
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/book_room.php)

Sudo Name Of Building From Database Rather Than Full Name
Length of Time Is In Minutes
Date and Time Can't Be Older Than Present Date

| Key             | Exemplar       | Special Format |
| --------------- | -------------- | -------------- |
| forename        | Matthew        |                |
| surname         | Frankland      |                |
| email           | mf48@hw.ac.uk  |                |
| room_name       | 1.41           |                |
| building_name   | EM             |                |
| book_date       | 2020-02-25     | YYYY-MM-DD     |
| book_time       | 00:00          | HH:MM          |
| length_min      | 20             |                |

## Cancel Room
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/cancel_room.php)

Sudo Name Of Building From Database Rather Than Full Name

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

| Key             | Exemplar        | Special Format |
| --------------- | --------------- | -------------- |
| employee_email  | mf48@hw.ac.uk   ||

## Future Events
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/future_events.php)

Sudo Name Of Building From Database Rather Than Full Name

| Key             | Exemplar   | Special Format |
| --------------- | ---------- | -------------- |
| room_name       | 1.41       ||
| building_name   | EM         ||

## Employee Check In
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/employee_check_in.php)

Employee Email Must Be In Employee Table Of Database
Sudo Name Of Building From Database Rather Than Full Name

| Key             | Exemplar      | Special Format |
| --------------- | ------------- | -------------- |
| employee_email  | mf48@hw.ac.uk ||
| room_name       | 1.41          ||
| building_name   | EM            ||

## Suggest An Edit
### [Request URL](https://www.matthewfrankland.co.uk/conv-agents/suggest_edit.php)

Email Does Not Have To Be Registered

| Key             | Exemplar                                     | Special Format |
| --------------- | -------------------------------------------- | -------------- |
| recipient_email | mf48@hw.ac.uk                                ||
| message         | Anything You Want To Send To The Above Email ||
