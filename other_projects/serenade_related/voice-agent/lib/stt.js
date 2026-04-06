const ASSEMBLYAI_API_KEY = process.env.ASSEMBLYAI_API_KEY;
const POLL_INTERVAL_MS = 1500;

/**
 * Transcribe audio buffer to text using AssemblyAI.
 * 1. Upload audio to AssemblyAI
 * 2. Submit transcription request
 * 3. Poll until complete
 * @param {Buffer} audioBuffer - Raw audio data
 * @returns {Promise<string>} Transcribed text
 */
async function transcribe(audioBuffer) {
  if (!ASSEMBLYAI_API_KEY) {
    throw new Error("ASSEMBLYAI_API_KEY not configured");
  }

  const headers = {
    Authorization: ASSEMBLYAI_API_KEY,
  };

  // Step 1: Upload audio
  console.log(`[STT] Uploading ${audioBuffer.length} bytes to AssemblyAI...`);

  const uploadRes = await fetch("https://api.assemblyai.com/v2/upload", {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/octet-stream" },
    body: audioBuffer,
  });

  if (!uploadRes.ok) {
    const errBody = await uploadRes.text();
    throw new Error(`AssemblyAI upload failed: ${uploadRes.status} ${errBody}`);
  }

  const { upload_url } = await uploadRes.json();
  console.log(`[STT] Upload complete: ${upload_url}`);

  // Step 2: Submit transcription
  const submitRes = await fetch("https://api.assemblyai.com/v2/transcript", {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      audio_url: upload_url,
      speech_models: ["universal-2"],
    }),
  });

  if (!submitRes.ok) {
    const errBody = await submitRes.text();
    throw new Error(`AssemblyAI submit failed: ${submitRes.status} ${errBody}`);
  }

  const { id: transcriptId } = await submitRes.json();
  console.log(`[STT] Transcription submitted: ${transcriptId}`);

  // Step 3: Poll for completion
  const pollUrl = `https://api.assemblyai.com/v2/transcript/${transcriptId}`;

  while (true) {
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));

    const pollRes = await fetch(pollUrl, { headers });
    const result = await pollRes.json();

    if (result.status === "completed") {
      return result.text || "";
    }
    if (result.status === "error") {
      throw new Error(`AssemblyAI transcription failed: ${result.error}`);
    }
  }
}

module.exports = { transcribe };
