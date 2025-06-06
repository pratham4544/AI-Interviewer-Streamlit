import streamlit as st
from src.helper import code_executor
from src.prompt import *

def main():
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

    # Submit button
    if st.button("Run Code"):
        if code:
           response = code_executor(code=code, problem=problem,prompt=code_executor_prompt)
           st.write(response)
           
           if st.button('Submit Code'):
               st.write('See You In Next Round')
        else:
            st.error("Please write some code before submitting.")

if __name__ == "__main__":
    main()