FROM astral/uv:0.8-python3.12-bookworm

# Install Node.js + npm (which includes npx)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtualenv
RUN uv sync

COPY src/ ./src/

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/main.py"]
