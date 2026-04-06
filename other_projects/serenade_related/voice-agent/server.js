const express = require("express");
const multer = require("multer");
const path = require("path");
const crypto = require("crypto");
const { execSync } = require("child_process");
const { runClaude, isBusy, cancelClaude } = require("./lib/claude");
const { transcribe } = require("./lib/stt");
const { synthesize } = require("./lib/tts");
const { logInteraction } = require("./lib/logger");
const { addNote, listNotes, handleNote } = require("./lib/notes");
const { startScheduler, getRunningJob, listJobs, createJob, cancelJob, retryJob } = require("./lib/scheduler");

const app = express();
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 25 * 1024 * 1024 } });
const PORT = process.env.PORT || 3000;
const AUTH_TOKEN = process.env.AUTH_TOKEN;
const REPO_DIR = process.env.REPO_DIR || "/data/serenade-remote-copy";

// --- Ring buffer logger ---
const LOG_BUFFER_SIZE = 50;
const logBuffer = [];

function log(level, message) {
  const entry = { ts: new Date().toISOString(), level, message };
  logBuffer.push(entry);
  if (logBuffer.length > LOG_BUFFER_SIZE) logBuffer.shift();
  const prefix = level === "error" ? "[ERROR]" : level === "warn" ? "[WARN]" : "[INFO]";
  if (level === "error") {
    console.error(`${prefix} ${message}`);
  } else {
    console.log(`${prefix} ${message}`);
  }
}

// In-memory audio cache (auto-expires after 5 min)
const audioCache = new Map();
function storeAudio(base64) {
  const id = crypto.randomUUID();
  audioCache.set(id, base64);
  setTimeout(() => audioCache.delete(id), 5 * 60 * 1000);
  return id;
}

// --- Middleware ---

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

function requireAuth(req, res, next) {
  if (!AUTH_TOKEN) return next();

  const header = req.headers.authorization;
  if (!header || header !== `Bearer ${AUTH_TOKEN}`) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  next();
}

// --- Routes ---

app.get("/api/health", (req, res) => {
  res.json({ status: "ok", busy: isBusy(), repoDir: REPO_DIR });
});

// Cancel running Claude request
app.post("/api/cancel", requireAuth, (req, res) => {
  const cancelled = cancelClaude();
  log("info", `[cancel] ${cancelled ? "Cancelled running request" : "Nothing to cancel"}`);
  res.json({ cancelled });
});

// Server logs endpoint
app.get("/api/logs", requireAuth, (req, res) => {
  res.json({ logs: logBuffer });
});

// Fetch cached audio by ID (auth via query param since <audio> can't send headers)
app.get("/api/audio/:id", (req, res) => {
  if (AUTH_TOKEN && req.query.token !== AUTH_TOKEN) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  const base64 = audioCache.get(req.params.id);
  if (!base64) {
    return res.status(404).json({ error: "Audio not found or expired" });
  }
  const buffer = Buffer.from(base64, "base64");
  res.setHeader("Content-Type", "audio/mpeg");
  res.setHeader("Content-Length", buffer.length);
  res.send(buffer);
});

// Transcribe-only endpoint: just STT, returns text
app.post("/api/transcribe", requireAuth, upload.single("audio"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No audio file provided" });
    }

    log("info", `[transcribe] Received ${Math.round(req.file.size / 1024)}KB audio`);

    const sttStart = Date.now();
    const userText = await transcribe(req.file.buffer);
    const sttMs = Date.now() - sttStart;
    log("info", `[STT] ${sttMs}ms: "${userText}"`);

    if (!userText || !userText.trim()) {
      return res.status(400).json({ error: "Could not transcribe audio. Try again." });
    }

    res.json({ userText, sttMs });
  } catch (err) {
    log("error", `[transcribe] ${err.message}`);
    res.status(500).json({ error: `Transcription failed: ${err.message}` });
  }
});

