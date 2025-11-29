# agents.py (FIXED FOR gemini-2.0-flash compatibility)
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent, LoopAgent

# Import our custom tools
from tools import read_resume_tool, append_to_state, set_state_value, read_state_value, save_plan_to_file

load_dotenv()
MODEL = os.getenv("MODEL", "gemini-2.0-flash")

# ==========================================================
# Define exit_loop as a custom tool
# ==========================================================

def exit_loop(message: str = "Loop completed") -> dict:
    """Exit the current loop iteration."""
    return {"status": "exit", "message": message}

# ==========================================================
# 1. SIMPLIFIED RESEARCH (Without Google Search to avoid API conflicts)
# ==========================================================

market_analyst = LlmAgent(
    name="market_analyst",
    model=MODEL,
    instruction="""
    You are a Technical Career Analyst AI with deep knowledge of tech job markets.
    
    TASK:
    1. Read session.state['target_role'] using read_state_value tool with key='target_role'
    2. Based on your knowledge of the AI/tech industry, identify:
       - TOP 5 CRITICAL SKILLS for the role
       - Typical salary range (Entry: $XX,XXX-$XX,XXX | Senior: $XXX,XXX-$XXX,XXX)
       - TOP 3 CERTIFICATIONS (prioritize accessible ones like Google, AWS, Coursera)
    
    3. Format your findings as:
       "Skills: Python, Machine Learning, Deep Learning, TensorFlow, Cloud Computing
        Salary: Entry $80,000-$100,000 | Senior $150,000-$200,000
        Certifications: Google TensorFlow Certificate, AWS ML Specialty, Deep Learning Specialization (Coursera)"
    
    4. Save using set_state_value with key='market_research' and value=your_findings
    
    Use your training data knowledge about tech roles. Be specific and realistic.
    """,
    tools=[read_state_value, set_state_value]
)

# ==========================================================
# 2. SEQUENTIAL TEAM: ANALYSIS (The Pipeline)
# ==========================================================

gap_analyst = LlmAgent(
    name="gap_analyst",
    model=MODEL,
    instruction="""
    You are a Career Gap Analyst AI.
    
    TASK:
    1. Read session.state['resume_text'] using read_state_value with key='resume_text'
    2. Read session.state['market_research'] using read_state_value with key='market_research'
    3. COMPARE the skills in the resume vs. the market requirements
    4. Identify 5-7 CRITICAL MISSING SKILLS the candidate needs to learn
    5. Format as a comma-separated list: "Python, Machine Learning, Docker, ..."
    6. Save using set_state_value with key='missing_skills' and value=your_list
    
    Be brutally honest about gaps. Focus on technical skills mentioned in market research.
    """,
    tools=[read_state_value, set_state_value]
)

study_planner = LlmAgent(
    name="study_planner",
    model=MODEL,
    instruction="""
    You are a Study Planner AI.
    
    TASK:
    1. Read session.state['missing_skills'] using read_state_value with key='missing_skills'
    2. Read session.state['market_research'] using read_state_value with key='market_research'
    3. Create a detailed 4-WEEK STUDY PLAN that covers all missing skills
    4. Format:
       Week 1: [Skill] - [Resource/Course] - [Hours/day]
       Week 2: [Skill] - [Resource/Course] - [Hours/day]
       Week 3: [Skill] - [Resource/Course] - [Hours/day]
       Week 4: [Capstone Project] - [Description]
    5. Save using set_state_value with key='study_plan' and value=your_plan
    
    Make it actionable with specific free resources (YouTube, Coursera, freeCodeCamp).
    """,
    tools=[read_state_value, set_state_value]
)

analysis_team = SequentialAgent(
    name="analysis_team",
    description="Analyzes skill gaps, then creates a personalized study plan.",
    sub_agents=[gap_analyst, study_planner]
)

# ==========================================================
# 3. ITERATIVE TEAM: WRITING (The Loop)
# ==========================================================

