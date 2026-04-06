"""
Tiny Toons API — Song generation via ACE-Step 1.5 on Modal

Deploy:  modal deploy api/modal_api.py
Test:    modal run api/modal_api.py
Logs:    modal app logs tiny-toons-api
"""

from pathlib import Path

import modal

# ---------------------------------------------------------------------------
# Image
# ---------------------------------------------------------------------------
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git", "ffmpeg")
    .pip_install(
        "torch==2.10.0+cu128",
        "torchvision==0.25.0+cu128",
        "torchaudio==2.10.0+cu128",
        index_url="https://download.pytorch.org/whl/cu128",
    )
    .run_commands(
        "git clone https://github.com/ace-step/ACE-Step-1.5.git /opt/ace-step",
        "pip install --no-deps /opt/ace-step/acestep/third_parts/nano-vllm/",
    )
    .pip_install(
        "xxhash",
        "triton>=3.0.0",
        "transformers>=4.51.0,<4.58.0",
        "diffusers",
        "safetensors==0.7.0",
        "scipy>=1.10.1",
        "soundfile>=0.13.1",
        "loguru>=0.7.3",
        "einops>=0.8.1",
        "accelerate>=1.12.0",
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.27.0",
        "numba>=0.63.1",
        "vector-quantize-pytorch>=1.27.15",
        "torchcodec>=0.9.1",
        "torchao>=0.14.1,<0.16.0",
        "toml",
        "modelscope",
        "diskcache",
        "typer-slim>=0.21.1",
        "peft>=0.18.0",
        "matplotlib>=3.7.5",
    )
    .run_commands(
        "pip install --no-deps -e /opt/ace-step/",
    )
)

# ---------------------------------------------------------------------------
# Share the model cache volume with serenade-ace-step
# ---------------------------------------------------------------------------
CHECKPOINTS_DIR = "/root/checkpoints"
model_cache = modal.Volume.from_name("ace-step-1.5-models")

app = modal.App("tiny-toons-api")


@app.cls(
    gpu="l40s",
    image=image,
    volumes={CHECKPOINTS_DIR: model_cache},
    timeout=300,
    scaledown_window=120,
)
class SongGenerator:
    """ACE-Step 1.5 song generation with a FastAPI web server."""

    @modal.enter()
    def init(self):
        import sys
        sys.path.insert(0, "/opt/ace-step")

        from acestep.handler import AceStepHandler
        from acestep.llm_inference import LLMHandler
        from acestep.gpu_config import get_gpu_config, set_global_gpu_config

        gpu_config = get_gpu_config()
        set_global_gpu_config(gpu_config)

        self.dit_handler = AceStepHandler()
        status, success = self.dit_handler.initialize_service(
            project_root=CHECKPOINTS_DIR,
            config_path="acestep-v15-turbo",
            device="cuda",
            use_flash_attention=True,
            compile_model=False,
            offload_to_cpu=False,
            offload_dit_to_cpu=False,
            use_mlx_dit=False,
        )
        print(f"DiT init: {status} (success={success})")

        self.llm_handler = LLMHandler()
        self.llm_handler.initialize(
            checkpoint_dir=CHECKPOINTS_DIR,
            lm_model_path="acestep-5Hz-lm-4B",
            backend="pt",
        )
        print(f"LLM init: initialized={self.llm_handler.llm_initialized}")

    def _generate_song(self, message: str, style: str) -> bytes:
        """Generate a song from a message and style. Returns MP3 bytes."""
        from acestep.inference import (
            GenerationParams,
            GenerationConfig,
            generate_music,
        )

        lyrics = f"[Verse]\n{message}"
        caption = f"{style}, catchy, melodic, short song, fun"

        params = GenerationParams(
            caption=caption,
            lyrics=lyrics,
            duration=30.0,
            vocal_language="en",
            inference_steps=8,
            guidance_scale=7.0,
            thinking=True,
            use_cot_caption=True,
            use_cot_language=True,
            use_cot_metas=True,
            seed=-1,
            task_type="text2music",
        )

        config = GenerationConfig(
            batch_size=1,
            use_random_seed=True,
            audio_format="mp3",
        )

        result = generate_music(
            dit_handler=self.dit_handler,
            llm_handler=self.llm_handler,
            params=params,
            config=config,
            save_dir="/tmp/tiny-toons-output",
        )

        if not result.success:
            raise Exception(f"Generation failed: {result.error or result.status_message}")

        if not result.audios:
            raise Exception("No audio generated")

        audio = result.audios[0]
        audio_path = audio.get("path") or audio.get("file")
        if not audio_path or not Path(audio_path).exists():
            raise Exception("Audio file not found")

        return Path(audio_path).read_bytes()

    @modal.asgi_app()
    def web(self):
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import Response
        from pydantic import BaseModel
        import time

        web_app = FastAPI(title="Tiny Toons API")
        web_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        class GenerateRequest(BaseModel):
            message: str
            style: str = "Pop"

        @web_app.post("/generate")
        async def generate(data: GenerateRequest):
            if not data.message.strip():
                return Response(
                    content='{"error": "Message is required"}',
                    status_code=400,
                    media_type="application/json",
                )

            start = time.time()
            try:
                audio_bytes = self._generate_song(data.message.strip(), data.style.strip())
            except Exception as e:
                return Response(
                    content=f'{{"error": "{str(e)}"}}',
                    status_code=500,
                    media_type="application/json",
                )

            elapsed = time.time() - start
            print(f"Generated song in {elapsed:.1f}s ({len(audio_bytes) / 1024:.0f} KB)")

            return Response(
                content=audio_bytes,
                status_code=200,
                media_type="audio/mpeg",
                headers={"X-Generation-Time-Ms": str(int(elapsed * 1000))},
            )

        @web_app.get("/health")
        async def health():
            return {"status": "ok"}

        return web_app


# ---------------------------------------------------------------------------
# Local test: modal run api/modal_api.py
# ---------------------------------------------------------------------------
@app.local_entrypoint()
def main():
    generator = SongGenerator()

    print("Generating test song...")
    audio_bytes = generator._generate_song.remote(
        message="Happy birthday Mom! You're the best and I love you so much.",
        style="Pop",
    )

    output = Path("/tmp/tiny-toons-test.mp3")
    output.write_bytes(audio_bytes)
    print(f"Saved: {output} ({len(audio_bytes) / 1024:.0f} KB)")
    print(f"Play: open {output}")
