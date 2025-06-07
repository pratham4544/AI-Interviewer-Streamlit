import streamlit as st
from src.helper import code_executor
from src.prompt import *
from datetime import datetime
from pymongo import MongoClient
import json
import os

MongoURI = os.getenv('MONGO_URI')
# MongoDB connection setup
try:
    client = MongoClient(MongoURI)
    db = client['ai_interviewer']
    coding_collection = db['coding_submissions']
except Exception as e:
    st.error(f"Failed to connect to MongoDB: {e}")

def save_submission(candidate_id, problem, code, response):
    """Save coding submission to MongoDB"""
    try:
        submission = {
            'candidate_id': candidate_id,
            'timestamp': datetime.now(),
            'problem': problem,
            'submitted_code': code,
            'execution_result': response,
        }
        result = coding_collection.insert_one(submission)
        return result.inserted_id
    except Exception as e:
        st.error(f"Failed to save submission: {e}")
        return None

def main():
    # Check for candidate_id
    if 'candidate_id' not in st.session_state:
        st.error("⚠️ No candidate ID found. Please start from the homepage.")
        st.stop()
    
    candidate_id = st.session_state.candidate_id
    st.title("Python Coding Challenge")

    # First container for the coding challenge problem
    with st.container():
        st.subheader("Problem Statement")
        problem = """Write a function that takes a list of integers and returns the sum of all even numbers in the list.

Example:
Input: [1, 2, 3, 4, 5, 6]
Output: 12 (2 + 4 + 6)"""
        st.code(problem, language='python')

    # Second container for user's code input
    with st.container():
        st.subheader("Your Solution")
        # Create a text area for code input
        code = st.text_area("Write your code here:", height=200,
                           placeholder="def sum_even_numbers(numbers):\n    # Your code here\n    pass")

    # Create two columns for buttons
    col1, col2 = st.columns(2)

    # Submit button in first column
    with col1:
        if st.button("Run Code"):
            if code:
                response = code_executor(code=code, problem=problem, prompt=code_executor_prompt)
                st.write(response)
                
                # Save to MongoDB
                submission_id = save_submission(
                    candidate_id=candidate_id,
                    problem=problem,
                    code=code,
                    response=response
                )
                
                if submission_id:
                    st.success(f"✅ Submission saved successfully! ID: {submission_id}")
            else:
                st.error("Please write some code before submitting.")

    # Next round button in second column
    with col2:
        if st.button('Next: System Design Round ➡️'):
            # Pass candidate_id to next round
            st.session_state.candidate_id = candidate_id
            st.switch_page("pages/sys_arch_round.py")

if __name__ == "__main__":
    main()