# Custom Jenkins image with Docker CLI inside
FROM jenkins/jenkins:lts-jdk17

USER root

# Install Docker CLI + Docker Compose plugin
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
       | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
       https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Add jenkins user to docker group (matches host docker socket GID)
RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins

# Pre-install useful Jenkins plugins
RUN jenkins-plugin-cli --plugins \
    git \
    workflow-aggregator \
    docker-workflow \
    blueocean \
    credentials-binding \
    timestamper \
    ws-cleanup \
    pipeline-stage-view
