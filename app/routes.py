import uuid
import os
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from werkzeug.utils import secure_filename
from flask import jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/create", methods=["GET", "POST"])
def create():
    session_id = str(uuid.uuid4())
    
    if request.method == "POST":
        # VERCEL MOCKUP: We don't save files here. We just fake the delay.
        print("Demo Mode: Redirecting to processing room...")
        return redirect(url_for('main.processing', session_id=session_id))   

    return render_template("create.html", myid=session_id)

@main_bp.route("/gallery")
def gallery():
    # Find the reels folder securely
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    reels_dir = os.path.join(BASE_DIR, 'static', 'reels')
    
    videos = []
    
    # Scan the folder for .mp4 files
    if os.path.exists(reels_dir):
        # List all files and keep only the MP4s
        videos = [f for f in os.listdir(reels_dir) if f.endswith('.mp4')]
        
        # Optional: Sort them by creation time so the newest is at the top
        videos.sort(key=lambda x: os.path.getmtime(os.path.join(reels_dir, x)), reverse=True)

    # Pass the list of video names to the HTML template
    return render_template('gallery.html', videos=videos)
    
    
    # The Waiting Room Page
@main_bp.route('/processing/<session_id>')
def processing(session_id):
    # This just loads the HTML and passes the UUID to it
    return render_template('processing.html', session_id=session_id)

# The Silent API Ping
@main_bp.route('/check_status/<session_id>')
def check_status(session_id):
    # VERCEL MOCKUP: Always return complete so the UI bar finishes and redirects
    return jsonify({"status": "complete"})  