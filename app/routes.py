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

        # 3. Save the uploaded images
        for key, file in request.files.items():
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                save_path = os.path.join(user_folder, filename)
                file.save(save_path)
                saved_paths.append(save_path)
                print(f"File saved in session folder: {save_path}")

        # 4. Redirect to Gallery after success to avoid the 404/Empty screen
        return redirect(url_for('main.gallery'))

    # GET request returns the form
    return render_template("create.html", myid=session_id)

@main_bp.route("/gallery")
def gallery():
    return render_template("gallery.html")