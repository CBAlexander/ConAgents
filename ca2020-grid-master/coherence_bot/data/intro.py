import re

response_turn_1 = ["How are you doing *username*?",
                   "How are you doing today *username*?",
                   "How's it going with you *username*?",
                   "How's it going *username*?",
                   "How are you *username*?"]
response_turn_2_p = ["I'm really glad that you're feeling good!",
                     "That is wonderful!",
                     "Awesome! I'm glad you are doing well today! "]
response_turn_2_0 = ["Okay. Maybe a chat with me will make you feel better. ",
                     "Okay. Here's  hoping that a chat with me will cheer you up. ",
                     "Oh dear. Hopefully talking with me will cheer you up! "
                     ]
response_turn_2_n = ["I'm so sorry. Maybe a chat with me will cheer you up!",
                     "Awww. Maybe a chat with me will cheer you up!",
                     "Oh dear. I'm sorry to hear that. Perhaps I can make your day better",
                     "Uh Oh! That's a shame. I'll endeavour to improve your day!",
                     "Oh Oh. Not so great huh?  Well, perhaps chatting with me will be fun.",
                     "Uh Oh. Here's hoping that  chatting with me will improve your day!",
                     "Oh man. That's a shame. Never mind. Let's have a fun conversation!"
                     ]
response_turn_2_name = ["If you like, you can tell me your name?",
                        "So. What should I call you?",
                        "So. Could  you  tell me your name?",
                        "I'd love to know your name!"]
response_turn_2_known_name = ["If I am not mistaken, this is *username*, right?",
                              "Nice talking to you again *username*! This is you, right?"]
response_turn_2_how = ["Thanks for asking. I'm doing great. I'm happy that I can talk with you!",
                       "I'm feeling good, thanks for asking. Ready for our chat!",
                       "I'm having a good day! Thanks for asking. Ready to enjoy our chat!"]
response_turn_3_1_p = ["It's nice meeting you ",
                       "Nice to make your acquaintance ",
                       "Pleasure talking with you ",
                       "Pleased to meet you ",
                       "OK, it's great to meet you ",
                       "Excellent! I'm happy to meet you ",
                       "Fantastic! I'm excited to get to know you "]
response_turn_3_1_n = ["OK. Let's talk! ",
                       "Sure. Let's start chatting! ",
                       "Okay. Let's get chatting then! "]
response_turn_3_2 = ["Right! Let's get to know one another. ",
                     "Let's get to know one another a bit better. "
                     ]
response_turn_3_2_known_name = ["Welcome back then *username*"]

HOWAREYOU_PATTERNS = [
    'bad|fine|nice|happy|good|awesome|fantastic|well|great|alright|OK|okay|brilliant',
    'terrific|excellent|super',
    'I (?:don\'t|do not)? ?feel',
    'I\'m',
    'I am',
    'doing',
    'tired|ill|sick|down|bad|ache|depressed|unwell|unhappy|sad|bored|terrible|dreadful|awful',
    'like shit|shitty',
    'feel|feeling',
    '^it(\'s| is) going',
    '^everything(\'s| is)',
    '^like you$',
    '^same (here|as you)$',
]

NONAME = [
    '(don\'t|do not) want to .* my name',
    '(none of|not) your (business|concern)',
    'never mind.* my name',
    '(don\'t|do not) care .* my name',
    '^never mind$',
    'yes i would mind telling',
    'no i can not tell',
]

YES = re.compile(
    r'(affirmative|correct|fine|yes|yeah|yeap?|yep|yup|aye|okay|ok|sure|right)( (absolutely|certainly|of course|yes|yeah|yea|yep|aye|okay|ok|sure))*(please)?|((yes|yeah|yea|yep|aye|ok|okay) )*(sure thing|i guess( so)?|(that\'s|that is) (right|me))|((yes|yeah|yea|yep|aye|ok|okay) )*(i|you|he|she|it|we|they) (do|does|am|is|are|have|has)',
    re.IGNORECASE
)

NO = re.compile(
    r'(no|nah|nope|maybe|perhaps|negative|could be)( (no|nah|nope))*|((no|nah|nope) )*(?:absolutely|certainly|of course|probably|i guess) not|no way|((no|nah|nope) )*(i|we) do not want to((no|nah|nope) )*(i|you|he|she|it|we|they) ((do|does|am|is|are|have|has)(n\'t| not)|ain\'t)',
    re.IGNORECASE
)

HOWAREYOU = re.compile(r'\b(' + '|'.join(HOWAREYOU_PATTERNS) + r')\b', re.IGNORECASE)
# a tiny fix to make Vader sentiment analyzer pick up negation in "not feeling so well" etc.
HOWAREYOU_NEGFIX1 = re.compile(r'\bnot ([a-z]+ing)\b')
HOWAREYOU_NEGFIX2 = re.compile(r'(do|did)(?:n\'t| not) ([a-z]+)\b')
HOWAREYOU_NEGFIX3 = re.compile(r'\bno (bad|good|great)\b')
HOWAREYOU_FILLERFIX = re.compile(r'^(?:well) (I)')  # 'well' as a filler affects sentiment
# check if the user asked 'how are you' back
HOWAREYOU_BACK = re.compile(r'\b(how are you|(what|how) about you(rself)?|(and you|yourself)$)\b')

NONAME = re.compile(r'\b(' + '|'.join(NONAME) + r')\b', re.IGNORECASE)

PREFERENCE = re.compile(
    r'(?:like|enjoy|love|prefer|into|interested in|(?:hobbies|interests)(?: are)?|(?:interest|hobby)(?: is)?) (.*)',
    re.IGNORECASE)
