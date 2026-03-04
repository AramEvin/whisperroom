# 👻 WhisperRoom

> Anonymous real-time group chat. Multiple rooms. Persistent nicknames. No sign-up. Production ready.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=flat-square&logo=jenkins)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎭 Anonymous nicknames | Random name like `silent_fox` — persists across sessions via cookie |
| 🏠 Multiple rooms | Create any room from the lobby, listed with live online count |
| 💾 Message history | Last 50 messages loaded when you join a room |
| ⚡ Real-time messaging | WebSockets via Flask-SocketIO |
| 👥 Live users list | See who is online per room, updates instantly |
| ✍️ Typing indicator | Shows when others are typing |
| 🔔 Sound notifications | Chime on new messages, toggleable per session |
| 🔍 Message search | Search history inside any room with highlight |
| @mention | `@nickname` highlights in chat |
| ⚡ Rate limiting | Max 5 messages per 10 seconds per user |
| 🔐 Admin panel | Delete rooms, ban/unban users at `/admin` |
| 🐳 Docker ready | One command deploy with Docker Compose + Nginx |
| 🔁 CI/CD | Jenkins pipeline — lint, build, test, deploy, health check |
| 🧪 Test suite | 11 pytest tests covering routes, models, search, auth |

---

## 🗂️ Project Structure

```
whisperroom/
├── run.py                          # Entry point
├── config.py                       # Dev / Prod config classes
├── gunicorn.conf.py                # Production WSGI server config
├── Dockerfile                      # App container
├── docker-compose.yml              # App + Nginx stack
├── .dockerignore
├── .env.example                    # Environment variables template
├── .gitignore
├── Jenkinsfile                     # CI/CD pipeline definition
├── pytest.ini                      # Test config
├── requirements.txt
│
├── nginx/
│   └── whisperroom.conf            # Reverse proxy + WebSocket config
│
├── jenkins/
│   ├── Dockerfile                  # Jenkins + Docker CLI image
│   ├── docker-compose.jenkins.yml  # Run Jenkins on port 8080
│   ├── entrypoint.sh               # Fixes Docker socket permissions
│   └── JENKINS_SETUP.md            # Step-by-step Jenkins guide
│
├── tests/
│   ├── __init__.py
│   └── test_app.py                 # 11 pytest tests
│
└── app/
    ├── __init__.py                 # App factory pattern
    ├── utils.py                    # Nick + token generators
    ├── models/
    │   ├── __init__.py
    │   ├── room.py                 # Room model
    │   ├── message.py              # Message model + search
    │   └── session.py              # UserSession + ban tracking
    ├── blueprints/
    │   ├── __init__.py
    │   ├── main.py                 # Lobby routes
    │   ├── chat.py                 # Room page + search API
    │   ├── admin.py                # Admin panel
    │   └── events.py               # All Socket.IO events + rate limiting
    └── templates/
        ├── base.html               # Shared layout + favicon
        ├── main/
        │   └── lobby.html          # Room list with live counts
        ├── chat/
        │   └── room.html           # Full chat UI
        └── admin/
            ├── login.html
            ├── dashboard.html
            └── users.html
```

---

## 🚀 Local Development

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/whisperroom.git
cd whisperroom

# 2. Virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env                      # set SECRET_KEY and ADMIN_PASSWORD

# 5. Run
python run.py
# → http://localhost:5000
# → http://localhost:5000/admin
```

---

## 🐳 Deploy with Docker

```bash
# 1. Configure
cp .env.example .env
nano .env                       # set SECRET_KEY and ADMIN_PASSWORD

# 2. Start app + nginx
docker compose up -d --build

# 3. Check logs
docker compose logs -f app

# → http://YOUR_SERVER_IP
# → http://YOUR_SERVER_IP/admin
```

---

## 🔁 CI/CD with Jenkins

```bash
# 1. Start Jenkins (port 8080)
docker compose -f jenkins/docker-compose.jenkins.yml up -d

# 2. Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 3. Open Jenkins
# → http://YOUR_LOCAL_IP:8080
```

See **`jenkins/JENKINS_SETUP.md`** for full walkthrough including GitHub webhook setup.

### Pipeline stages:
```
git push → webhook → Jenkins
  📥 Checkout → 🔍 Lint → 🐳 Build → 🧪 Test → 🚀 Deploy → ❤️ Health Check
```

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

```
tests/test_app.py::test_lobby_loads              PASSED
tests/test_app.py::test_create_room              PASSED
tests/test_app.py::test_room_page_loads          PASSED
tests/test_app.py::test_missing_room_returns_404 PASSED
tests/test_app.py::test_admin_login_page         PASSED
tests/test_app.py::test_admin_wrong_password     PASSED
tests/test_app.py::test_admin_correct_password   PASSED
tests/test_app.py::test_search_endpoint          PASSED
tests/test_app.py::test_search_too_short         PASSED
tests/test_app.py::test_room_get_or_create       PASSED
tests/test_app.py::test_user_session_persistence PASSED
tests/test_app.py::test_message_search           PASSED
```

---

## 🔐 Admin Panel

Visit `/admin` — default password is `admin1234`.
**Change it** by setting `ADMIN_PASSWORD` in your `.env`.

| Feature | Description |
|---|---|
| Dashboard | Total rooms, messages, users, banned count |
| Rooms | Delete any room + all its messages |
| Users | View all sessions, ban or unban by nickname |

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.11, Flask 3.0 |
| Real-time | Flask-SocketIO (WebSockets) |
| Database | SQLite via Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Prod server | Gunicorn + gevent-websocket |
| Reverse proxy | Nginx |
| Containers | Docker + Docker Compose |
| CI/CD | Jenkins (Pipeline + Blue Ocean) |
| Tests | pytest + pytest-flask |

---

## 🌿 Git Branch Strategy

```
main      ← stable, auto-deploys via Jenkins
testing   ← integration testing
feature/* ← individual features
```

```bash
# Start a new feature
git checkout -b feature/my-feature

# Done → merge to testing
git checkout testing && git merge feature/my-feature

# Tested → merge to main → Jenkins auto-deploys
git checkout main && git merge testing && git push
```

---

## 🗺️ Build History

- [x] Step 1: Project structure + base chat UI
- [x] Step 2: Real-time messaging with Flask-SocketIO
- [x] Step 3: Live online users list with join/leave events
- [x] Step 4: Typing indicator + UI polish
- [x] Step 5: SQLite DB, multiple rooms, persistent nicknames, modular structure
- [x] Step 6: Admin panel, sound notifications, @mention highlighting
- [x] Step 7: Docker + Gunicorn + Nginx production deploy
- [x] Step 8: Message search, rate limiting, live online count badges
- [x] Step 9: Jenkins CI/CD pipeline + pytest test suite
