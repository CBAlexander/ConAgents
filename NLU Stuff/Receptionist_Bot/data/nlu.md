## intent:greet
    - Hi
    - Hey
    - Hi bot
    - Hey bot
    - Hello
    - Good morning
    - hi again
    - hi folks
    - hi Mister
    - hi pal!
    - hi there
    - hi alana
    - hello alana
    - greetings alana
    - greetings
    - hello everybody
    - hello is anybody there
    - hello robot
    - hallo
    - heeey
    - hi hi
    - hey
    - hey hey
    - hello there
    - hi
    - hello
    - yo
    - hola
    - hi?
    - hey bot!
    - hello friend

## intent:goodbye
    - bye
    - goodbye
    - see you around
    - see you later
    - that is all, thank you

## intent:affirm
    - yes
    - indeed
    - of course
    - that sounds good
    - correct

## intent:deny
    - no
    - never
    - I don't think so
    - don't like that
    - no way
    - not really

## intent:stop
    - ok then you cant help me
    - that was shit, you're not helping
    - you can't help me
    - you can't help me with what i need
    - i guess you can't help me then
    - ok i guess you can't help me
    - that's not what i want
    - ok, but that doesnt help me
    - this is leading to nothing
    - this conversation is not really helpful
    - you cannot help me with what I want
    - I think you cant help me
    - hm i don't think you can do what i want
    - stop
    - stop go back
    - do you get anything?
    - and you call yourself bot company? pff
    - and that's it?
    - nothing else?

## intent:check_in
    - please check [Jack Walker](person) in to room [1.46](check_in_room)
    - check [Matthew Frankland](person) in to room [1.46](check_in_room)
    - can I check in [Tomasz Mosak](person) to room [1.46](check_in_room)
    - check in [Keir Convery](person) to room [1.46](check_in_room)

## intent:bot_challenge
    - are you a bot?
    - are you a human?
    - am I talking to a bot?
    - am I talking to a human?

## intent:cancel_room
    - I'd like to cancel room [1.46](cancel_room)
    - cancel room [1.46](cancel_room)
    - I'd like to cancel room [1.46](cancel_room) on [Monday](day)
    - cancel room [1.46](cancel_room) on [Monday](day)
    - can I cancel the [Research Room](cancel_room)
    - cancel a room for [Tuesday](day)
    - am I able to cancel my free room for [Tuesday](day)
    - cancel  room [1.46](cancel_room) for [3](amount) people
    - could you please cancel my room for [5](amount) people
    - can I cancel a [Research Room](cancel_room) for [8](amount) people
    - is the [Robotics Room](cancel_room) free to be cancelled which was booked for [2] people
    - am I able to get a cancel my room for [12](amount) people on [Wednesday](day)

## intent:book_room
    - I'd like to book room [1.46](book_room)
    - book room [1.46](book_room)
    - I'd like to book room [1.46](book_room) on [Monday](day)
    - book room [1.46](book_room) on [Monday](day)
    - can I book the [Research Room](book_room)
    - I'd like to book room [1.46](book_room) for [2](amount) collegues
    - book me room [1.46](book_room) for [3](amount) people
    - could you please book me a room for [5](amount) people
    - can I book the [Research Room](book_room)
    - can I book a [Research Room](book_room) for [8](amount) people
    - is the [Robotics Room](book_room) free to be booked for [2] people
    - am I able to get a free room for [12](amount) people on [Wednesday](day)
    - book a room for [Tuesday](day)
    - can I book a room on [Monday](day)
    - book some room [1.45](book_room) I made from [Monday](day)
    - book me room [1.46](book_room) for [3](amount) people
    - could you please book me a room for [5](amount) people

## intent:find_person
    - where is [Tomasz Mosak](person)
    - is [Cory Alexander](person) currently available?
    - find [Jack Walker](person)
    - get me [Matthew Frankland](person)
    - I want to locate [Keir Convey](person)
    - is [Keir Convey](person) on campus today?
    - is [Jack Walker](person) teaching a lecture?
    - is [Matthew Frankland](person) taking a lecture today?

## intent:future_events
    - any events upcoming in the [Research Room](room)?
    - what events are going to take place in [1.46](room)?
    - is there anything happening in [1.46](room) in the near future?
    - are there any bookings in room [1.46](room) soon?

## intent:suggest_edit
    - Pretty sure that the room for [Jack Walker](person) is incorrect
    - office number for [Cory Alexander](person) is wrong
    - The email for [Cory Alexander](person) is not available
    - The email for [Matthew Frankland](person) is wrong
    - I don't think [Tomasz Mosak](person) works here anymore
    - The title for [Keir Convery](person) is wrong, it should be Mr instead of Mrs
    - The name of [Jack Walker](person) seems wrong
    - who do i report to that [Tomaz Mosak](person)'s name is spelt wrong

## lookup:person
    data/lookups/people.txt

## lookup:day
    data/lookups/day.txt

## regex:amount
    - \b(\d{1,2})\b

## regex:book_room
    - \b1.\d{1,2}|Research Room|Robotics Room\b

## lookup:cancel_room
    - \b1.\d{1,2}|Research Room|Robotics Room\b
