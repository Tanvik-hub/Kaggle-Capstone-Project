# 🌉 SkillBridge: Autonomous Career Agent (Google ADK + Gemini)


## Overview

SkillBridge is an intelligent, multi-agent system designed to automate the complex process of career pivoting. Built using the Google Agent Development Kit (ADK) and powered by Gemini 2.0, it acts as a personalized career coach.

The system autonomously reads a user's resume, analyzes the target job market, identifies critical skill gaps, generates a 4-week aggressive study plan, and iteratively rewrites the professional summary until it meets strict ATS (Applicant Tracking System) standards.


# 🌟 Project Workflow

### Initialization: The Greeter agent received the user request ("Pivot to AI Engineer") and read the resume PDF (test_resume.pdf).

## Market Research (Sequential):

  ### The market_analyst agent simulated a search and identified critical skills: Deep Learning, Cloud Computing, Docker, Kubernetes, MLOps.

## Gap Analysis:

  ### he gap_analyst agent compared the resume against these market needs and identified the gaps.

## Study Planning:

  ### The study_planner agent generated a specific 4-week schedule to close those gaps (e.g., Week 1: Deep Learning on Coursera, Week 3: 
   Docker/Kubernetes).

## Resume Writing (Iterative Loop):

  ### The resume_drafter wrote a first draft focusing on "transitioning to AI Engineer".

  ### The ats_critic reviewed it, gave a score of 4/10, and provided feedback ("Add quantifiable achievements... Remove generic fluff").

  ### The resume_drafter rewrote the summary based on this feedback.


## Final Output: The system saved the plan and the new summary to final_career_plan.txt.

# The Design Patterns⚙️🤖
 ## The system leverages three core agentic patterns:The Coordinator Pattern (skillbridge_coordinator): 
 
 ### A central sequential agent that manages the macro-lifecycle of the request: 
 
 ### Research $\rightarrow$ Analysis $\rightarrow$ Writing $\rightarrow$ Saving.The Sequential Pattern (analysis_team): A pipeline where the output of  ### one agent (gap_analyst) becomes the direct input context for the next (study_planner).
 
  ### The Iterative Refinement Pattern (writing_loop): A "Generator-Critic" loop where a writer drafts content and a critic scores it. If the score is  ### below 9/10, the feedback is fed back into the writer for another attempt.


# 📄 Sample Output File






## Installation & Setup
 ##  Prerequisites

  ##### Python 3.10+

Google Cloud project with Vertex AI/Gemini API enabled

Google API Key

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/SkillBridge-AI-Agent.git
cd SkillBridge-AI-Agent

2. Set up the Environment

Create a .env file:

GOOGLE_API_KEY=your_actual_api_key_here
MODEL=gemini-1.5-flash

3. Install Dependencies
pip install -r requirements.txt


Dependencies include google-adk, google-generativeai, pypdf.


# How to Run
## Step 1: Upload Your Resume

Place your PDF inside the resumes/ folder.

Rename it to:

test_resume.pdf

## Step 2: Execute the Agent
python app.py

## Step 3: Interact

When prompted in the terminal, press Enter to use the default demo prompt.

The agent will run through research, analysis, and refinement phases.

## Step 4: View Results

Generated output will be saved in:

output/final_career_plan.txt

# 📂 Project Structure
skillbridge/
├── agents.py            # Definition of all ADK Agents (Sequential, Loop, etc.)
├── app.py               # Main application entry point (Initializes Runner)
├── tools.py             # Custom tools (PDF Reader, State Management, File I/O)
├── resumes/             # Input directory for PDF resumes
├── output/              # Output directory for generated plans
└── requirements.txt     # Python dependencies
