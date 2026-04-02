FROM node:20-slim

# System deps: git, curl, python3, pip, tmux
RUN apt-get update && apt-get install -y \
    git curl gosu python3 python3-pip tmux \
    && rm -rf /var/lib/apt/lists/*

# yt-dlp
RUN pip3 install --break-system-packages yt-dlp

# Claude CLI
RUN npm install -g @anthropic-ai/claude-code

# Non-root user (Claude CLI requirement)
RUN useradd -m -s /bin/bash agent

WORKDIR /app

COPY package.json ./
RUN npm install --production

COPY . .
RUN chmod +x scripts/entrypoint.sh

RUN mkdir -p /data/repos

EXPOSE 3000

CMD ["bash", "scripts/entrypoint.sh"]
