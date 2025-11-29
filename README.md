# 🌉 SkillBridge: Autonomous Career Agent (Google ADK + Gemini)


## Overview

SkillBridge is an intelligent, multi-agent system designed to automate the complex process of career pivoting. Built using the Google Agent Development Kit (ADK) and powered by Gemini 2.0, it acts as a personalized career coach.

The system autonomously reads a user's resume, analyzes the target job market, identifies critical skill gaps, generates a 4-week aggressive study plan, and iteratively rewrites the professional summary until it meets strict ATS (Applicant Tracking System) standards.

## Detailed Agent Roles

Greeter	LlmAgent :	Entry point. Parses user intent, reads the PDF using read_resume_tool, and initializes the workflow.
Market Analyst :	LlmAgent	Simulates a recruiter to identify top skills and salary ranges for the target role.
Analysis Team :	SequentialAgent	Contains Gap Analyst and Study Planner.
Writing Loop :	LoopAgent	Uses a drafter and critic to iteratively refine the resume summary.
File Saver :	LlmAgent	Manages the final output and persists files to disk.


## Installation & Setup
 ##  Prerequisites

     ##     Python 3.10+

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

