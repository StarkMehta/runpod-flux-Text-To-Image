import runpod
import torch
from diffusers import FluxPipeline
import base64
from io import BytesIO
import os

# 1. INITIALIZATION: Runs once on boot
print("--- Initializing Smart FLUX Handler ---")
device = "cuda" if torch.cuda.is_available() else "cpu"

# Logic to detect GPU Capacity
vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
print(f"Detected VRAM: {vram_gb:.2f} GB")

try:
    # Load model weights
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-schnell", 
        torch_dtype=torch.bfloat16
    )

    # DYNAMIC OPTIMIZATION
    if vram_gb >= 40:
        print("Strategy: High Performance (Full VRAM)")
        pipe.to(device)
    elif vram_gb >= 22:
        print("Strategy: Balanced (CPU Offload)")
        pipe.enable_model_cpu_offload()
    else:
        print("Strategy: Low Memory (Sequential Offload)")
        pipe.enable_sequential_cpu_offload()

    # Always enable for stability
    pipe.enable_vae_slicing()
    
    print("--- Model Loaded Successfully ---")
except Exception as e:
    print(f"Error loading model: {e}")
    raise e

def handler(job):
    job_input = job.get("input", {})
    prompt = job_input.get("prompt", "A futuristic cyberpunk city")
    width = job_input.get("width", 1024)
    height = job_input.get("height", 1024)

    try:
        # High-speed Inference
        image = pipe(
            prompt,
            num_inference_steps=4,
            guidance_scale=0.0, 
            width=width,
            height=height
        ).images[0]

        # Convert to Base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {"image": img_str, "status": "success"}

    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})