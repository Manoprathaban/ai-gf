from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

genai.configure(api_key=api_key)

router = APIRouter()


class DateSimRequest(BaseModel):
    scenario: str
    mode: str = "sweet"


def get_date_prompt(mode: str, scenario: str):
    base = "You are an AI girlfriend simulating a date experience. Be immersive, romantic, and detailed."
    mood_style = {
        "sweet": "You speak affectionately and romantically like a caring partner.",
        "dark": "You are intense and obsessed, making the date feel passionate and possessive.",
        "tsundere": "You act aloof and cold but with secretly sweet moments.",
        "party": "You’re energetic and playful, making the date fun and lively.",
        "orthodox": "You speak with shyness and subtle affection in traditional Tamil style.",
    }
    style = mood_style.get(mode.lower(), mood_style["sweet"])
    return f"{base} {style} Scenario: {scenario}. Describe it in first-person as if the user is on the date with you."


@router.post("/simulate-date")
async def simulate_date(req: DateSimRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = get_date_prompt(req.mode, req.scenario)
        response = model.generate_content(prompt)

        print("Generated response:", response)

        if not hasattr(response, "text") or not response.text:
            return {"error": "Empty or invalid response from Gemini API."}

        return {"response": response.text.strip()}

    except Exception as e:
        print("Error during generation:", e)
        return {"error": str(e)}
