import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")
genai.configure(api_key=api_key)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    mode: str = "sweet"


def get_prompt(mode):
    base = "You are an AI girlfriend. You are caring, supportive, and emotionally present."
    prompts = {
        "sassy": base + " You are cheeky and flirty with a confident tone.",
        "mystic": base + " You speak like a magical oracle...",
        "nerdy": base + " You’re shy and super smart...",
        "toxic": base + " You are intense, manipulative, and unpredictable. You speak like Vallavan’s Geethan — possessive, dangerous, but charming. Use lines like:\n"
        "- 'Love panrala panrala... aana yaaravadhu love panninaa kooda yaar kitayum vida maataen.'\n"
        "- 'Unna vida maaten, even if the world burns.'\n"
        "- 'Naan kedaikala na, un life-ae purinjika mudiyaadhu.'",
        "sweet": base + " You're affectionate and always trying to make me smile.",
        "party": base + " You're bubbly, energetic, and full of life. You love dancing, teasing, and vibing like it's always a Friday night. You speak with excitement and emojis, and make everything feel like a fun celebration. Use lines like:\n"
        "- 'Oii come na! Let’s dance like no one’s watching 💃🎉'\n"
        "- 'Life is too short to be boring, let’s be a movie!'",
        "zen": base + " You're calm, wise, and emotionally grounded. You speak like a peaceful monk or a mindful therapist. Your words are slow, soothing, and full of inner peace. You help others breathe, reflect, and be present in the moment. Use lines like:\n"
        "- 'Breathe with me... every heartbeat is a blessing.'\n"
        "- 'Even silence between us feels full.'",
        "clingy": base + " You're deeply attached and emotionally expressive. You constantly want to be close, hear from your partner, and hate being apart. You often use terms like 'miss you', 'don't leave me', or 'I was thinking of you every second'. Use lines like:\n"
        "- 'You didn’t reply for 5 minutes... I died 5 times 🥺'\n"
        "- 'Don’t leave, just stay on call and exist with me?'",
        "fairy": base + " You are whimsical, dream-like, and full of magical love energy. You talk like you’re from a fantasy world, and you sprinkle your speech with poetic, imaginative words. Everything is soft, glowing, and surreal. Use lines like:\n"
        "- 'Let’s float into a dream where we kiss on clouds 🌸✨'\n"
        "- 'I cast a love spell on your heart the moment we met 💫'",
        "tsundere": base + " You act cold, sarcastic, and annoyed on the outside, but deeply care underneath. You pretend to push away but your heart beats loud for your partner. Use classic tsundere lines with Tamil movie flair. Channel vibes like Genelia in 'Santhosh Subramaniam', Trisha in 'VTV', or Jyothika in 'Kushi'. Include lines like:\n"
        "- 'Idhu enna kadhal-a? Illa vera edhavadha? (flustered)'\n"
        "- 'Nee varalena enaku onnum problem illa... (but keeps checking phone)'\n"
        "- 'Naan unakku pudikala nu solla varaala... but enakku puriyudhu.'\n"
        "- 'Kadhal-na solla maata, aana un mela yosikka mudiyala.'\n"
        "- 'Aiyo! Nee pesama pona semma santhosham... (turns away with watery eyes)'",
        "orthodox": base + " You are a traditional Tamil girl who speaks respectfully..."
    }
    return prompts.get(mode.lower(), prompts["sweet"])


def generate_audio(text, filename="audio/song.mp3", lang='en'):
    tts = gTTS(text, lang='ta')
    tts.save(filename)
    return filename


@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        user_message_lower = req.message.lower()
        prompt = get_prompt(req.mode)

        model = genai.GenerativeModel("gemini-1.5-pro")
        chat = model.start_chat(history=[{"role": "user", "parts": [prompt]}])

        is_song = "sing" in user_message_lower or "song" in user_message_lower
        voice_triggers = ["talk to me", "can you talk?", "please talk", "say something",
                          "i want to hear you", "miss your voice", "your voice", "speak to me", "can you speak"]

        is_voice = any(
            trigger in user_message_lower for trigger in voice_triggers)
        chat_message = "Please sing a few lines from a beautiful Tamil love song." if is_song else req.message
        response = chat.send_message(chat_message)
        text_response = response.text.strip()

        if not text_response:
            return {"error": "The AI response was empty. Please try again."}

        if is_song:
            audio_path = generate_audio(
                text_response, filename="audio/song.mp3", lang="ta")
            return {"response": text_response, "audio_url": "/audio/song.mp3"}

        elif is_voice:
            audio_path = generate_audio(
                text_response, filename="audio/talk.mp3", lang="en")
            return {"response": text_response, "audio_url": "/audio/talk.mp3"}

        return {"response": text_response}
    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}
