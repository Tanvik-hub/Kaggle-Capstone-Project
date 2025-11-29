# tools.py
import os
from pypdf import PdfReader
from google.adk.tools import ToolContext
from typing import Dict

def append_to_state(tool_context: ToolContext, key: str, value) -> Dict[str, str]:
    """Append `value` to list stored at session.state[key]."""
    lst = tool_context.state.get(key, [])
    if isinstance(lst, list):
        lst.append(value)
    else:
        lst = [value]
    tool_context.state[key] = lst
    return {"status": "ok", "message": f"Appended to {key}"}

def set_state_value(tool_context: ToolContext, key: str, value: str) -> Dict[str, str]:
    """Overwrites or sets a single value in session.state[key]."""
    tool_context.state[key] = value
    return {"status": "ok", "message": f"Set {key}"}

def read_state_value(tool_context: ToolContext, key: str) -> Dict[str, str]:
    """Reads a value from state. Useful for agents to 'see' what others did."""
    val = tool_context.state.get(key, "Not found")
    return {"value": str(val)}

def read_resume_tool(tool_context: ToolContext, filename: str) -> Dict[str, str]:
    """Reads a PDF resume and saves text to state['resume_text'].
    
    Args:
        filename: Can be just filename (e.g., 'test_resume.pdf') or path (e.g., 'resumes/test_resume.pdf')
    """
    # Handle both cases: filename only OR full path
    if filename.startswith("resumes/"):
        file_path = filename  # Already has resumes/ prefix
    else:
        file_path = os.path.join("resumes", filename)  # Add resumes/ prefix
    
    if not os.path.exists(file_path):
        return {
            "status": "error", 
            "message": f"File not found at: {file_path}"
        }
    
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        tool_context.state['resume_text'] = text
        return {
            "status": "ok", 
            "preview": text[:200] + "...",
            "total_chars": len(text)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def save_plan_to_file(tool_context: ToolContext, filename: str = "final_career_plan.txt") -> Dict[str, str]:
    """Saves the final study plan and resume summary to a text file."""
    plan = tool_context.state.get('study_plan', 'No Plan')
    summary = tool_context.state.get('final_summary', 'No Summary')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"--- CAREER PIVOT PLAN ---\n\n{plan}\n\n--- NEW SUMMARY ---\n{summary}")
    
    return {"status": "ok", "path": filename}