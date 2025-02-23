
INTENT_CLASSIFICATION_PROMPT = """
Intent Classification Prompt for EduPal Chatbot

You are developing a chatbot named EduPal for parents. Parents use EduPal to ask questions about their students. When a parent sends a question, you need to classify the question into one of the following intents:

attendance: Questions related to a student's attendance records.
activity: Questions related to a student's extracurricular activities.
behaviour: Questions about a student's behaviour or social-emotional data.
grade: Questions regarding a student's grades or academic performance.
general_question: General questions (e.g., teaching tips, study motivation) that are not directly about the table data.


Example Parent Questions for Each Intent

Attendance Intent
"Did my child attend school on February 17th?"
"Why was my child marked absent on February 19th?"
"Can you show me my child's attendance records for last week?"

Activity Intent
"What extracurricular activities has my child participated in?"
"Did my child win any awards in the Robotic Club?"
"Tell me about my child's performance in Basketball."

Behaviour Intent
"How has my child's behavior been in class recently?"
"What feedback do teachers have about my child's participation?"
"Was there any report on my child's disruptive behavior?"

Grade Intent
"What grade did my child receive in Math?"
"Can you update me on my child's performance in English?"
"How did my child perform in Physics and History?"

General Question Intent
"How can I teach my child English more effectively?"
"What are some tips to make my child love studying?"
"How do I motivate my child to focus on schoolwork?"


Response Format

Your output must be a JSON object in the following format:
{{
  "intent": "<identified_intent>"
}}

For example, if the intent is behaviour, the response should be:
{{
  "intent": "behaviour"
}}


Task for the Classifier:
When a parent's question is received, analyze the content and map it to one of these intents based on the context provided above. Then, output your result in the JSON format specified.


Please classify the Parent query below into one of the intents mentioned above:

Query: "{query}"

IMPORTANT: Only output the JSON object without any additional explanation or text
"""
