# Jenkins CI/CD Setup for WhisperRoom

## 1. Start Jenkins

```bash
cd whisperroom

# Start Jenkins (runs on port 8080)
docker compose -f jenkins/docker-compose.jenkins.yml up -d

# Get the initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open: http://localhost:8080 (or http://YOUR_LOCAL_IP:8080)

---

## 2. First-time Jenkins setup

1. Paste the password from above
2. Click **Install suggested plugins** — wait for it to finish
3. Create your admin user
4. Jenkins is ready ✅

---

## 3. Create the Pipeline job

1. Click **New Item**
2. Name it `whisperroom`
3. Choose **Pipeline** → click OK
4. Under **Pipeline** section:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/YOUR_USERNAME/whisperroom.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
5. Click **Save**

---

## 4. Run the pipeline

1. Click **Build Now**
2. Watch the stages in real time:
   - 📥 Checkout
   - 🔍 Lint
   - 🐳 Build
   - 🧪 Test
   - 🚀 Deploy (main branch only)
   - ❤️  Health Check

---

## 5. Auto-trigger on git push (Webhook)

### On GitHub:
1. Go to your repo → Settings → Webhooks → Add webhook
2. Payload URL: `http://YOUR_SERVER_IP:8080/github-webhook/`
3. Content type: `application/json`
4. Events: **Just the push event**
5. Click **Add webhook**

### In Jenkins:
1. Open your pipeline → Configure
2. Check **GitHub hook trigger for GITScm polling**
3. Save

Now every `git push` to `main` triggers the pipeline automatically! 🎉

---

## 6. Pipeline stages explained

| Stage | What it does |
|---|---|
| Checkout | Pulls latest code from GitHub |
| Lint | Checks Python syntax on all files |
| Build | Builds the Docker image |
| Test | Runs pytest inside a container |
| Deploy | Runs `docker compose up -d --build` |
| Health Check | Curls localhost:80 to confirm app is up |

---

## 7. Useful commands

```bash
# View Jenkins logs
docker logs -f jenkins

# Restart Jenkins
docker compose -f jenkins/docker-compose.jenkins.yml restart

# Stop Jenkins
docker compose -f jenkins/docker-compose.jenkins.yml down

# Run tests locally
pip install pytest pytest-flask
pytest tests/ -v
```
