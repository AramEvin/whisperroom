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
| @ Mention | `@nickname` highlights in chat |
| ⚡ Rate limiting | Max 5 messages per 10 seconds per user |
| 🔐 Admin panel | Delete rooms, ban/unban users at `/admin` |
| 🐳 Docker ready | One command deploy with Docker Compose + Nginx |
| 🔁 CI/CD | Jenkins pipeline — lint, build, test, version, push to Docker Hub, deploy |
| 🧪 Test suite | pytest tests covering routes, models, search, auth |

---

## 🗂️ Project Structure

```
whisperroom/
├── run.py                          # Entry point
├── config.py                       # Dev / Prod / Testing config classes
├── gunicorn.conf.py                # Production WSGI server config
├── Dockerfile                      # App container
├── docker-compose.yml              # App + Nginx stack
├── .dockerignore
├── .env.example                    # Environment variables template
├── .gitignore
├── Jenkinsfile                     # CI/CD pipeline definition
├── VERSION                         # Auto-bumped version (e.g. 1.4)
├── pytest.ini                      # Test config
├── conftest.py                     # Pytest path setup
├── requirements.txt                # Dev dependencies
├── requirements.prod.txt           # Prod dependencies (includes gunicorn + gevent)
│
├── nginx/
│   ├── Dockerfile                  # Nginx image with config baked in
│   └── whisperroom.conf            # Reverse proxy + WebSocket config
│
├── jenkins/
│   ├── Dockerfile                  # Jenkins + Docker CLI image
│   ├── docker-compose.jenkins.yml  # Run Jenkins on port 8080
│   ├── entrypoint.sh               # Fixes Docker socket permissions at runtime
│   └── JENKINS_SETUP.md            # Step-by-step Jenkins setup guide
│
├── tests/
│   ├── __init__.py
│   └── test_app.py                 # pytest tests
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
    │   └── events.py               # Socket.IO events + rate limiting
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

# 3. Install dev dependencies (no gevent — Python 3.13 safe)
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

> **Note:** Production uses `requirements.prod.txt` inside Docker (Python 3.11) which includes gunicorn + gevent. Dev uses `requirements.txt` without gevent for Python 3.13 compatibility.

---

## 🔁 CI/CD with Jenkins

### Start Jenkins

```bash
# Start Jenkins on port 8080
docker compose -f jenkins/docker-compose.jenkins.yml up -d

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Open browser
# → http://YOUR_LOCAL_IP:8080
```

### Jenkins Credentials needed

| ID | Kind | Value |
|---|---|---|
| `dockerhub-credentials` | Username with password | Docker Hub username + access token |
| `github-credentials` | Username with password | GitHub username + personal access token |
| `whisperroom-env` | Secret file | Your `.env` file |

### Pipeline stages

```
git push → GitHub webhook → Jenkins
  📥 Checkout
  🔍 Lint
  🐳 Build
  🧪 Test
  🏷️  Version    (main only) → bumps 1.0 → 1.1 → 1.2
  🚀 Push        (main only) → yourname/whisperroom:1.x + latest
  🚀 Deploy      (main only) → docker compose up -d --build
  ❤️  Health Check (main only) → curl localhost:80
```

See **`jenkins/JENKINS_SETUP.md`** for full walkthrough including GitHub webhook setup.

---

## 🧪 Run Tests

```bash
# Always use venv python
python -m pytest tests/ -v
```

Expected output:
```
tests/test_app.py::test_lobby_loads              PASSED
tests/test_app.py::test_create_room              PASSED
tests/test_app.py::test_room_page_loads          PASSED
tests/test_app.py::test_missing_room_returns_404 PASSED
tests/test_app.py::test_admin_login_page         PASSED
tests/test_app.py::test_admin_wrong_password     PASSED
tests/test_app.py::test_admin_correct_password   PASSED
tests/test_app.py::test_admin_requires_login     PASSED
tests/test_app.py::test_search_endpoint          PASSED
tests/test_app.py::test_search_too_short         PASSED
tests/test_app.py::test_room_get_or_create       PASSED
tests/test_app.py::test_user_session_persistence PASSED
tests/test_app.py::test_message_search           PASSED
tests/test_app.py::test_ban_user                 PASSED
```

---

## 🔐 Admin Panel

Visit `/admin` — default password is `admin1234`.
**Always change it** by setting `ADMIN_PASSWORD` in your `.env`.

| Feature | Description |
|---|---|
| Dashboard | Total rooms, messages, users, banned count |
| Rooms | Delete any room + all its messages |
| Users | View all sessions, ban or unban by nickname |

---

## 🐳 Docker Hub

Images are automatically pushed on every `main` build:

```
hub.docker.com/r/YOUR_USERNAME/whisperroom
  tags: latest, 1.4, 1.3, 1.2, 1.1, 1.0
```

Pull and run anywhere:
```bash
docker pull YOUR_USERNAME/whisperroom:latest
```

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.11, Flask 3.0 |
| Real-time | Flask-SocketIO (WebSockets) |
| Database | SQLite via Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Prod server | Gunicorn + gevent-websocket |
| Reverse proxy | Nginx (config baked into image) |
| Containers | Docker + Docker Compose |
| CI/CD | Jenkins Pipeline + Docker Hub |
| Tests | pytest |

---

## 🌿 Git Branch Strategy

```
main      ← stable, auto-deploys via Jenkins + pushes to Docker Hub
testing   ← integration testing
feature/* ← individual features
```

```bash
# Start a new feature
git checkout -b feature/my-feature

# Done → merge to testing → run tests
git checkout testing && git merge feature/my-feature && git push

# All good → merge to main → Jenkins auto-deploys
git checkout main && git merge testing && git push
```

---

## ↩️ Roll Back to Previous Version

```bash
# See commit history
git log --oneline

# Go back to a specific commit
git reset --hard <commit-hash>

# Or pull a specific Docker Hub image version
docker pull YOUR_USERNAME/whisperroom:1.2
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
- [x] Step 10: Docker Hub auto push with versioning, secure credentials, nginx baked into image
