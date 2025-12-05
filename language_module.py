# language_module.py
import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are a control AI for a robotic arm. 
You receive human instructions and a brief vision context.
Your job: return the servo commands required to execute the task.

Example format:
[
  {"servo": 14, "angle": 150},
  {"servo": 15, "angle": 135}
]

Each servo corresponds to:
0: shoulder
2: arm
6: wrist
9: rotate joint
14: gripper
15: base rotation

Only output valid JSON — no explanations.
"""

def interpret_command(command_text, vision_context=""):
    """
    Sends the user's instruction and vision data to OpenAI and gets servo actions.
    """
    user_prompt = f"Vision context: {vision_context}\nUser command: {command_text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4o" if you have access
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    try:
        raw_output = response.choices[0].message.content.strip()
        actions = json.loads(raw_output)
        return actions
    except Exception as e:
        print("⚠️ Failed to parse model response:", e)
        print("Raw output:", response.choices[0].message.content)
        return []
