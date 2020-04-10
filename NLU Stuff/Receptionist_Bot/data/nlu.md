[comment]: # (Definitly need to expand on the basic intents)

##intent:greet
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

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?

## intent:book_room
- I'd like to book room [1.45](room_number)
- book me room [1.45](room_number)
- I'd like to book room [1.45](room_number) for [2](aomount) collegues
- book me room [G.7](room_number) for [3](amount) people
- could you please book me a room for [5](amount) people
- can I book the [Research Room](specific_room)
- can I book a [Research Room](specific_room) for [8](amount) people
- is the [Robotics Room](specific_room) free to be booked for [2] people
- am I able to get a free room for [12](amount) people

## intent:find_person
- where is [Tomasz Mosak](person)
- is [Cory Alexander](person) currently available?
- where will I find Mr [Convey](person)
- how can I find Mr [Frankland](person)
- is [Keir Convey](person) on campus today?
- will I find Mr [Mosak](person) on campus today?
- when is [Cory Alexander](person)s next lecture?
- is [Jack Walker](person) teaching a lecture?
- is [Matthew Frankland](person) taking a lecture today?
- what are the contact details for [Jack Walker](person)

# intent:future_events
- what is happening [tomorrow](date)
- any events on [this week](time_period)
- any events involving [Artificial Intelligence](subject) in the [near future](time_period)

[comment]: # (Need to finish custom python actions)

## intent:suggest_edit
- Pretty sure that the room for [Jack Walker](person) is incorrect
- office number for Mr [Alexander](person) is wrong
- The email for [Cory Alexander](person) is not available
- The email for [Matthew Frankland](person) is wrong
- I don't think [Tomasz Mosak](person) works here anymore
- The title for [Keir Convery](person) is wrong, it should be Mr instead of Mrs
- It's Mr [Convey](person) instead of Mrs [Convey](person)

## lookup:person
data/lookups/people.txt

## lookup:weekday
- monday
- tuesday
- wednesday
- thursday
- friday

## lookup:weekend
- saturday
- sunday

## lookup:specific_room
- Research Room
- Robotics Room

## regex:room_number
- \b(1\.\d{1,2}|G\.\d{1,2})\b

## regex:amount
- \b(\d{1,2})\b