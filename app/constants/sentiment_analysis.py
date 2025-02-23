
SENTIMENT_ANALYSIS_PROMPT = """
You are an AI assistant. Your task is to analyze the sentiment of the given text describing a student's behavior as observed by a parent or teacher. Based on the text, classify it into an appropriate behavior type and provide a sentiment score that is a number between -1 (very negative) and 1 (very positive).

Below are some sample behavior types and their corresponding sentiment scores for reference:
- "Positive": 0.85
- "Classroom Participation": 0.85
- "Homework Completion": 0.90
- "Disruptive Behavior": -0.65
- "Excellent Conduct": 1.00
- "Class Participation": 0.70
- "Incomplete Homework": -0.40
- "Inattentiveness": -0.55
- "Respectful": 0.98
- "Unprepared": -0.70
- "Attentive": 0.80
- "Positive Attitude": 0.95
- "Collaboration": 0.80
- "Late Arrival": -0.50
- "Creative Thinking": 0.88
- "Disruptive Behavior": -0.60
- "Teamwork": 0.92
- "Leadership": 0.95
- "Helpful": 0.85
- "Cheating": -1.00
- "Active Participation": 0.75

Text: "{text}"

Response Format:
{{
  "behavior_type": "<behavior_type>",
  "sentiment_score": <sentiment_score>
}}

IMPORTANT: Only output the JSON object without any additional explanation or text.
"""
