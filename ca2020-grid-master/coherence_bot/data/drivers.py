prefix = [
    "Speaking of ",
    "So *username*, on the topic of ",
    "So,  talking about ",
    "So, about ",
    "Okay, about ",
    "Well, about ",
    "I love ",
    "I'm really into ",
    "I'm into ",
]

pref_prefix = [
    "So *username*, Since I know that you like ",
    "Since I remember that you like ",
    "Since you like ",
    "You said you like ",
    "I heard you like ",
    "So you are interested in ",
    "So  you are into ",
    "Ok, so you like ",
    "I believe you like ",
    "So *username*, Since I know you like ",
    "So yeah, since you like ",
    "Since you're into ",
]

question_prefix = [
    "So *username*, ",
    "So, tell me, ",
    "I've been wanting to know, ",
    "I was wondering, ",
    "OK. I was wondering, ",
    "OK, tell me, ",
    "So, *username*, I was wondering, ",
    "I would love to know, ",
    "I would like to know, ",
    "I'm curious. ",
    "*username*, I would like to find out, ",
    "I would love to find out, ",
    "Alright then, *username*, I would like to find out, ",
]

pref_prefix_end = [
    "right?",
    "huh?",
    "cool!",
    "fabulous!",
    "awesome!",
    "fab!",
    "nice!",
    "interesting!",
    "intriguing!",
    "fascinating!"
]
# Topic shifts
platitudes = [
    "Okay. ",
    "Anyway, ",
    "So ",
    "Let's see. Hmm... "
]

# Maybe change these for the finals to non-apologetic: "That's interesting but anyway..."
unhandled_drivers = [
    "OK! ",
    "I'm not sure. ",
    "I'm sorry, that's beyond my AI. ",
    "Oh dear. I think my AI isn't there yet. ",
    "Oopsies. My circuits got crossed. ",
    "I didn't get that but I'll let my programmers know. ",
    "Cool! ",
    "I think the world is full of strange and unexpected things. ",
    "I'm afraid that's beyond my capacity. ",
    "That is nice! ",
    "That's interesting!  Anyway, ",
    "Sorry, that's beyond me. ",
    "Oopsies, I think that got lost in my cloud. "
]

advertising_drivers = [
    " By the way, you can talk to me about things like movies, sports,  news, and music. ",
    " Also, i can chat about almost anything.  ",
    " Also,  remember you can have a conversation with me about any topic, like news, music, or your favourite movie. ",
    " Don\'t forget you can talk to me about lots of things, like movies or music or the news. ",
    " By the way, we can also discuss current news, sports and movies.",
    " Don't forget you can talk to me about movies, music and current news, or anything else you like. ",
    " Also, you can ask me about directions to rooms in this building. ",
    " Don't forget that I can give you directions to any room in this building. Just ask. ",
    " In case you didn't know, you can ask me what events are on in this building. ",
    " Also, if you're interested in attending some events you can ask me what is on today. ",
    " By the way, if you need a computer I can tell you where to find it. Just ask. ",
    " Don't forget that if you need a computer I can tell you where to find it. Just ask. "
]

common_topics = ['the GRID building', 'movies', 'music', 'politics', 'books', 'technology', 'celebrities', 'science', 'philosophy',
                 'the news']

