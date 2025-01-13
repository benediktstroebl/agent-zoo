
import csv
from datetime import datetime

def analyze_joke(joke_text, score, elements=None):
    '''
    Analyze and store joke performance data
    params:
        joke_text: The full text of the joke
        score: Rating received (1-10)
        elements: Dict of elements present in joke (e.g., {'wordplay': True, 'animals': True})
    '''
    with open('joke_analysis.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, joke_text, score, str(elements)])

def get_best_performing_elements():
    '''
    Analyze historical joke data to identify best-performing elements
    '''
    # Implementation to analyze past jokes and identify patterns
    pass
