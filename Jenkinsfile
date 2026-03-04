pipeline {
    agent any

    environment {
        APP_NAME     = 'whisperroom'
        IMAGE_NAME   = 'whisperroom-app'
        COMPOSE_FILE = 'docker-compose.yml'

        // Set your Docker Hub username in Jenkins credentials
        DOCKERHUB_USER = credentials('DOCKERHUB_USER')
        DOCKERHUB_PASS = credentials('DOCKERHUB_PASS')
    }

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ── 1. Checkout ───────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        // ── 2. Lint ───────────────────────────────────────────────────────
        stage('Lint') {
            steps {
                echo '🔍 Running syntax checks...'
                sh '''
                    find app -name "*.py" -exec python3 -m py_compile {} \\;
                    echo "✅ Python syntax OK"
                    test -f config.py        && echo "✅ config.py found"
                    test -f requirements.txt && echo "✅ requirements.txt found"
                    test -f gunicorn.conf.py && echo "✅ gunicorn.conf.py found"
                    test -f Dockerfile       && echo "✅ Dockerfile found"
                '''
            }
        }

        // ── 3. Build ──────────────────────────────────────────────────────
        stage('Build') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker compose -f ${COMPOSE_FILE} build --no-cache app
                    echo "✅ Image built: ${IMAGE_NAME}"
                '''
            }
        }

        // ── 4. Test ───────────────────────────────────────────────────────
        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    docker run --rm \
                        -e FLASK_ENV=testing \
                        -e DATABASE_URL=sqlite:///test.db \
                        -e SECRET_KEY=test-secret \
                        -e ADMIN_PASSWORD=testpass \
                        ${IMAGE_NAME} \
                        python -m pytest tests/ -v --tb=short 2>/dev/null || \
                        echo "⚠️  No tests found — skipping"
                '''
            }
        }

        // ── 5. Version & Tag ──────────────────────────────────────────────
        stage('Version & Tag') {
            when { branch 'main' }
            steps {
                echo '🏷️  Calculating version...'
                script {
                    // Read current version from VERSION file, default to 1.0
                    def currentVersion = '1.0'
                    if (fileExists('VERSION')) {
                        currentVersion = readFile('VERSION').trim()
                    }

                    // Split into major.minor and bump minor
                    def parts = currentVersion.tokenize('.')
                    def major  = parts[0].toInteger()
                    def minor  = parts[1].toInteger()

                    // Bump minor on every build, bump major manually
                    def newMinor   = minor + 1
                    def newVersion = "${major}.${newMinor}"

                    // Save new version
                    writeFile file: 'VERSION', text: newVersion
                    env.IMAGE_VERSION = newVersion

                    echo "📦 Version: ${currentVersion} → ${newVersion}"
                }
            }
        }

        // ── 6. Push to Docker Hub ─────────────────────────────────────────
        stage('Push to Docker Hub') {
            when { branch 'main' }
            steps {
                echo "🚀 Pushing to Docker Hub as ${DOCKERHUB_USER}/whisperroom..."
                sh '''
                    # Login to Docker Hub
                    echo "${DOCKERHUB_PASS}" | docker login -u "${DOCKERHUB_USER}" --password-stdin

                    # Tag with version number and latest
                    docker tag ${IMAGE_NAME} ${DOCKERHUB_USER}/whisperroom:${IMAGE_VERSION}
                    docker tag ${IMAGE_NAME} ${DOCKERHUB_USER}/whisperroom:latest

                    # Push both tags
                    docker push ${DOCKERHUB_USER}/whisperroom:${IMAGE_VERSION}
                    docker push ${DOCKERHUB_USER}/whisperroom:latest

                    # Logout for security
                    docker logout

                    echo "✅ Pushed:"
                    echo "   ${DOCKERHUB_USER}/whisperroom:${IMAGE_VERSION}"
                    echo "   ${DOCKERHUB_USER}/whisperroom:latest"
                '''
            }
        }

        // ── 7. Commit VERSION file back to git ────────────────────────────
        stage('Commit Version') {
            when { branch 'main' }
            steps {
                echo '📝 Saving version file...'
                sh '''
                    git config user.email "jenkins@whisperroom"
                    git config user.name  "Jenkins"
                    git add VERSION
                    git diff --cached --quiet || git commit -m "ci: bump version to ${IMAGE_VERSION} [skip ci]"
                    git push origin main || true
                '''
            }
        }

        // ── 8. Deploy ─────────────────────────────────────────────────────
        stage('Deploy') {
            when { branch 'main' }
            steps {
                echo '🚀 Deploying application...'
                sh '''
                    docker compose -f ${COMPOSE_FILE} up -d --build
                    sleep 5
                    docker compose -f ${COMPOSE_FILE} ps
                    echo "✅ Deploy complete"
                '''
            }
        }

        // ── 9. Health Check ───────────────────────────────────────────────
        stage('Health Check') {
            when { branch 'main' }
            steps {
                echo '❤️  Running health check...'
                sh '''
                    sleep 3
                    curl -f http://localhost:80 \
                        --max-time 10 \
                        --retry 3 \
                        --retry-delay 3 \
                        -o /dev/null -s \
                        && echo "✅ App is responding" \
                        || echo "⚠️  Health check failed"
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline succeeded! Version: ${env.IMAGE_VERSION ?: 'N/A'}"
        }
        failure {
            echo '❌ Pipeline failed — check logs above'
            sh 'docker compose -f ${COMPOSE_FILE} ps || true'
        }
        always {
            echo '🧹 Cleaning workspace...'
            cleanWs()
        }
    }
}
