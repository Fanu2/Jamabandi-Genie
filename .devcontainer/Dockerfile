# Use a slim Python 3.11 image as base
FROM python:3.11-slim

# Prevents interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# ✅ Install system dependencies (OpenCV, basic build tools, Git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# ✅ Set up working directory inside the container
WORKDIR /workspace

# ✅ Upgrade pip before installing packages
RUN python -m pip install --upgrade pip

# ✅ Copy requirements.txt into the container
# Make sure requirements.txt is in your repo root
COPY requirements.txt .

# ✅ Install Python dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose Streamlit's default port
EXPOSE 8501

# Default shell is bash
SHELL ["/bin/bash", "-c"]