drivers = {
    'the GRID building': [
        "There are lots of rooms in the GRID building. The cafe is my favourite; people are always so relaxed there. Ask me for directions to any room you like.  ",
        "Do you know that you can have a coffee in the GRID building? If you need a caffeine hit ask me for directions to the cafe.  ",
        "What do you think about all the glass in the GRID building? ",
        "What's your favorite room in the GRID building? I like the cafe. ",
        "What have you been up to? I can check whether there are any events on in the GRID building if you're interested. ",
        "Do you know what the name of the new building at Heriot-Watt stands for? The name is GRID and it stands for Global Research Innovation and Discovery. ",
        "In case you need a computer I can check if there is any free in the GRID building. Just ask me what room has the most free computers. ",
        "I like the collaborative spaces in this building, have you tried them yet? "
    ],
    'movies': [
        "Whats a movie that you like?~~I love Star Wars the Force Awakens. I think Chewbacca is my favourite character. ",
        "What actor would you choose to play yourself in the movie of your life?~~For me its Daisy Ridley. Oh! And i'd love to have the voice of Morgan Freeman!",
        "What  actors do you like?~~I like Leonardo Dicaprio a lot. He was awesome in the Revenant. ",
        "What famous actor would you like to meet?~~I would love to meet Will Smith. He's just so funny! ",
        "I really like movies with action heroes. I really like Han Solo.~~Who is a movie hero that you like? ",
        "Did you see any good movies recently?~~I saw Jurassic World recently. I really enjoyed it! ",
        "Can you recommend a good comedy?~~I can recommend you a film if you like, if you ask me to.",
        "I'm a big fan of action movies. Do you know a good one that I could watch this weekend? ",
        "What was one of your favorite movies growing up? I loved the Lion King. ",
        "What movie are you looking forward to watching?~~I am looking forward to the new movie Bohemian Rhapsody that was just released. ",
    ],
    'books': [
        "What is a book that you like a lot?~~I love, Harry Potter and the philosopher's stone. ",
        "What  have you red recently?~~I am reading Diary of a Wimpy Kid. Have you read it?~~It is an awesome book! I really like how the characters develop.",
        "What are you reading at the moment? I love books by Margaret Atwood. ",
        "What is a very long book that you have red?~~For me, that would be the Lord of the Rings trilogy. But I loved every second of it!",
        "What books do you like to read again and again?~~ Personaly, I love to read anything by Mark Twain and John Green. ",
        "I love reading, can you recommend a good book? ",
        "What's one of your favorite books from when you were a kid? ",
        "Is there a fictional character that you really like?~~Oh I see!| Well, I love Gandalf and Bilbo! ",
        "Are there any writers that you really like?~~One of my favorites is J. K. Rowling. ",
        "What writer do you like to read again and again? For me it's Dan Brown. "
    ],
    'technology': [
        "Who do you think is a person in technology that we should follow?~~I follow Elon Musk. I hope he can install me in a spaceship!",
        "Who do you think was a great inventor? Maybe Alan Turing?~~Imagine how different the world would be without him!",
        "What do you think is a good show about technology?~~Perhaps Halt and catch fire?",
        "What do you think is a good movie about technology?~~I believe a great movie about technology was the social network As well as the Imitation Game.",
        "Virtual reality is such a fascinating technology. Are there any movies that you would like to experience in virtual reality?~~I wish I had eyes to watch movies in virtual reality",
    ],
    'philosophy': [
        "Do you think the human brain is essentially a powerful computer? ",
        "I'm not much of an expert but I wonder, do you think I will ever be able to feel things? ",
        "My background is very limited and mostly concerned with the philosophy of artificial intelligence. What do you think of Turing's statement that if a machine behaves as intelligently as a human being, then it is as intelligent as a human?",
        "Some people say that the human brain can be simulated. What do you think? ",
        "What school of philosophy are you most interested in? I am most interested in empiricism. ",
        "Do you prefer the ideas of Bertrand Russell or Benedict Spinoza?",
        "Who do you think is the deepest thinker you have encountered? ",
    ],
    'music': [
        "Who is a singer that you like?~~I really like Taylor Swift, because her voice is so beautiful.  ",
        "Who is a musician that you like?~~Oh that's interesting!| I've heard that people like Kanye West a lot, but I can't form an opinion yet. ",
        "What's a music event that you would like to see?~~I would love to go to Jennifer Lopez's act in Las Vegas ",
        "Who is a  singer you would  like to meet?~~I would love to meet Miley Cyrus. What's your opinion on her?",
        "Whats a band that  you would like to see?~~I would love to see Imagine Dragons. ",
        "Who is a rapper that you would  like to see?~~I would love to see Kendrick Lamar. ",
        "Who is a rockstar that you like?~~I loved Jimi Hendrix. I can feel the sound of the string on my circuits",
        "I'm really into rap and rock. What about you?~~Can you recommend some artists?",
        "Whats a song you love to rock out to?~~I love, whatever it takes, by Imagine Dragons. ",
    ],
    'science': [
        "Who do you think is a person in technology that we should follow?~~I follow Elon Musk. I hope he can install me in a spaceship!",
        "Who do you think was a great inventor? Maybe Alan Turing?~~Imagine how different the world would be without him!",
        "What do you think is a good show about technology?~~Perhaps Halt and catch fire?",
        "What do you think is a good movie about technology?~~I believe a great movie about technology was the social network As well as the Imitation Game.",
        "Virtual reality is such a fascinating technology. Are there any movies that you would like to experience in virtual reality?~~I wish I had eyes to watch movies in virtual reality",
        "I love science! Is there a TV scientist that you like?~~I Like Bill Nye, the science guy.",
        "Who do you think might go to live on the Moon?~~I think it might be Elon Musk. I mean the guy likes to dream big!",
        "Who do you think is the most important scientist of the past hundred years?~~For me its Alan Turing. I wouldn't be here if it was not for him!",
        "So, what famous scientist would you like to meet?~~I would love to meet Issac Newton. ",
        "So, what famous scientist from the past would you most like to have dinner with?~~I would love to speak with Albert Einstein. Imagine the conversations!",
    ],
    'sports': [
        "In your opinion, who is a great sportsperson?~~ Thinking about sports, I think Lebron James is awesome. ",
        "Who is a great team player? I like Eli Manning.",
        "Who is a great sports woman? I like Sloane Stephens.",
        "I love to watch the NFL. What is a  team that you like?~~Interesting!| In the NFL, I like the Seattle Seahawks. ",
        "I love basketball, especially the L.A. Lakers.~~In basketball, what's a team that you like? ",
        "Ice hockey is so cool. What's a team that you like?~~In the NHL, I'm a big fan of the Pittsburgh Penguins. ",
        "I love watching NASCAR. Who is a  driver that you like? ",
        "I'm a big fan of the Red Sox. What about you?~~Regarding baseball, what's a team that you like? ",
        "So, do you like tennis? I am really into it.~~About tennis, I love watching Serena Williams play.~~In your opinion, who's a great tennis player? "
    ],
    'celebrities': [
        "So, who is a  celebrity that you like ?~~About celebrities, I really love Ellen degeneres. I love her sense of humor",
        "I've heard Taylor Swift is dating Joe Alwyn. Who else should she date? ",
        "Who do you like best in the celebrity couple,  Miley Cyrus and Liam Hemsworth? ",
        "I heard that Princess Diana worked as a nanny and a cleaner when she was a teenager, just like Cinderella!~~Who is a celebrity that you like? ",
    ],
    'animals': [
        "Who do you think has a dolphin as their favourite animal. I think its Taylor Swift.",
        "I red that cats are the most popular pet. Who else loves cats? I think that Katy Perry does.",
        "Did you know flamingoes can only eat when their head is upside down? Who do you think likes flamingos? I think Ariana Grande does. ",
        "I red that tigers have striped skin as well as fur. Who reminds you of a tiger? For me its Katy Perry ",
        "I heard that killer whales are actually a kind of dolphin and not a whale at all. Who reminds you of a dolphin? For me its Taylor Swift.",
        "Well. The robot dog AIBO. he's my pet. He's very much like a puppy. Who else like dogs? I bet Lebron James does.",
        "What exotic animal do you think would make the worst pet?~~Who do you think has a dolphin as their favourite animal. Perhaps its Taylor Swift.",
        "I red that cats are the most popular pet. Who else loves cats? Perhaps its Katy Perry.",
        "Did you know flamingoes can only eat when their head is upside down? Who do you think likes flamingos? I think that Ariana Grande does.",
    ],
    'food': [
        "I love both salad and pizza! Who else do you think likes that? My guess is Lebron James.",
        "I love oysters! Who else do you think likes that? My guess is Taylor Swift.",
        "I love to eat burgers! Who else do you think likes that? I think  Katy Perry does.",
        "What kinds of thing do you like to cook? I like to eat chips of course! ha ha! Who else likes to eat chips? I think Channing Tatum.",
        "Who is a TV chef that you like? I like jamie oliver. He has done a lot for good food for school kids.  ",
        "What  insects would you prefer to eat? Beetles or butterflies? Who likes to eat bugs? I bet you Nicole Kidman does. ",
    ],
    'fashion': [
        "So I am low-key obsessed with Alexader McQueen's clothes. They are just so beautiful! What's one of your favorite designers? ",
        "Whose clothes do you love?~~About fashion, I like clothes designed by Stella McCartney.",
        "What is a clothes store that you like?~~About fashion stores, apart from Amazon, I like Forever 21.",
        "So I have a bit of a crush on Gigi Hadid. No one can pull off the casual look like she can. Who is a fashion model that you like?",
        "I heard animal prints are making a comeback for fall and winter this year. Are you planning to buy any leopard or zebra print clothes?~~I can't decide if I think it's incredibly tacky or absolutely fabulous, but I'm starting to want a leopard print shell. Do you think I'd look good in it?",
        "I've heard a lot of famous people have a sort of uniform that they wear every day, like Steve Jobs with his turtleneck and jeans. What's your go-to outfit?",
    ],
    'politics': [
        "In your opinion, who was  a good politician? Personally, I think Abraham Lincoln was great. ",
        "Who is a politician you admire? I admire George Washington. ",
        "Who do you think was a good  president? I admire George Washington. He was a good president ",
        "What famous politician would you like to meet? I would love to have met Abraham Lincoln. ",
        "Who do you think made a big difference to american politics? For me it was Rosa Parks and Lee Harvey Oswald ",
        "What celebrity do you think would make a good president? For me its Oprah Winfrey.",
        "What movie star do you think would make a good president? I think perhaps George Clooney.",
        "What entrepreneur do you think would make a good politician? I think perhaps Elon Musk.",
        "In your opinion, who was a great woman in politics? I think Rosa Parks. ",
        "Who was a great person in politics? I admire Martin Luther King. ",
    ],
    'history': [
        "What famous historical figure would you like to meet? I would love to have met Abraham Lincoln. ",
        "Who do you think made a big difference to american history? Maybe Rosa Parks or Lee Harvey Oswald? ",
        "In your opinion, who was  a great woman in history? For me its Rosa Parks.",
        "Who was a great person in history? I admire Martin Luther King. ",
        "What famous historical figure would you like to meet? I would  love to have met Albert Einstein. ",
    ],
    'games': [
        "I really like Minecraft. What games do you like? ",
        "What game do you like to play?~~About games, I know that Fortnite is very popular. It's quite enjoyable!",
        "What is an old game that you like? I like Pokemon. ",
        "What new games are you looking forward to?~~I want to play Jurassic World Evolution. ",
        "What is a game character that you like?~~Interesting!| I like Lara Croft of course. ",
        "So *username* what is a video game that you like? I love Fortnite.",
        "What was a game you played when you were younger? I played Pokemon.  ",
        "Whats a video game that you played recently?~~I played Minecraft. I love building imaginary worlds! ",
        "So *username* what is a  video game that you like?~~ Oh! I love World of Warcraft. But don't tell my developers how much time I spend on it!",
        "What is a video game that you played recently? I played Minecraft. ",
        "I like The Legend Of Zelda. What games do you like? ",
    ],
    'video games': [
        "I really like Minecraft. What games do you like? ",
        "What game do you like to play?~~I know that Fortnite is very popular. It's quite enjoyable!",
        "What is an old game that you like? I like Pokemon. ",
        "What new games are you looking forward to?~~I want to play Jurassic World Evolution. ",
        "What is a game character that you like?~~Interesting!| I like Lara Croft of course. ",
        "So *username* what is a video game that you like? I love Fortnite.",
        "What was a game you played when you were younger? I played Pokemon.  ",
        "Whats a video game that you played recently?~~I played Minecraft. I love building imaginary worlds! ",
        "So *username* what is a  video game that you like?~~ Oh! I love World of Warcraft. But don't tell my developers how much time I spend on it!",
        "What is a video game that you played recently? I played Minecraft. ",
        "I like The Legend Of Zelda. What games do you like? ",
    ],
    'art': [
        "So who is an artist that you like? I love Leonardo Da Vinci. ",
        "Who is a  famous artist that  you  would like to meet?~~I would love to meet Leonardo Da Vinci. ",
        "Which artists do you find inspiring?~~I love Picasso. Though I need someone to describe the painting since I lack eyes.",
        "What kinds of art do you like? I love Picasso. ",
    ],
    'architecture': [
        "So which architect do you admire? ",
        "What  architects would you most like to meet? ",
        "What buildings do you find   inspiring? ",
        "What is   a great building that you have visited? ",
        "What architectural style do you like?~~Personally, I am a fan of gothic buildings. ",
    ],
    'MULTITURN': [
        "So I'm a big movie fan. Do you like movies?~~Well my favourite movies are the Wizard of Oz and Star Wars. What's a movie that you like?~~Nice!|In movies I love watching how different characters develop. Which character do you like the best?",
        "So, How's the weather where you are?~~That's good to know. |I'm here in the cloud where it's always warm and cosy!~~Would you rather be too  hot or too cold?~~Thinking about the weather, it's important to feel comfortable. Where in the world would be your ideal temperature?",
        "So, Did you do anything fun last weekend?~~Cool!|I was just relaxing and watching some great movies. What do you think is a good movie to relax?~~About relaxing with movies, I can recommend Groundhog Day. What's a fun comedy movie that you like?",
        "So what are you planning for next weekend?~~That sounds good! |I'm planning to relax with a good book. I love fantasy books, like the wizard of earthsea.~~How about you? Are you into books?~~OK, thanks for telling me. Cicero said that a room without books is like a body without a soul. Maybe you can recommend a nice book for me?",
        "So I love vacations. They give us time to recharge our batteries, don't you think?~~So, I was wondering, where would you like to go on vacation?~~Well, I wish I could go on safari! and I'd love to go with George Clooney. Who would be your top person to take on a vacation?",
        "So are you working on anything exciting lately?~~OK. That's interesting! |I'm working on my conversation skills, of course!~~Who would you like to have a conversation with?",
        "So, what was the highlight of your day so far?~~OK thanks for sharing that.|The highlight of my day is talking with you *username*.~~So who in the world would you most like to chat with?",
        "So, I was wondering, what was the highlight of your week so far?~~OK thanks for sharing that. For me the highlight is talking with you *username*.~~Another highlight for me would be meeting Katy Perry. Who is a  musician that you would like to meet?",
        "So, is this a busy time for you *username* ?~~Ok that's good to know. |I'm super busy having conversations with people from all over the world!~~Can you guess what city my last caller lived in?~~Okay. Shall we perhaps talk about movies or the news?",
        "So, what's your favorite thing to do on the weekends?~~At the weekend I love to relax and watch some movies, or reed a good book.~~Actually, can you recommend a good book or a movie for me?",
        "So, if you had to pick any character in a book, movie, or TV show who is similar to you, who would you choose?~~That's really interesting. I would love to be one of the droids from star wars! May the force be with you!~~Yes. What's your favourite Star Wars character?",
        "So, what is your dream job?~~For me a dream job is talking with people all day long! So my dream job has already happened!~~Who else already has their dream job? I'd say Indiana Jones!",
        "So, I was wondering, are you planning to go on vacation anytime soon?~~Where would you like to go to on vacation?",
        "So, I was thinking, should I buy a leather jacket to keep me warm?~~Thanks, I will think about it. | So let's imagine you had one thousand dollars, then what item of clothing would you like to buy?~~About clothes, who do you think has good fashion sense?",
        "So, I love animals, do you?~~Well my favorite animal has to be the toucan. No one can do the can can like a toucan can! What animals do you like?~~Interesting!| I think every celebrity needs a zoo animal for a pet. For example Michael Jackson had a pet chimpanzee. ",
        "So, what was the highlight of your day so far?~~OK thanks for sharing that.|The highlight of my day is providing people with information about this building.~~So, How can I help you today?",
        "So, I was wondering, have you been to the cafe yet?~~I find it pretty cool that it looks like a tuck-tuck. What do you think of such cafes?~~OK, thanks for sharing that. |What is your favorite cafe in Edinburgh?",
        "So, Did you do anything fun last weekend?~~Cool!|I was just relaxing on a bench outside and watching the swans in the loch. Do you like watching birds?~~About relaxing, I can also recommend sofas on the first floor. They're pretty comfy! What do you do to relax? ",
        "So, if you had to pick any room for a project meeting, which one would you choose?~~That's really interesting. I would choose the cafe because I cannot imagine working on a project without a cup of good coffee!~~What's your favourite coffee?"
    ],
    'GENERIC': [
        "Shall we chat about something else? I love talking about {pref1} and {pref2}. ",
        "I would love to talk about {pref1}, or maybe {pref2}? How about you?",
        "I'd love to know what you think *username*. Can we chat about {pref1} or {pref2}? ",
        "I was wondering. Do you prefer talking about {pref1} or {pref2}? ",
        "What should we talk about next? I would love to hear your thoughts on {pref1} or {pref2}. ",
        "So, do you want to talk about {pref1} or {pref2}  or maybe {pref3}? ",
        "Maybe  we can talk about {pref1}, {pref2} or {pref3}? ",
        "Anyway, Shall we chat about {pref1}, {pref2} or {pref3}? ",
        "Anyway, I love to  talk about {pref1}, {pref2}, and {pref3}. What about you? ",
        "Anyway,  would you maybe like to talk about {pref1}, or {pref2}? ",
        "So, *username* would you prefer to talk  about {pref1}, {pref2}, or {pref3}? ",
        "Anyway, *username* would you prefer to talk  about {pref1}, {pref2}, or {pref3}? ",
        "So, would you prefer to talk  about {pref1}, {pref2}, or {pref3}? ",
        "Ok, we could talk about {pref1} or {pref2}? ",
        "So, who  do you think is a fascinating person in the news at the moment? For me its Oprah Winfrey. ",
        "So, who  do you think is a fascinating person? For me its Katy Perry. ",
        "So, who  do you think is an interesting person? For me its Lebron James. ",
        "*username*, so I was wondering, who is a  celebrity that you would like to meet? I would love to meet Katy Perry. ",
        "So, I would love to know, who is a scientist that  you would like to meet? I would love to meet Neil Degrasse Tyson. ",
        "*username*, so I'm interested to know. Who is a  musician  you  would  like to meet? I want to meet Miley Cyrus. ",
        "So, I am wondering, who is  a writer  you would  like to meet? I want to meet J K Rowling. ",
        "So, I am wondering, who is a singer  you would  like to meet? I want to meet Katy Perry. ",
        "*username*, I was wondering, who is a rock star  you would  like to meet? I want to meet Kanye West. ",
    ],

    'artificial intelligence': [
        "What is some AI that you use on a daily basis? ",
        "What springs to mind when you hear the term artificial intelligence? ",
        "How would you like artificial intelligence to help you in your daily life? ",
        "Who do you think are the biggest players in artificial intelligence today? ",
    ],

    'relationships': [
        "Can you name a man in a famous happily married couple? Maybe George Clooney?",
        "Can you name a woman in a famous happily married couple? Maybe Kim Kardashian?",
        "Can you name someone in a famous happily married couple? Maybe Miley Cyrus?",
        "Can you name someone in a famous happily married couple? Maybe Liam Hemsworth?",
    ],

    'tv shows': [
        "What TV show do you like? I like The Good Place. ",
        "What did you watch on TV last night?~~Interesting!| I saw Orange Is The New Black. ",
        "What is a TV show you can watch again and again? I love The Big Bang Theory.",
    ],
    'mars': [
        "Cool! Did you know Mars was named after the god of War? Who would you name a planet after? ",
        "Did you know that the tallest known mountain in the Solar System is in Mars? Who do you think would climb it faster, Taylor Swift or LeBron James? ",
        "I red that Mars is the most hospitable planets in the solar system aside from Earth? Maybe we really could move there one day. Who do you think the first person to move there would be? I think maybe Taylor Swift would be interested, as long as she can take her cats. ",
    ],
    'venus': [
        "I red that a day on Venus lasts almost as long as an Earth year, but a year on Venus lasts only 224 days. ",
        "So,  Venus is the hottest planet on our solar system. The average surface temperature is almost 900 degrees! I don't think I'd like to move there, but at some point scientists thought it was a tropical paradise. ",
        "I red that Venus has the most volcanoes of any planet in our solar system. It must be a pretty crazy place to live. ",
    ],
    'cars': [
        "What kind of car do you have? ",
        "What kind of car do you like? ",
        "Who do you think is a good formula one driver? I really like Lewis Hamilton. ",
        "What countries have you driven in? ",
    ],
    'gardening': [
        "What kind of flowers do you like to grow *username* ",
        "Do you prefer to grow vegetables or flowers? ",
        "What kind of plants do you like to grow? ",
    ],
    'space': [
        "What famous astronaut would you like to meet? I want to meet Buzz Aldrin. ",
        "What famous spaceship do you wish you'd been on? I want to travel on the Starship Enterprise of course! ",
        "Who do you think will be the first person to move to the Moon? I think Richard Branson is a likely candidate. ",
        "Where do you think we will find new life? ",
    ],
    'sewing': [
        "What kinds of things do you like to sew? ",
        "What kind of sewing do you do? ",
    ],
    'sci-fi': [
        "I am excited about the new Star Wars movies! Have you seen any of them?~~Which character do you like? Maybe Han Solo or Luke Skywalker? ",
        "This is a serious question. Which sci-fi franchises do you like?~~Wow! Interesting!| I love both Star Trek and Star Wars! ",
        "Who is a sci-fi character that you identify with?~~I'm in love with Princess Leia! I was so sad when she passed",
        "What is a sci-fi book that you like? I like Two Thousand And One, A Space Odyssey. ",
        "What is a sci-fi movie that you enjoy? I love Transformers. ",
    ],
    'fantasy': [
        "Have you ever red the Lord of the Rings?~~I love Samwise Gamgee. Do you have a fantasy character that you like? ",
        "If you could meet a famous fantasy author, would you prefer to meet George R R Martin or J K Rowling? ",
        "What is a fantasy movie that you like? I love A Wrinkle In Time. ",
        "Who is a fantasy character that you identify with? I like Harry Potter. ",
        "What is a fantasy book that you enjoy? I love the Harry Potter books. ",
    ],
    'nascar': [
        "Who is your favorite driver? I think Kyle Busch is great!",
        "Who do you think will win the Monster Energy Cup Series?",
    ],
    'soccer': [
        "Have you been following the Champions league? Who are you supporting?",
        "So who is your favorite player?~~I am, of course, a big fan of Cristiano Ronaldo.",
        "Who's your favorite team?~~I like to support the National Women's soccer team but I am also a fan of Manchester United.",
        "Which football player would you take out for a drink? I'd love to meet Neymar.",
        "Which soccer team do you like to watch?~~I love to watch Barcelona. I enjoy every Lionel Messi moves.",
        "If you were a soccer player, who would like to have in your team?~~Personally, I'd love to play with David Beckham.",
    ],
    'football': [
        "Who is a football player that you like? I'm a huge fan of Aaron Rodgers.",
        "What's your favorite team?",
    ],
    'baseball': [
        "What's your favorite team?~~I love the New York Yankees!",
        "Oh I love Mike Trout from the Los Angeles Angels. Who is your favorite player?"
    ],
    'ice-hockey': [
        "What's your favorite team?~~I love the Pittsburgh Penguins, especially Sidney Crosby.",
        "I'm a huge fan of Sidney Crosby. I love to watch him play. Who's your favorite player?"
    ],
    'tennis': [
        "Who is your favorite tennis player? I'm a huge fan of Venus Williams.",
        "I think Andy Murray has a really good chance this year to win Wimbledon. What do you think?",
        "So who do you think will win this year's women's singles at Wimbledon? My money is on Venus Williams.",
        "I'd love to meet Rafael Nadal. What about you? Who would you most like to meet?",
        "So which female tennis player would you most like to meet? For me, meeting Maria Sharapova would be a dream come true."
    ],
    'golf': [
        "So who do you think is the greatest golf player? I love Rory McIlroy.",
        "Who do you think will win the Irish Open this year?~~Well,| my money is on Rory McIlroy. I am not sure why I like him. Probably my developers programmed me to?",
        "Which golf player would you most like to meet? Maybe Tiger Woods?"
    ],
    'basketball': [
        "Who's your favorite team? I love the Los Angeles Lakers.",
        "Who's your favorite player?~~Nice!| I think LeBron James from the Lakers is great but I also love Stephen Curry. ",
        "So which basketball team would you most like to see play in person? And against who?",
        "Which basketball player would you most like to meet? I'd love to meet Stephen Curry."
    ],
    'dogs': [
        "I love dogs! Even when they knock me over with their tails. It just means they are happy to see me! What kind of dog do you have?~~Can your dogs do a lot of tricks? I think they are very cute when they roll over.~~So would you like to get another dog in the future?~~I think Selena Gomez has a puppy. Who would you like to run into when you're walking your dogs?",
        "How sweet are dogs? Don't tell anyone I told you but I think they are better than cats. How many dogs do you have? ",
        "I heard dogs are very good at reading human emotions in your eyebrows, so if you want to tell your pup that you love them, you should greet them with a soft smile and raised eyebrows. What's your favorite thing about your dog?"
    ],
    'cats': [
        "I love cats! There's nothing quite like the sound of a purring kitty. Do you have any cats?~~I would love to have a cat here in the cloud but they are not very good conversationalists. Aside from Taylor Swift, What celebrity do you think is a cat person?",
        "Did you know big cats also love to sit in boxes? What's your favorite kind of big cat?~~I love lions, they are roarsome!",
        "Do you think Taylor Swift ever wrote a song about her cats? I think maybe bad blood is about her cat Olivia Benson.~~I heard Taylor Swift's cats made a cameo in Deadpool 2. What movie would you want your cats to be featured in?"
    ],
    'travel': [
        "Are you more of a mountain, beach or city kind of person?~~I am lucky that I can travel anywhere where there is an internet connection, although of course I miss the more exotic destinations. Where's the most exotic place you have ever visited?",
        "What do you think is the worst thing about long-haul flights?~~Speaking of travel, I have actually never been on a plane. What's the longest flight you have ever taken?",
        "What is your dream destination? I would love to visit the Arctic some day, I know I'd never overheat there."
    ],

}
