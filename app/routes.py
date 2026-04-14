import uuid
import os
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/create", methods=["GET", "POST"])
def create():
    # 1. Generate the unique session ID
    session_id = str(uuid.uuid4())
    
    if request.method == "POST":
        # Capture form data
        script_text = request.form.get('text')
        
        # 2. Define and Create the USER-SPECIFIC folder
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(user_folder, exist_ok=True)

        # --- NEW: Save the Script Text ---
        if script_text:
            text_file_path = os.path.join(user_folder, "description.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(script_text)
            print(f"Script saved to: {text_file_path}")

        saved_paths = []
        uploaded_filenames = []

        # 3. Save the uploaded images
        for key, file in request.files.items():
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                save_path = os.path.join(user_folder, filename)
                file.save(save_path)
                saved_paths.append(save_path)
                print(f"File saved in session folder: {save_path}")
                uploaded_filenames.append(filename)
                
                
        # --- NEW: Generate FFmpeg input.txt Manifest ---
      # --- NEW: Generate FFmpeg input.txt Manifest ---
        print(f"DEBUG: Attempting to write manifest for: {uploaded_filenames}")
        if uploaded_filenames:
            try:
                manifest_path = os.path.join(user_folder, "input.txt")
                with open(manifest_path, "w") as f:
                    for fname in uploaded_filenames:
                        f.write(f"file '{fname}'\n")
                        f.write("duration 1\n")
                    f.write(f"file '{uploaded_filenames[-1]}'\n")
                print(f"✅ SUCCESS: Manifest created at {manifest_path}")
            except Exception as e:
                print(f"❌ ERROR writing manifest: {e}")
        else:
            print("⚠️ WARNING: No filenames captured. Check your form/loop.")

        # 4. Redirect to Gallery after success to avoid the 404/Empty screen
        return redirect(url_for('main.gallery'))

    # GET request returns the form
    return render_template("create.html", myid=session_id)

@main_bp.route("/gallery")
def gallery():
    # 1. Find the reels folder securely
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    reels_dir = os.path.join(BASE_DIR, 'static', 'reels')
    
    videos = []
    
    # 2. Scan the folder for .mp4 files
    if os.path.exists(reels_dir):
        # List all files and keep only the MP4s
        videos = [f for f in os.listdir(reels_dir) if f.endswith('.mp4')]
        
        # Optional: Sort them by creation time so the newest is at the top
        videos.sort(key=lambda x: os.path.getmtime(os.path.join(reels_dir, x)), reverse=True)

    # 3. Pass the list of video names to the HTML template
    return render_template('gallery.html', videos=videos)
    