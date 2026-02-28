# 👻 WhisperRoom v2

> Anonymous real-time group chat. Multiple rooms. Persistent nicknames. No sign-up.

## ✨ Features

- 🎭 Random nickname that **persists across sessions** (stored in cookie + SQLite)
- 🏠 **Multiple chat rooms** — create any room, list on lobby
- 💾 **Message history** — last 50 messages loaded when you join a room
- ⚡ Real-time messaging via WebSockets
- 👥 Live online users list per room
- ✍️ Typing indicator
- 📱 Mobile friendly

## 🗂️ Project Structure

```
whisperroom/
├── run.py                        # Entry point
├── config.py                     # Dev / Prod config
├── requirements.txt
├── .env.example
├── .gitignore
└── app/
    ├── __init__.py               # App factory
    ├── utils.py                  # Nick + token generators
    ├── models/
    │   ├── room.py               # Room model
    │   ├── message.py            # Message model
    │   └── session.py            # UserSession model
    ├── blueprints/
    │   ├── main.py               # Lobby routes
    │   ├── chat.py               # Room route
    │   └── events.py             # All Socket.IO events
    └── templates/
        ├── base.html
        ├── main/lobby.html
        └── chat/room.html
```

## 🚀 Quick Start

```bash
# 1. Clone & enter
git clone https://github.com/YOUR_USERNAME/whisperroom.git
cd whisperroom

# 2. Virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Copy env
cp .env.example .env

# 5. Run (auto-creates DB and default room)
python run.py
```

Open: http://localhost:5000
Local network: http://YOUR_LOCAL_IP:5000

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, Flask |
| Real-time | Flask-SocketIO (WebSockets) |
| Database | SQLite via Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Frontend | Vanilla HTML/CSS/JS |

## 🗺️ Build History

- [x] Step 1: Project structure + base UI
- [x] Step 2: Real-time messaging with Flask-SocketIO  
- [x] Step 3: Live online users list with join/leave events
- [x] Step 4: Typing indicator + polish
- [x] Step 5: SQLite DB, multiple rooms, persistent nicknames, modular structure
EOF
