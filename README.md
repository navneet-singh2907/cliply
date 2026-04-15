Cliply: Decoupled AI Video Processing Engine

![Cliply Demo Presentation](link-to-your-demo-gif-or-video-here.gif)

**Cliply** is a full-stack, asynchronous microservice that automatically generates 9:16 video reels using AI voiceovers and dynamic media conforming. 

Instead of relying on a monolithic, blocking web server, Cliply utilizes a **Decoupled Worker Architecture**. It separates the web interface from the heavy media rendering pipeline, allowing for real-time user feedback, queue processing, and seamless API integrations without freezing the client application.

---

## System Architecture & Tech Stack

- Frontend: HTML5, CSS Grid, Vanilla JavaScript (Asynchronous Polling)
- Producer (Web Layer): Flask, Werkzeug, Jinja2, Python Blueprint Routing
- Consumer (Processing Daemon): Python Background Engine, File I/O Management
- Media Orchestration: FFmpeg (Concat demuxer, aspect ratio conforming, A/V multiplexing)
- AI Integration: ElevenLabs API (Text-to-Speech)

---

## Core Features

Asynchronous Media Rendering:** The web server captures payloads and immediately frees the main thread, passing the heavy FFmpeg rendering to an independent background worker.
Client-Server Polling:** Implemented a JavaScript polling bridge that queries a Flask REST API (`/check_status`) to provide a real-time progress bar, redirecting automatically upon the daemon's completion.
Dynamic UUID Sessions:** Every upload triggers a sandboxed UUID environment, preventing data crossover and allowing for safe, parallel batch processing.
Automated Media Conforming:** Programmatically commands FFmpeg to ingest varying array lengths of images, pad them to a strict `1080x1920` (9:16) format, and sync duration dynamically (`-shortest` flag) with the AI-generated audio track.

---

## Engineering Challenges & Solutions

Building a multi-stage assembly line introduced complex race conditions and environment execution errors. Here is how I architected solutions for the system's core bottlenecks:

1. Asynchronous I/O Race Conditions

**The Problem:** The background worker (`generation_engine.py`) was triggering the FFmpeg subprocess the millisecond the ElevenLabs API initiated the audio download. Because the `.mp3` file was zero bytes or incomplete on disk, FFmpeg crashed with a `No such file or directory` error.

**The Solution:** I engineered a defensive file I/O "Wait Guard." Before executing the subprocess, the engine actively loops, forcing the thread to sleep and verify both the file's existence and completion state. This prevents the worker from moving to the rendering stage until the network payload is fully flushed to the disk.

2. Context-Aware Pathing in a Microservice

**The Problem:** The Flask server and the background daemon were launched from different directory levels. Relying on the Current Working Directory (`os.getcwd()`) caused relative pathing failures, creating ghost folders and losing media assets.

**The Solution:** I refactored the entire codebase to use absolute, context-aware pathing via `os.path.abspath(__file__)`. The engine now dynamically maps its own location at runtime, building an unbreakable, environment-agnostic bridge to the `static/uploads` directory regardless of how or where the cron job or script is executed.

3. Namespace Routing & Werkzeug BuildErrors

**The Problem:** Scaling the application using Flask Blueprints caused `werkzeug.routing.exceptions.BuildError` crashes when the UI attempted to redirect users to the asynchronous processing room.

**The Solution:** Mapped the internal routing logic strictly to the Blueprint namespace (`url_for('main.processing')`), cleanly separating the API status pings and gallery UI rendering from the core application initialization.

---

⚙️ Local Installation & Execution

Because Cliply is a decoupled system, it requires two processes to run simultaneously.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/navneet-singh2907/cliply.git](https://github.com/navneet-singh2907/cliply.git)
   cd cliply
   ```

## Environment Setup: Create a .env file in the root directory and add your ElevenLabs key:

    ELEVENLABS_API_KEY=your_api_key_here

#  Cliply: Decoupled AI Video Processing Engine

**[ Live UI Demo (Frontend Only)]**(https://(https://cliply-azure.vercel.app/))
*(Note: This demo is a frontend-only Vercel deployment to showcase the UI and async polling. The heavy FFmpeg/AI backend is fully functional when run locally or on a dedicated server.)*




## Future Roadmap
[ ] Migrate local SQLite database to Supabase for persistent user account memory.

[ ] Implement AWS S3 or Cloudinary storage for ephemeral server compatibility (Render/Railway).

[ ] Integrate Celery/Redis for enterprise-grade task queuing and distributed worker scaling.