// Voice endpoint: returns JSON (text first, audio ID for separate fetch)
app.post("/api/voice", requireAuth, upload.single("audio"), async (req, res) => {
  const startTime = Date.now();
  const steps = [];

  try {
    if (isBusy()) {
      return res.status(429).json({ error: "Agent is busy. Try again in a moment.", steps });
    }

    if (!req.file) {
      return res.status(400).json({ error: "No audio file provided", steps });
    }

    const sessionId = req.body.sessionId || null;
    log("info", `[voice] Received ${Math.round(req.file.size / 1024)}KB audio, session=${sessionId || "new"}`);

    // Step 1: STT
    const sttStart = Date.now();
    let userText;
    try {
      userText = await transcribe(req.file.buffer);
      const sttMs = Date.now() - sttStart;
      steps.push({ step: "stt", status: "ok", ms: sttMs, detail: `${(userText || "").length} chars transcribed` });
      log("info", `[STT] ${sttMs}ms: "${userText}"`);
    } catch (err) {
      const sttMs = Date.now() - sttStart;
      steps.push({ step: "stt", status: "error", ms: sttMs, detail: err.message });
      log("error", `[STT] Failed after ${sttMs}ms: ${err.message}`);
      return res.status(500).json({ error: `STT failed: ${err.message}`, steps });
    }

    if (!userText || !userText.trim()) {
      steps.push({ step: "stt", status: "error", ms: Date.now() - sttStart, detail: "Empty transcription" });
      return res.status(400).json({ error: "Could not transcribe audio. Try again.", steps });
    }

    // Step 2: Claude
    const claudeStart = Date.now();
    let claudeResult;
    try {
      claudeResult = await runClaude(userText, sessionId);
      const claudeMs = Date.now() - claudeStart;
      steps.push({ step: "claude", status: "ok", ms: claudeMs, detail: `${claudeResult.result.length} chars` });
      log("info", `[Claude] ${claudeMs}ms, ${claudeResult.result.length} chars`);
    } catch (err) {
      const claudeMs = Date.now() - claudeStart;
      steps.push({ step: "claude", status: "error", ms: claudeMs, detail: err.message });
      log("error", `[Claude] Failed after ${claudeMs}ms: ${err.message}`);
      return res.status(500).json({ error: `Claude failed: ${err.message}`, steps, userText });
    }

    // Step 3: TTS
    const ttsStart = Date.now();
    let audioId = null;
    try {
      const audioBase64 = await synthesize(claudeResult.result);
      const ttsMs = Date.now() - ttsStart;
      const sizeKB = Math.round(audioBase64.length / 1024);
      steps.push({ step: "tts", status: "ok", ms: ttsMs, detail: `${sizeKB}KB audio` });
      log("info", `[TTS] ${ttsMs}ms, ${sizeKB}KB`);
      audioId = storeAudio(audioBase64);
    } catch (err) {
      const ttsMs = Date.now() - ttsStart;
      steps.push({ step: "tts", status: "error", ms: ttsMs, detail: err.message });
      log("error", `[TTS] Failed after ${ttsMs}ms: ${err.message}`);
    }

    const totalMs = Date.now() - startTime;
    log("info", `[voice] Complete in ${totalMs}ms`);
    res.json({
      userText,
      claudeText: claudeResult.result,
      audioId,
      sessionId: claudeResult.sessionId,
      steps,
      timing: { sttMs: Date.now() - sttStart, claudeMs: Date.now() - claudeStart, ttsMs: Date.now() - ttsStart, totalMs },
    });
  } catch (err) {
    log("error", `[voice] Unhandled error: ${err.message}`);
    res.status(500).json({ error: err.message, steps });
  }
});

