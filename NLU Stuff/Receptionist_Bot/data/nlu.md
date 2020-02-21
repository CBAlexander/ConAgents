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
- I'd like to book room [G.7](room_number)
- book me room [G.2](room_number)
- could you please book me a room

## intent:find_person
- where is [Tomasz Mosak](person)
- is [Cory Alexander](person) currently available?
- where will I find [Mr Convey](person)

# intent:future_events
- what is happening [tomorrow](date)
- any events on [this week](time_period)
- any events involving [Artificial Intelligence](subject) in the [near future](time_period)

[comment]: # (Need to create custom python actions for the above)

## intent:suggest_edit
- Pretty sure that the room for [Jack Walker](person) is incorrect
- The email for [Cory Alexander](person) is not available
- I don't think [Tomasz Mosak](person) works here anymore

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

## regex:room_number
- G.[1-7]{1}

[comment]: # (Need to rework regex for room number)