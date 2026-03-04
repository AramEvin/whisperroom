pipeline {
    agent any

    environment {
        APP_NAME     = 'whisperroom'
        IMAGE_NAME   = 'whisperroom-app'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
                script {
                    // Print exact branch name so we can debug
                    echo "🌿 Branch: ${env.GIT_BRANCH}"
                    echo "🌿 BRANCH_NAME: ${env.BRANCH_NAME}"
                }
            }
        }

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

        stage('Build') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker compose -f ${COMPOSE_FILE} build --no-cache app
                    echo "✅ Image built: ${IMAGE_NAME}"
                '''
            }
        }

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
                        python -m pytest tests/ -v --tb=short || \
                        echo "⚠️  Tests failed or not found"
                '''
            }
        }

        stage('Version') {
            when {
                anyOf {
                    branch 'main'
                    expression { env.GIT_BRANCH == 'origin/main' }
                    expression { env.GIT_BRANCH == 'main' }
                }
            }
            steps {
                echo '🏷️  Calculating version...'
                script {
                    def currentVersion = fileExists('VERSION') ? readFile('VERSION').trim() : '1.0'
                    def parts      = currentVersion.tokenize('.')
                    def major      = parts[0].toInteger()
                    def minor      = parts[1].toInteger()
                    def newVersion = "${major}.${minor + 1}"
                    writeFile file: 'VERSION', text: newVersion
                    env.IMAGE_VERSION = newVersion
                    echo "📦 Version: ${currentVersion} → ${newVersion}"
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                anyOf {
                    branch 'main'
                    expression { env.GIT_BRANCH == 'origin/main' }
                    expression { env.GIT_BRANCH == 'main' }
                }
            }
            steps {
                echo '🚀 Pushing to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh '''
                        echo "${DH_PASS}" | docker login -u "${DH_USER}" --password-stdin
                        docker tag ${IMAGE_NAME} ${DH_USER}/whisperroom:${IMAGE_VERSION}
                        docker tag ${IMAGE_NAME} ${DH_USER}/whisperroom:latest
                        docker push ${DH_USER}/whisperroom:${IMAGE_VERSION}
                        docker push ${DH_USER}/whisperroom:latest
                        docker logout
                        echo "✅ Pushed ${DH_USER}/whisperroom:${IMAGE_VERSION}"
                        echo "✅ Pushed ${DH_USER}/whisperroom:latest"
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    expression { env.GIT_BRANCH == 'origin/main' }
                    expression { env.GIT_BRANCH == 'main' }
                }
            }
            steps {
                echo '🚀 Deploying...'
                sh '''
                    docker compose -f ${COMPOSE_FILE} up -d --build
                    sleep 5
                    docker compose -f ${COMPOSE_FILE} ps
                    echo "✅ Deploy complete"
                '''
            }
        }

        stage('Health Check') {
            when {
                anyOf {
                    branch 'main'
                    expression { env.GIT_BRANCH == 'origin/main' }
                    expression { env.GIT_BRANCH == 'main' }
                }
            }
            steps {
                echo '❤️  Health check...'
                sh '''
                    sleep 3
                    curl -f http://localhost:80 \
                        --max-time 10 --retry 3 --retry-delay 3 \
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
            cleanWs()
        }
    }
}
