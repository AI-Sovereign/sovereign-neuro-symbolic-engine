FROM python:3.10-slim

# The standard "I need audio and video processing to pretend I'm alive" packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying your "masterpiece" into the container
COPY . .

# Setting up the environment so your neural weights don't vanish into the void
ENV HF_DATA_PATH="/data"
RUN mkdir -p /data/aeterna_storage_v_nova && chmod -R 777 /data

# Render injects the PORT dynamically. Defaulting to 7860 just in case.
ENV PORT=7860
EXPOSE $PORT

# Run the beast
CMD ["python", "app.py"]

