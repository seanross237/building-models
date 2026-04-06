// In dev, Vite proxies /api/* to Modal. In production, set VITE_API_URL to the Modal URL.
const API_BASE = import.meta.env.VITE_API_URL || "/api";

export interface GenerateSongParams {
  message: string;
  style: string;
}

export interface GenerateSongResult {
  audioUrl: string;
  generationTimeMs: number;
}

export async function generateSong(params: GenerateSongParams): Promise<GenerateSongResult> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: params.message,
      style: params.style,
    }),
  });

  if (!res.ok) {
    let errorMsg = "Song generation failed";
    try {
      const err = await res.json();
      errorMsg = err.error || errorMsg;
    } catch {
      // response wasn't JSON
    }
    throw new Error(errorMsg);
  }

  const audioBlob = await res.blob();
  const audioUrl = URL.createObjectURL(audioBlob);
  const generationTimeMs = parseInt(res.headers.get("X-Generation-Time-Ms") || "0", 10);

  return { audioUrl, generationTimeMs };
}
