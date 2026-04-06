const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const MAX_TTS_CHARS = 1000;
const VOICE = process.env.TTS_VOICE || "ash";
const SPEED = parseFloat(process.env.TTS_SPEED) || 1.35;

/**
 * Convert text to speech using OpenAI gpt-4o-mini-tts (REST API, no SDK).
 * Truncates long text for TTS (full text is returned separately in transcript).
 * @param {string} text - Text to speak
 * @returns {Promise<string>} Base64-encoded mp3 audio
 */
async function synthesize(text) {
  if (!OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY not configured");
  }

  let ttsText = text;
  if (text.length > MAX_TTS_CHARS) {
    ttsText =
      text.slice(0, MAX_TTS_CHARS) +
      "... I've truncated the rest. Check the transcript for the full response.";
  }

  const response = await fetch("https://api.openai.com/v1/audio/speech", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-mini-tts",
      voice: VOICE,
      input: ttsText,
      speed: SPEED,
      response_format: "mp3",
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`OpenAI TTS failed: ${response.status} ${err}`);
  }

  const buffer = Buffer.from(await response.arrayBuffer());
  return buffer.toString("base64");
}

module.exports = { synthesize };
