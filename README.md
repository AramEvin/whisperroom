# 👻 WhisperRoom

> Anonymous real-time group chat. No sign-up. No history. Just whispers.

Users get a random nickname when they join. Everyone in the room chats together anonymously.

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/whisperroom.git
cd whisperroom

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open: http://localhost:5000

## 🗺️ Roadmap

- [x] Step 1: Project structure + basic UI
- [ ] Step 2: Real-time messaging with Flask-SocketIO
- [ ] Step 3: Random nickname on join
- [ ] Step 4: Online users list
- [ ] Step 5: Polish + deploy

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SocketIO
- **Frontend:** Vanilla HTML/CSS/JS
- **Real-time:** WebSockets via Socket.IO
