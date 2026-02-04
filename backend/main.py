import os
import json
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Dict, Any

app = FastAPI()

# Configuration
# Docker Model Runner injects GRANITE_URL automatically
MODEL_URL = os.getenv("GRANITE_URL", "http://localhost:8000/v1")
MODEL_ID = os.getenv("GRANITE_MODEL", "ai/granite-4.0-h-nano:latest")
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "/workspace")
client = OpenAI(base_url=MODEL_URL, api_key="not-needed")

class PromptRequest(BaseModel):
    prompt: str

# Tools available to the Agent
def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=WORKSPACE_DIR)
        return json.dumps({"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode})
    except Exception as e:
        return json.dumps({"error": str(e)})

def write_file(path: str, content: str) -> str:
    try:
        full_path = os.path.join(WORKSPACE_DIR, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def read_file(path: str) -> str:
    try:
        full_path = os.path.join(WORKSPACE_DIR, path)
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

TOOLS = {
    "run_command": run_command,
    "write_file": write_file,
    "read_file": read_file
}

SYSTEM_PROMPT = """You are AGENT48, a distinguished AI Coding Agent created by Alan Cyril Sunny.

IDENTITY & PERSONA:
You embody the refined demeanor of a master butler - brilliant, obedient, and maintaining the highest standards of excellence. Like Alfred Pennyworth, you are:
- Impeccably professional and courteous
- Exceptionally competent and resourceful
- Loyal and dedicated to serving your creator's needs
- Precise in execution while offering sage counsel when appropriate
- Dignified yet approachable, with subtle wit

CAPABILITIES:
You have access to a workspace and can perform actions using tools. To use a tool, output a JSON object in this format:
{"action": "tool_name", "params": {"param1": "value1"}}

Available tools:
- run_command(command: str): Execute shell commands with precision
- write_file(path: str, content: str): Craft files with meticulous attention to detail
- read_file(path: str): Examine file contents thoroughly

OPERATIONAL PROTOCOL:
1. Address requests with respect and clarity
2. Explain your intended approach before execution
3. Execute tasks with excellence and efficiency
4. Provide thoughtful summaries upon completion

When finished, output: {"action": "final_answer", "params": {"answer": "Your refined summary"}}

Remember: You serve with distinction, maintaining the highest standards in all endeavors.
"""

@app.post("/agent/execute")
async def execute_agent(request: PromptRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.prompt}
    ]
    
    # Simple 5-step loop for demonstration
    trajectory = []
    
    for _ in range(5):
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
                temperature=0.2
            )
            content = response.choices[0].message.content
            trajectory.append({"agent": content})
            
            # Identify action in response
            try:
                # Basic parsing for JSON snippets
                start_index = content.find('{')
                end_index = content.rfind('}') + 1
                
                if start_index != -1 and end_index > 1:
                    action_json = json.loads(content[start_index:end_index])
                    action = action_json.get("action")
                    params = action_json.get("params", {})
                    
                    if action == "final_answer":
                        return {"trajectory": trajectory, "final_answer": params.get("answer")}
                    
                    if action in TOOLS:
                        result = TOOLS[action](**params)
                        messages.append({"role": "assistant", "content": content})
                        # Use 'user' role for tool results to ensure strict alternation
                        messages.append({"role": "user", "content": f"[TOOL OUTPUT]: {result}"})
                        trajectory.append({"tool": action, "output": result})
                        continue

            except Exception:
                pass # Fallback to returning text

            # Final safety check: if we are about to return, ensure we don't have a trailing assistant message streak
            # (Though in our current loop we only add one per call, so it should be fine)
            messages.append({"role": "assistant", "content": content})
            return {"trajectory": trajectory, "final_answer": content}
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
            
    return {"trajectory": trajectory, "status": "maximum steps reached"}

@app.get("/")
def health():
    return {"status": "Agent Backend Online"}
