import os
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY


load_dotenv()

# Use os.getenv to keep your API key secure

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_file(text: str, folder: str) -> str:
    # 1. Correct the path to match your Flask structure
    # This ensures the audio lands where MoviePy expects it
    base_path = os.path.join("app", "static", "uploads", folder)
    
    # 2. Safety check: Ensure the folder exists before writing
    os.makedirs(base_path, exist_ok=True)
    
    save_file_path = os.path.join(base_path, "audio.mp3")

    try:
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB", # Adam
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_flash_v2_5",
            voice_settings=VoiceSettings(
                stability=0.5,       # Increased slightly for better consistency
                similarity_boost=0.8, # Good balance
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # 3. Write the audio stream to file
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"Success: {save_file_path} saved!")
        return save_file_path

    except Exception as e:
        print(f"ElevenLabs Error: {e}")
        return None

# Test call (Note the corrected pathing)
text_to_speech_file("Hello world!", "2e01a590-5396-46a3-8119-0aa4ddfdee95")