## find_person
* greet
    - utter_greet
* find_person
    - utter_find
    - action_find_person
    
## booking
* greet
    - utter_greet
* book_room
    - utter_book
* affirm
    - utter_details_requested
    - action_display_booking_form
* deny
     - utter_deny

## future_events
* greet
  - utter_greet
* future_events
  - utter_future_events
  - action_find_event

## suggest_an_edit
* greet
  - utter_greet
* suggest_edit
  - utter_edit
* affirm
  - action_send_email
* deny
   - utter_deny
   
## cancellation
* greet
 - utter_greet
* cancel_room
 - utter_cancel
* affirm
 - action_cancel_booking
* deny
  - utter_deny
  
## check_in
* greet
  - utter_greet
* check_in
  - utter_check_in
  - action_check_in

## stop_system
* goodbye
  - utter_goodbye
* stop
  - utter_stop
