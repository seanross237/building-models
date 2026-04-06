FROM node:20-slim

# Install git, curl, and postgresql-client (for psql queries)
RUN apt-get update && apt-get install -y git curl postgresql-client gosu && rm -rf /var/lib/apt/lists/*

# Install Claude CLI
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user (Claude CLI refuses --dangerously-skip-permissions as root)
RUN useradd -m -s /bin/bash agent

# Create app directory
WORKDIR /app

# Copy package files and install
COPY package.json ./
RUN npm install --production

# Copy app source
COPY . .

# Make entrypoint executable
RUN chmod +x scripts/entrypoint.sh

# Create data directory
RUN mkdir -p /data

EXPOSE 3000

CMD ["bash", "scripts/entrypoint.sh"]
