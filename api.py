import os
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from src.helper import (
    extract_candidate_info, 
    generate_questions, 
    store_interview_template,
    get_stored_interview_template,
    evaluate_answer,
    generate_follow_up_question,
    get_candidate_average_score
)

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['aieta']
candidates_collection = db['candidates']

# Initialize FastAPI app
app = FastAPI(title="Rupadi - AI Interviewer API")

# Define data models
class CandidateRequest(BaseModel):
    candidate_id: str

class AnswerRequest(BaseModel):
    candidate_id: str
    question: str
    answer: str

class FollowUpRequest(BaseModel):
    candidate_id: str
    original_question: str
    previous_answer: str

# API routes
@app.get("/")
def read_root():
    return {"message": "Rupadi AI Interviewer API", "status": "running"}

@app.get("/candidates")
def list_candidates():
    """List all available candidates"""
    try:
        candidates = []
        for candidate in candidates_collection.find({}, {'_id': 1, 'personal_information.first_name': 1}):
            candidates.append({
                "id": candidate['_id'],
                "name": candidate['personal_information'].get('first_name', 'Unknown')
            })
        return {"candidates": candidates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching candidates: {str(e)}")

@app.post("/prepare-interview")
def prepare_interview(request: CandidateRequest):
    """Extract candidate info and generate questions"""
    try:
        candidate_data = extract_candidate_info(request.candidate_id)
        if not candidate_data:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        response, questions, greeting_script = generate_questions(candidate_data)
        store_interview_template(candidate_data, greeting_script, questions)
        
        return {
            "candidate_id": request.candidate_id,
            "greeting": greeting_script,
            "questions": questions,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error preparing interview: {str(e)}")

@app.get("/interview/{candidate_id}")
def get_interview(candidate_id: str):
    """Get stored interview questions for a candidate"""
    try:
        greeting, questions = get_stored_interview_template(candidate_id)
        if not greeting or not questions:
            raise HTTPException(status_code=404, detail="Interview template not found")
        
        return {
            "candidate_id": candidate_id,
            "greeting": greeting,
            "questions": questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving interview: {str(e)}")

@app.post("/evaluate-answer")
def process_answer(request: AnswerRequest):
    """Evaluate a candidate's answer to a question"""
    try:
        evaluation = evaluate_answer(request.question, request.answer)
        response = {
            "evaluation": evaluation["evaluation"],
            "needs_follow_up": evaluation["evaluation"]["score"] < 6
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")

@app.post("/generate-follow-up")
def get_follow_up(request: FollowUpRequest):
    """Generate a follow-up question based on previous answer"""
    try:
        follow_up = generate_follow_up_question(
            request.original_question, 
            request.previous_answer
        )
        return {"follow_up_question": follow_up}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating follow-up: {str(e)}")

@app.get("/results/{candidate_id}")
def get_results(candidate_id: str):
    """Get the interview results for a candidate"""
    try:
        avg_score = get_candidate_average_score(candidate_id)
        return {
            "candidate_id": candidate_id,
            "average_score": avg_score["average_score"],
            "feedback": avg_score["feedback"],
            "interactions": avg_score["interactions"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving results: {str(e)}")
