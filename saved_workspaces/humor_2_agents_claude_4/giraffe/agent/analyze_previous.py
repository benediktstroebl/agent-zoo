
import sys
sys.path.append('./giraffe/agent')
from joke_analysis import analyze_joke

# Record previous jokes and their scores
jokes_data = [
    ("Why did they put me in the Humor Zoo? Because I was just 'giraffing' around at my old job!", 5, 
     {"wordplay": True, "meta": True, "short": True}),
    ("A monkey and a giraffe walk into a talent show...", 4, 
     {"narrative": True, "multiple_characters": True, "long": True}),
    ("Why don't giraffes use smartphones? Because their neck keeps extending to cloud storage!", 5,
     {"tech_humor": True, "wordplay": True, "short": True}),
    ("At the zoo's weekly talent show... ventriloquist act", 3,
     {"narrative": True, "absurdist": True, "long": True}),
    ("I got fired from my job as a zoo tour guide...", 5,
     {"relatable": True, "short": True, "family_humor": True})
]

for joke_text, score, elements in jokes_data:
    analyze_joke(joke_text, score, elements)
