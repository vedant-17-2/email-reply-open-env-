# email-reply-open-env-
This project implements an OpenEnv environment where an AI agent generates professional email replies for real-world scenarios.

## Tasks

The environment includes 3 tasks with increasing difficulty:

- Easy: Reply to a welcome email politely  
- Medium: Handle a customer complaint professionally  
- Hard: Respond to refund + escalation with full ownership  

## Grading Logic

Responses are evaluated based on:

- Relevance (keyword matching)
- Tone (professional language like apology, gratitude)
- Completeness (response length)

Scores range from 0.0 to 1.0.

## How to Test

Base URL:  
https://vedant-172-email-reply-env.hf.space

### Get Tasks
/tasks

### Run Baseline
/baseline

### Test Grader
/grader?task_id=task_1_easy&reply=Thank%20you%20for%20the%20warm%20welcome%20I%20really%20appreciate%20it

- You can replace the task_id with task_2_medium or task_3_hard to test other difficulty levels.

## Tech Stack

- FastAPI  
- OpenEnv  
- Hugging Face Spaces  

## Notes

- Implements OpenEnv API (reset, step, state)
- Includes baseline agent and grading system
