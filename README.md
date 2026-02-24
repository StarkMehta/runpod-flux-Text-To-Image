# RunPod Serverless: FLUX.1 Text-to-Image API

I used FLUX.1-schnell because it is the fastest version of FLUX and is free, unlike the 'dev' version.

## Overview
```bash
A simple, reliable API for FLUX.1-schnell. It’s built to be "hardware-aware," meaning it automatically adjusts to whatever GPU you pick without crashing.
```
## Design Choices
```bash
Auto-Memory: The code detects the GPU size. It uses "Fast Mode" for 48GB cards and "Safe Mode" for 24GB cards to prevent memory errors.

Pre-Loaded: The model loads once at startup. This makes individual image requests much faster.

Secure: Uses environment variables for API keys so no secrets are leaked in the code.

Web Ready: Returns images as Base64 strings, making them easy to display on any website.
```
## Deployment

**1. Build & Push**

# Build for RunPod
```bash
docker build --platform linux/amd64 -t "Your Docker Username"/runpod-flux-dev:smart-v1 .
```
# Push to Docker Hub
```bash
docker push "Your Docker Username"/runpod-flux-dev:smart-v1

```
**2. RunPod Settings**
```bash
Image: "Your Docker Username"/runpod-flux-dev:smart-v1

Disk: 50GB

Env: HF_TOKEN = your key

GPU: Works on RTX 3090, 4090, A6000, or A100.
```



