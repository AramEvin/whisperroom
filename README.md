# 👻 WhisperRoom

> Anonymous real-time group chat. Multiple rooms. Persistent nicknames. No sign-up.

## ✨ Features

- 🎭 Random nickname that persists across sessions
- 🏠 Multiple chat rooms — create any room, listed in lobby
- 💾 Message history — last 50 messages loaded on join
- ⚡ Real-time messaging via WebSockets
- 👥 Live online users list per room
- ✍️  Typing indicator
- 🔔 Sound notifications (toggleable)
- 🔐 Admin panel — delete rooms, ban/unban users
- 🐳 Docker + Nginx deploy ready

## 🗂️ Project Structure

```
whisperroom/
├── run.py                         # Entry point
├── config.py                      # Dev / Prod config
├── gunicorn.conf.py               # Production server config
├── Dockerfile                     # Container build
├── docker-compose.yml             # Full stack (app + nginx)
├── .dockerignore
├── requirements.txt
├── .env.example
├── .gitignore
├── nginx/
│   └── whisperroom.conf           # Nginx reverse proxy config
└── app/
    ├── __init__.py                # App factory
    ├── utils.py                   # Nick + token generators
    ├── models/
    │   ├── room.py
    │   ├── message.py
    │   └── session.py
    ├── blueprints/
    │   ├── main.py                # Lobby
    │   ├── chat.py                # Room page
    │   ├── admin.py               # Admin panel
    │   └── events.py              # Socket.IO events
    └── templates/
        ├── base.html
        ├── main/lobby.html
        ├── chat/room.html
        └── admin/{login,dashboard,users}.html
```

## 🚀 Local Development

```bash
git clone https://github.com/YOUR_USERNAME/whisperroom.git
cd whisperroom

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env           # edit SECRET_KEY and ADMIN_PASSWORD

python run.py
# → http://localhost:5000
```

## 🐳 Deploy with Docker

```bash
# 1. Copy and edit your env file
cp .env.example .env
nano .env                      # set SECRET_KEY and ADMIN_PASSWORD

# 2. Build and start everything (app + nginx)
docker compose up -d --build

# 3. Check logs
docker compose logs -f

# → http://YOUR_SERVER_IP
# → http://YOUR_SERVER_IP/admin
```

## 🔧 Deploy without Docker (VPS manual)

```bash
# On your server
git clone https://github.com/YOUR_USERNAME/whisperroom.git
cd whisperroom
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env

# Init DB
python -c "from run import app; from app import db; app.app_context().__enter__(); db.create_all()"

# Run with gunicorn
gunicorn --config gunicorn.conf.py run:app

# Set up nginx separately
sudo cp nginx/whisperroom.conf /etc/nginx/sites-available/whisperroom
sudo ln -s /etc/nginx/sites-available/whisperroom /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## 🔐 Admin Panel

Visit `/admin` — default password is `admin1234`.
**Change it** by setting `ADMIN_PASSWORD` in your `.env` file.

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, Flask |
| Real-time | Flask-SocketIO (WebSockets) |
| Database | SQLite via Flask-SQLAlchemy |
| Prod server | Gunicorn + gevent |
| Reverse proxy | Nginx |
| Container | Docker + Docker Compose |

## 🗺️ Build History

- [x] Step 1: Project structure + base UI
- [x] Step 2: Real-time messaging with Flask-SocketIO
- [x] Step 3: Live online users list with join/leave events
- [x] Step 4: Typing indicator + polish
- [x] Step 5: SQLite DB, multiple rooms, persistent nicknames, modular structure
- [x] Step 6: Admin panel, sound notifications, @mention highlighting
- [x] Step 7: Docker + Gunicorn + Nginx deploy setup
