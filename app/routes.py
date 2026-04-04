import uuid
import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename

# We define the blueprint here
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    
    if request.method == "POST":
        # Get the text the user entered
        script_text = request.form.get('text')
        print(f"Processing script: {script_text}")

        # Loop through the files uploaded by your JavaScript
        for key, file in request.files.items():
            if file and file.filename != '':
                # SECURE the filename (Crucial for security!)
                filename = secure_filename(file.filename)
                
                # Create a unique path for this user session
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                print(f"Saved file to: {save_path}")

    return render_template("create.html", myid=myid)

@main_bp.route("/gallery")
def gallery():
    return render_template("gallery.html")