// Text endpoint: returns JSON
app.post("/api/text", requireAuth, async (req, res) => {
  const startTime = Date.now();
  const steps = [];

  try {
    if (isBusy()) {
      return res.status(429).json({ error: "Agent is busy. Try again in a moment.", steps });
    }

    const { text, sessionId } = req.body;
    if (!text || !text.trim()) {
      return res.status(400).json({ error: "No text provided", steps });
    }

    log("info", `[text] "${text.slice(0, 100)}${text.length > 100 ? "..." : ""}", session=${sessionId || "new"}`);

    // Step 1: Claude
    const claudeStart = Date.now();
    let claudeResult;
    try {
      claudeResult = await runClaude(text, sessionId || null);
      const claudeMs = Date.now() - claudeStart;
      steps.push({ step: "claude", status: "ok", ms: claudeMs, detail: `${claudeResult.result.length} chars` });
      log("info", `[Claude] ${claudeMs}ms, ${claudeResult.result.length} chars`);
      // Log to Supabase (fire-and-forget)
      logInteraction(text, claudeResult).catch(() => {});
    } catch (err) {
      const claudeMs = Date.now() - claudeStart;
      steps.push({ step: "claude", status: "error", ms: claudeMs, detail: err.message });
      log("error", `[Claude] Failed after ${claudeMs}ms: ${err.message}`);
      return res.status(500).json({ error: `Claude failed: ${err.message}`, steps, userText: text });
    }

    // Step 2: TTS
    const ttsStart = Date.now();
    let audioId = null;
    try {
      const audioBase64 = await synthesize(claudeResult.result);
      const ttsMs = Date.now() - ttsStart;
      const sizeKB = Math.round(audioBase64.length / 1024);
      steps.push({ step: "tts", status: "ok", ms: ttsMs, detail: `${sizeKB}KB audio` });
      log("info", `[TTS] ${ttsMs}ms, ${sizeKB}KB`);
      audioId = storeAudio(audioBase64);
    } catch (err) {
      const ttsMs = Date.now() - ttsStart;
      steps.push({ step: "tts", status: "error", ms: ttsMs, detail: err.message });
      log("error", `[TTS] Failed after ${ttsMs}ms: ${err.message}`);
    }

    const totalMs = Date.now() - startTime;
    log("info", `[text] Complete in ${totalMs}ms`);
    res.json({
      userText: text,
      claudeText: claudeResult.result,
      audioId,
      sessionId: claudeResult.sessionId,
      steps,
      timing: { claudeMs: Date.now() - claudeStart, ttsMs: Date.now() - ttsStart, totalMs },
    });
  } catch (err) {
    log("error", `[text] Unhandled error: ${err.message}`);
    res.status(500).json({ error: err.message, steps });
  }
});

// --- Notes endpoints ---

app.post("/api/notes", requireAuth, async (req, res) => {
  try {
    const { what_sean_said, sean_learnings, suggested_file, suggested_section } = req.body;
    if (!what_sean_said) return res.status(400).json({ error: "Nothing to save" });
    const created = await addNote(what_sean_said, {
      seanLearnings: !!sean_learnings,
      suggestedFile: suggested_file || null,
      suggestedSection: suggested_section || null,
    });
    log("info", `[notes] Added: "${what_sean_said.slice(0, 80)}"`);
    res.json(created);
  } catch (err) {
    log("error", `[notes] Add failed: ${err.message}`);
    res.status(500).json({ error: err.message });
  }
});

app.get("/api/notes", requireAuth, async (req, res) => {
  try {
    const notes = await listNotes({
      handled: req.query.handled !== undefined ? req.query.handled === "true" : undefined,
    });
    res.json(notes);
  } catch (err) {
    log("error", `[notes] List failed: ${err.message}`);
    res.status(500).json({ error: err.message });
  }
});

app.patch("/api/notes/:id", requireAuth, async (req, res) => {
  try {
    const result = await handleNote(req.params.id);
    log("info", `[notes] Handled: ${req.params.id}`);
    res.json(result);
  } catch (err) {
    log("error", `[notes] Handle failed: ${err.message}`);
    res.status(500).json({ error: err.message });
  }
});

// --- Scheduled jobs endpoints ---

app.get("/api/jobs", requireAuth, listJobs);
app.post("/api/jobs", requireAuth, createJob);
app.post("/api/jobs/:id/cancel", requireAuth, cancelJob);
app.post("/api/jobs/:id/retry", requireAuth, retryJob);

// Pull latest code
app.post("/api/pull", requireAuth, (req, res) => {
  try {
    const output = execSync("git fetch origin && git merge origin/main --no-edit", { cwd: REPO_DIR, timeout: 30000, shell: true }).toString();
    log("info", `[pull] ${output.trim()}`);
    res.json({ status: "ok", output: output.trim() });
  } catch (err) {
    log("error", `[pull] ${err.message}`);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  log("info", `Voice agent server running on port ${PORT}`);
  log("info", `Repo dir: ${REPO_DIR}`);
  startScheduler();
});
