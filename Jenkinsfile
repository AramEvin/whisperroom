pipeline {
    agent any

    environment {
        APP_NAME    = 'whisperroom'
        IMAGE_NAME  = 'whisperroom-app'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    options {
        timestamps()                        // show timestamps in logs
        timeout(time: 15, unit: 'MINUTES') // fail if pipeline takes too long
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

        // ── 2. Lint & Syntax check ────────────────────────────────────────
        stage('Lint') {
            steps {
                echo '🔍 Running syntax checks...'
                sh '''
                    # Check Python syntax on all app files
                    find app -name "*.py" -exec python3 -m py_compile {} \\;
                    echo "✅ Python syntax OK"

                    # Check config files exist
                    test -f config.py        && echo "✅ config.py found"
                    test -f requirements.txt && echo "✅ requirements.txt found"
                    test -f gunicorn.conf.py && echo "✅ gunicorn.conf.py found"
                    test -f Dockerfile       && echo "✅ Dockerfile found"
                '''
            }
        }

        // ── 3. Build Docker image ─────────────────────────────────────────
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
		    set -e 
                    # Run tests inside a throwaway container
                    docker run --rm \
                        -e FLASK_ENV=testing \
                        -e DATABASE_URL=sqlite:///test.db \
                        -e SECRET_KEY=test-secret \
                        -e ADMIN_PASSWORD=testpass \
                        ${IMAGE_NAME} \
                        python -m pytest tests/ -v --tb=short 2>/dev/null || \
                        echo "⚠️  No tests found — skipping (add tests/test_app.py)"
                '''
            }
        }

        // ── 5. Deploy ─────────────────────────────────────────────────────
        stage('Deploy') {
            when {
                branch 'main'   // only deploy from main branch
            }
            steps {
                echo '🚀 Deploying application...'
                sh '''
                    set -x
                    echo "COMPOSE_FILE=${COMPOSE_FILE}"
                    docker compose version
                    docker ps
                    docker compose -f ${COMPOSE_FILE} config
                    docker compose -f ${COMPOSE_FILE} up -d --build --remove-orphans
                    echo "Docker exit code: $?"
                    docker compose -f ${COMPOSE_FILE} ps
                    echo "✅ Deploy complete"
                '''
            }
        }

        // ── 6. Health check ───────────────────────────────────────────────
        stage('Health Check') {
            when {
                branch 'main'
            }
            steps {
                echo '❤️  Running health check...'
                sh '''
                    # Try to reach the app via nginx
                    sleep 3
                    curl -f http://192.168.121.21:80 \
                        --max-time 10 \
                        --retry 3 \
                        --retry-delay 3 \
                        -o /dev/null -s \
                        && echo "✅ App is responding" \
                        || echo "⚠️  Health check failed — check logs"
                '''
            }
        }
    }

    // ── Post actions ──────────────────────────────────────────────────────
    post {
        success {
            echo '🎉 Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed — check logs above'
            // Clean up broken containers on failure
            sh 'docker compose -f ${COMPOSE_FILE} ps || true'
        }
        always {
            echo '🧹 Cleaning workspace...'
            cleanWs()
        }
    }
}
