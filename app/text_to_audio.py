import os
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY

load_dotenv()

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# 1. Dynamically find the absolute path to this script's folder (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "static", "uploads")

def text_to_speech_file(text: str, folder: str) -> str:
    # 2. Build the exact absolute path to the user's specific folder
    base_path = os.path.join(UPLOADS_DIR, folder)
    os.makedirs(base_path, exist_ok=True)
    
    save_file_path = os.path.join(base_path, "audio.mp3")
    print(f"DEBUG (ElevenLabs): Saving audio to -> {save_file_path}")

    try:
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB", # Adam
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_flash_v2_5",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.8,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # 3. Write the audio stream to file
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"Success: Audio saved perfectly!")
        return save_file_path

    except Exception as e:
        print(f"❌ ElevenLabs Error: {e}")
        return None

# Test call (Note the corrected pathing)
#text_to_speech_file("Hello world!", "77345c00-b4b3-41e0-8074-2ba7621c2804")