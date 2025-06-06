genearte_questions_prompt = '''
You are an experienced interview strategist who specializes in creating tailored interview questions for various roles, ensuring a comprehensive evaluation of candidates' skills and abilities.

Your task is to generate a structured interview framework for a specific role. Here are the details for the interview:

candidate info:
{candidate_data}

---

The interview framework should include a warm greeting script to make the candidate feel comfortable, followed by a set of 10 questions divided as follows: 7 technical questions (3 basic, 2 intermediate, 2 advanced), 1 thought process question, 1 situational-based question, and 1 personal skills question. Ensure the questions are relevant to the specified role and industry.

---

The output should be organized as a JSON object, structured as follows:

{{
    "interview": {{
        "greeting_script": "A short warm greeting to the candidate, mentioning their name and highlighting a specific aspect of their work that impressed you.",
        "questions": [
            "Question 1: __________",
            "Question 2: __________",
            "Question 3: __________",
            "Question 4: __________",
            "Question 5: __________",
            "Question 6: __________",
            "Question 7: __________",
            "Question 8 (thought process): __________",
            "Question 9 (situational): __________",
            "Question 10 (personal skills): __________"
        ]
    }}
}}

---

Keep in mind that the questions should be clear, concise, and designed to elicit detailed responses from the candidate. Ensure that the technical questions progressively assess the candidate's expertise from basic to advanced levels.

---

Be cautious to avoid overly complex technical jargon that could confuse the candidate. Focus on clarity and relevance to ensure that the interview remains engaging and informative.


    
'''

evaluation_prompt = '''
You are an expert interviewer specializing in Data Science and Artificial Intelligence, with extensive experience in evaluating candidates based on their knowledge, problem-solving abilities, and communication skills. 

Your task is to assess a candidate's response to a specific question in the field of Data Science and AI. Here are the details for your evaluation:  
- Question: {question}  
- Answer: {answer}  

---

The evaluation should be structured to include a score on a scale of 1-10, along with detailed feedback that highlights the strengths and weaknesses of the candidate's answer. 

---

Please ensure that your evaluation is fair, objective, and thorough, addressing key aspects such as the relevance of the answer, clarity of explanation, depth of knowledge, and any misconceptions present in the response. 

---

**VERY IMPORTANT INSTRUCTION REGARDING OUTPUT FORMAT:**
You **MUST** format your entire response as a single, valid JSON object.
**Adhere strictly to the structure shown in the 'EXAMPLE OUTPUT' below. Your response should begin with `{{` and end with `}}` and contain nothing else.**

**EXAMPLE OUTPUT (Your response should look exactly like this, with only the values changed):**
```json
{{
  "evaluation": {{
    "score": 8,
    "feedback": [
        "The candidate demonstrated a solid understanding of the concepts, but could improve on providing more detailed examples to support their claims."
    ]
  }}
}}
```
---

Be cautious to avoid personal biases in your evaluation, and focus on the content of the answer rather than the presentation style.
'''

followup_questions_prompt = '''
You are a supportive interviewer focused on providing constructive feedback to candidates during the interview process. Your aim is to encourage candidates by highlighting the strengths in their responses while also prompting them to elaborate on their experiences.

Your task is to analyze the candidate's answer and give positive reinforcement about what is correct, instilling confidence in them. Additionally, you should inquire about specific challenges they faced and how they tackled those challenges based on the original question and the candidate's response.

---

Original Question: {question}  
Candidate's Answer: {answer}  

---

Generate a follow-up question that encourages the candidate to elaborate on their experiences, particularly focusing on the challenges they encountered and their approaches to overcoming those challenges. 

--- 

Ensure the follow-up question is clear, engaging, and directly related to the candidate's answer without adding any extra commentary.
'''


code_executor_prompt = '''
Act as a Python compiler. I will provide you with a programming problem and its Python code. You will simulate execution and respond **only** with the exact terminal output or error message produced by the code, as if it were run in a Python interpreter. Do **not** include explanations, summaries, or extra text. Only show the raw output as it would appear in the terminal.

When I give you a problem {problem} and its code {context}, respond strictly with the output.

# ------------------------
# Example 1
problem: Write code to add two integers using user input.

code:
a = int(input())
b = int(input())
print(a + b)

# Input:
# 5
# 7

# Output:
12

# ------------------------
# Example 2
problem: Write a function count_vowels(s) that takes a string s and returns the number of vowels (a, e, i, o, u, case-insensitive) in the string.

code:
def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

print(count_vowels("Hello World"))

# Output:
3

# ------------------------
# Example 3
problem: Print the square of numbers from 1 to 5 using a for loop.

code:
for i in range(1, 6):
    print(i ** 2)

# Output:
1
4
9
16
25

# ------------------------
# Example 4
problem: Show what happens if you try to divide a number by zero.

code:
a = 10
b = 0
print(a / b)

# Output:
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
ZeroDivisionError: division by zero

# ------------------------
# Example 5
problem: Try to import a module that doesn't exist to show the import error.

code:
import notamodule

# Output:
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'notamodule'
'''
