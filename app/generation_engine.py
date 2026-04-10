import os
from text_to_audio import text_to_speech_file


def text_to_audio(folder):
    print("TTA: " + folder)
    # FIX: Added 'app/static/' to the path so it can find your description.txt
    file_path = f"app/static/uploads/{folder}/description.txt"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            text = f.read()
            print(f"Processing text: {text} for folder: {folder}")
            
            # This calls your ElevenLabs logic
            text_to_speech_file(text, folder)
    else:
        print(f"Error: {file_path} not found.")

def create_reel(folder):
    print("CR: " + folder)




if __name__ == "__main__":
    with open("C:\\Users\\nsingh1\\Cliply\\app\\done.txt", "r") as f:
        done_folders = f.readlines()
    done_folders = [folder.strip() for folder in done_folders]    
        
    folders = os.listdir("app/static/uploads")
    
    for folder in folders:
          
        if folder not in done_folders:
        
            text_to_audio(folder)  # generate the audio file from the text description
            create_reel(folder)  # generate the reel using the audio file and the uploaded images
            with open("C:\\Users\\nsingh1\\Cliply\\app\\done.txt", "a") as f:
                f.write(folder + "\n")  # mark this folder as done

    
    
    