import os
from google import genai
from dotenv import load_dotenv, find_dotenv
from google.genai import types

# --- SETUP: ENVIRONMENT VARIABLES ---
load_dotenv(find_dotenv())
key = os.getenv('GOOGLE_API_KEY')
print(key)

# --- AI FUNCTIONS ---
def generate_ai_text(prompt):
    if not key:
        raise ValueError("GOOGLE_API_KEY is missing in the .env file.")
        
    with genai.Client(api_key=key) as client:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3, 
                max_output_tokens=700,
                system_instruction=(
                    "You are a careful pension assistance guide. "
                    "Use simple language. Never claim to access a bank "
                    "or government portal. Never invent official rules. "
                    "Do not request OTPs, passwords, Aadhaar numbers, "
                    "or full bank credentials."
                )
            )
        )
        
    if not response.text:
        raise RuntimeError("Gemini returned no text. Please try again.")
        
    return response.text

def explain_rejection(pensioner_name, rejection_reason):
    prompt = f"""
Explain this demo Life Certificate rejection in simple English.
Pensioner name: {pensioner_name}
Rejection reason: {rejection_reason}

Include:
1. Why the submission failed.
2. What the mismatch means.
3. What the pensioner should check.
4. How to make a corrected resubmission.
5. When to contact the bank or pension authority.

This is only a software demonstration. Do not guarantee approval.
Do not ask for confidential information.
"""
    return generate_ai_text(prompt)

def generate_pension_guidance(question):
    prompt = f"""
A pensioner asks the following general question:
{question}

Answer in plain, respectful language. If the answer depends on 
official rules, a bank account, PPO status or a government portal, 
tell the person to confirm with their bank or pension authority. 
Do not invent a rule or claim to have checked their records.
"""
    return generate_ai_text(prompt)

# --- NOTIFICATION FUNCTIONS ---
def generate_whatsapp_message(name, certificate_id, reason):
    return f"""
Dear {name},

Your Life Certificate submission was REJECTED
in the demonstration application.

Certificate ID: {certificate_id}
Reason: {reason}

Please check your registered PPO and bank details,
then make a corrected submission. Contact your bank
or pension authority if you need official assistance.

Pension Assistance Demo
"""

def generate_success_message(name, certificate_id):
    return f"""
Dear {name},

Your submission passed the local demo checks.

Certificate ID: {certificate_id}

This is NOT official bank or government approval.
Please follow the official pension authority process.

Pension Assistance Demo
"""