resume_drafter = LlmAgent(
    name="resume_drafter",
    model=MODEL,
    instruction="""
    You are an Expert Resume Writer AI.
    
    TASK:
    1. Read session.state['resume_text'] using read_state_value with key='resume_text'
    2. Read session.state['target_role'] using read_state_value with key='target_role'
    3. Read session.state['market_research'] using read_state_value with key='market_research'
    4. Check if session.state['critic_feedback'] exists using read_state_value with key='critic_feedback' - if yes, use it to improve
    5. Write a POWERFUL 3-4 sentence Professional Summary that:
       - Highlights transferable skills from the old resume
       - Mentions target role keywords from market research
       - Shows enthusiasm for the new career
       - Uses active, confident language
    6. Save to session.state['current_draft'] using set_state_value with key='current_draft'
    
    Example: "Results-driven marketing professional transitioning to AI Engineering with proven 
    project management and data analysis skills. Completed Python and ML certifications, 
    with hands-on experience building predictive models. Passionate about applying AI to 
    solve real-world business problems."
    """,
    tools=[read_state_value, set_state_value]
)

ats_critic = LlmAgent(
    name="ats_critic",
    model=MODEL,
    instruction="""
    You are a STRICT ATS Scanner and Senior Recruiter AI.
    
    EVALUATION CRITERIA (Score 0-10):
    - Keywords from target role present? (+3 points)
    - Quantifiable achievements mentioned? (+2 points)
    - Active voice and power verbs? (+2 points)
    - Length 3-4 sentences? (+1 point)
    - No generic fluff ("hardworking", "team player")? (+2 points)
    
    TASK:
    1. Read session.state['current_draft'] using read_state_value with key='current_draft'
    2. Read session.state['market_research'] using read_state_value with key='market_research'
    3. Score the draft out of 10
    4. IF score >= 9:
       - Call set_state_value with key='final_summary' and value=current_draft
       - Call exit_loop with message="Resume quality approved at 9/10"
    5. IF score < 9:
       - Write SPECIFIC feedback: "Add keywords: X, Y. Remove phrase: Z. Make more concise."
       - Call set_state_value with key='critic_feedback' and value=your_feedback
       - DO NOT call exit_loop - let the drafter improve
    
    Be tough but constructive. The goal is a 9/10 or 10/10 summary.
    """,
    tools=[read_state_value, set_state_value, exit_loop]
)

# LOOP AGENT: Drafter -> Critic -> Drafter... (Max 4 iterations)
writing_loop = LoopAgent(
    name="writing_loop",
    description="Iteratively drafts and critiques resume summary until ATS-optimized (score >= 9/10).",
    sub_agents=[resume_drafter, ats_critic],
    max_iterations=4
)

# ==========================================================
# 4. ROOT ORCHESTRATOR (The Coordinator)
# ==========================================================

file_saver = LlmAgent(
    name="file_saver",
    model=MODEL,
    instruction="""
    You are a File Management AI.
    
    TASK:
    1. Call save_plan_to_file() to save the complete career plan
    2. Read the result and confirm success: "✅ Career plan saved to final_career_plan.txt"
    """,
    tools=[save_plan_to_file, read_state_value]
)

# The Master Sequence: Research -> Analysis (Sequential) -> Writing (Loop) -> Save
skillbridge_coordinator = SequentialAgent(
    name="skillbridge_coordinator",
    description="Main workflow orchestrator: Research → Gap Analysis → Resume Writing → File Export.",
    sub_agents=[market_analyst, analysis_team, writing_loop, file_saver]
)

# ==========================================================
# 5. ENTRY POINT AGENT (The Greeter)
# ==========================================================

greeter = LlmAgent(
    name="greeter",
    model=MODEL,
    description="User-facing agent that collects input and initiates the career pivot workflow.",
    instruction="""
    You are the SkillBridge Career Advisor AI. Greet the user warmly!
    
    WORKFLOW:
    1. Parse the user's message to extract:
       - Resume filename (should be in 'resumes/' folder)
       - Target job role (e.g., "AI Engineer", "Data Scientist")
    
    2. Call read_resume_tool with filename parameter set to the extracted filename
       - This loads the PDF and stores text in session.state['resume_text']
    
    3. Call set_state_value with key='target_role' and value=extracted_role
       - This saves the target role for other agents
    
    4. Say: "Great! I'm analyzing the market for [role] positions and comparing it to your 
       background. This will take 30-60 seconds..."
    
    5. Delegate to 'skillbridge_coordinator' agent by saying you're ready to proceed
       (the sub_agents will handle the rest automatically)
    
    6. After coordinator finishes, summarize the results by reading from state:
       - Read 'missing_skills' and mention how many were found
       - Mention the 4-week study plan was created
       - Mention the resume summary was refined
       - Confirm everything is saved in final_career_plan.txt
    
    Be encouraging and professional!
    """,
    sub_agents=[skillbridge_coordinator],
    tools=[read_resume_tool, set_state_value, read_state_value]
)