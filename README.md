# 👻 WhisperRoom

> Anonymous real-time group chat. No sign-up. No history. Just whispers.

Users get a random nickname when they join. Everyone in the room chats together anonymously in real time.

## ✨ Features

- 🎭 Random animal nickname on every visit
- ⚡ Real-time messaging via WebSockets
- 👥 Live online users list with join/leave notifications
- ✍️ Typing indicator ("ghost_fox is typing...")
- 📱 Mobile friendly
- 🕐 Message timestamps on hover

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

# 4. Run
python app.py
```

Open: http://localhost:5000
Local network: http://YOUR_LOCAL_IP:5000

## 🗂️ Project Structure

```
whisperroom/
├── app.py               # Flask + SocketIO server
├── requirements.txt     # Python dependencies
├── .gitignore
├── README.md
└── templates/
    └── index.html       # Full frontend (single file)
```

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SocketIO
- **Frontend:** Vanilla HTML / CSS / JS
- **Real-time:** WebSockets via Socket.IO

## 🗺️ Build Steps

- [x] Step 1: Project structure + base UI
- [x] Step 2: Real-time messaging with Flask-SocketIO
- [x] Step 3: Live online users list with join/leave events
- [x] Step 4: Typing indicator + polish
