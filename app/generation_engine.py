import os
import time
import subprocess
from text_to_audio import text_to_speech_file

# dynamically find the absolute path to this script's folder (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "static", "uploads")
REELS_DIR = os.path.join(BASE_DIR, "static", "reels")
DONE_FILE = os.path.join(BASE_DIR, "done.txt")

def text_to_audio(folder):
    print("TTA: " + folder)
    # Using the absolute path guaranteed to be correct
    file_path = os.path.join(UPLOADS_DIR, folder, "description.txt")
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            print(f"Processing text: {text} for folder: {folder}")
            
            # This calls your ElevenLabs logic
            text_to_speech_file(text, folder)
    else:
        print(f"Error: {file_path} not found.")

def create_reel(folder):
    input_txt = os.path.join(UPLOADS_DIR, folder, "input.txt")
    audio_mp3 = os.path.join(UPLOADS_DIR, folder, "audio.mp3")
    output_mp4 = os.path.join(REELS_DIR, f"{folder}.mp4")

    # The Race Condition Guard: Wait for audio to exist
    attempts = 0
    while not os.path.exists(audio_mp3) and attempts < 10:
        print("Waiting for audio to finish saving...")
        time.sleep(2)
        attempts += 1
        
    if not os.path.exists(audio_mp3):
        print(f"FATAL: Audio file never arrived at {audio_mp3}. Skipping video.")
        return

    # FFmpeg command using the safe absolute paths
    command = f'''ffmpeg -f concat -safe 0 -i "{input_txt}" -i "{audio_mp3}" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p "{output_mp4}"'''
    subprocess.run(command, shell=True, check=True)
    
    print("CR (Complete) -", folder)

if __name__ == "__main__":
    # Ensure done.txt exists so we don't crash on the first run
    if not os.path.exists(DONE_FILE):
        open(DONE_FILE, "w").close()

    while True:
        print("Checking for new folders to process...")
        with open(DONE_FILE, "r") as f:
            done_folders = [line.strip() for line in f.readlines()] 
            
        folders = os.listdir(UPLOADS_DIR)
        
        for folder in folders:
            if folder not in done_folders:
                text_to_audio(folder)  
                create_reel(folder)  
                
                with open(DONE_FILE, "a") as f:
                    f.write(folder + "\n")  
                    
        print("Sleeping for 5 seconds...")            
        time.sleep(5)