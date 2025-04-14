FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    xz-utils \
    libxi6 \
    libxrender1 \
    libsm6 \
    libxext6 \
    libxxf86vm1 \
    libgl1 \
    libglu1-mesa \
    libsm6 \
    libxext6 \
    libxrender1 \
    libegl1 \
    libgl1 \
    libglu1-mesa \
    libxi6 \
    libxxf86vm1 \
    libxfixes3 \
    libxcursor1 
    
RUN tar -xJf ./src/assets/blender-4.4.0-linux-x64.tar.xz -C /usr/local \
    && rm ./src/assets/blender-4.4.0-linux-x64.tar.xz \
    && ln -s /usr/local/blender-4.4.0-linux-x64/blender /usr/local/bin/blender

RUN mkdir -p /app/output/video \ 
    && mkdir -p /app/output/audio




CMD ["python", "src/production.py"]
