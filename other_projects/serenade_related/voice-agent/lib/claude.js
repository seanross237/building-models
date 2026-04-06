const { spawn } = require("child_process");
const path = require("path");

const REPO_DIR = process.env.REPO_DIR || "/data/serenade-remote-copy";
const TIMEOUT_MS = 5 * 60 * 1000; // 5 minutes

let busy = false;
let currentChild = null;
let cancelledFlag = false;

function isBusy() {
  return busy;
}

const SYSTEM_PROMPT = [
  "Keep responses concise (2-3 paragraphs max) since they will be spoken aloud via TTS. Avoid code blocks, bullet lists, and markdown formatting — use plain conversational English. If the user asks for code or detailed output, summarize the key points verbally and mention you've made the changes.",
  "",
  "Git workflow: You are working on the 'voice-agent' branch. When you make code changes, commit and push to this branch (git push origin voice-agent). Do NOT push to main unless the user explicitly says to push to main. If the user says 'push to main' or 'push that to main', then push to main.",
  "",
  'Notes/Todos: When Sean says "add a note", "add a to-do", "add food for thought", or "add a quick win", save his FULL voice input (the entire thing he said) to the notes API. If he says "add to Sean Learnings", "add this to Sean Learnings", or mentions "Sean Learnings" in the context of saving a note, set sean_learnings to true.',
  "",
  "IMPORTANT: When saving a note, you MUST ALWAYS include suggested_file and suggested_section in your curl POST body. Pick the best match from these destinations:",
  "  Serenade Clean: file=god-system/pillars/serenade/clean/clean-items.json sections: quick-wins (<30 min tasks), todos, maybe-later",
  "  Serenade Automate: file=god-system/pillars/serenade/automate/automate-items.json sections: open-projects, backlog",
  "  Serenade Push: file=god-system/pillars/serenade/push/push-items.json sections: open-projects, backlog",
  "  Little Upgrades (30min-2hr tasks): file=god-system/pillars/serenade/push/little-upgrades-items.json sections: up-for-grabs, hidden",
  "  Sherpa (systems/meta): file=god-system/pillars/sherpa/sherpa-items.json sections: next-steps, open-questions, backlog, maybe-later",
  "  Big Brain (long-term): file=god-system/pillars/big-brain/big-brain-items.json sections: open-projects, backlog, maybe-later",
  "  Life GetterDones (personal): file=god-system/pillars/life/life-wins.json sections: little-wins, todos, maybe-later",
  "Serenade = song product. Sherpa = work systems. Big Brain = long-term AI/automation. Life = personal. When in doubt, default to Life > todos. Never omit suggested_file/suggested_section.",
  "",
  "Use the Bash tool to call:",
  '  Add: curl -s -X POST http://localhost:$PORT/api/notes -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_TOKEN" -d \'{"what_sean_said":"his full input verbatim","sean_learnings":false,"suggested_file":"path/to/file.json","suggested_section":"section-id"}\'',
  '  (set "sean_learnings":true when he mentions Sean Learnings)',
  '  List: curl -s http://localhost:$PORT/api/notes -H "Authorization: Bearer $AUTH_TOKEN"',
  '  List unhandled: curl -s "http://localhost:$PORT/api/notes?handled=false" -H "Authorization: Bearer $AUTH_TOKEN"',
  '  Mark handled: curl -s -X PATCH http://localhost:$PORT/api/notes/NOTE_ID -H "Authorization: Bearer $AUTH_TOKEN"',
  "Always confirm what you saved. Keep it brief.",
].join("\n");

/**
 * Spawn claude -p and collect output. Returns { result, sessionId, durationMs }.
 */
function spawnClaude(prompt, sessionId) {
  return new Promise((resolve, reject) => {
    const args = [
      "-p",
      prompt,
      "--output-format",
      "json",
      "--model",
      "sonnet",
      "--dangerously-skip-permissions",
      "--append-system-prompt",
      SYSTEM_PROMPT,
    ];

    if (sessionId) {
      args.push("--resume", sessionId);
    }

    const env = { ...process.env };
    delete env.CLAUDECODE;

    const startTime = Date.now();

    const child = spawn("claude", args, {
      cwd: REPO_DIR,
      env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    currentChild = child;

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error("Claude timed out after 5 minutes"));
    }, TIMEOUT_MS);

    child.on("close", (code) => {
      clearTimeout(timer);
      currentChild = null;
      const durationMs = Date.now() - startTime;

      if (cancelledFlag) {
        cancelledFlag = false;
        return reject(new Error("Request cancelled"));
      }

      if (code !== 0 && !stdout) {
        return reject(
          new Error(`Claude exited with code ${code}: ${stderr.trim()}`)
        );
      }

      try {
        const parsed = JSON.parse(stdout);
        let resultText = parsed.result;

        // If result is empty or missing (e.g. stop_reason is tool_use/max_turns),
        // provide a friendly fallback instead of dumping raw JSON
        if (!resultText || !resultText.trim()) {
          if (parsed.stop_reason === "tool_use" || parsed.stop_reason === "error_max_turns") {
            resultText = "I ran out of turns while working on that. You can continue the conversation to pick up where I left off.";
          } else {
            resultText = "I completed the task but didn't produce a text response.";
          }
        }

        resolve({
          result: resultText,
          sessionId: parsed.session_id || sessionId || null,
          durationMs,
          fullOutput: parsed,
        });
      } catch {
        resolve({
          result: stdout.trim() || stderr.trim(),
          sessionId: sessionId || null,
          durationMs,
        });
      }
    });

    child.on("error", (err) => {
      clearTimeout(timer);
      currentChild = null;
      reject(err);
    });
  });
}

/**
 * Run claude -p with the given prompt. Returns { result, sessionId, durationMs }.
 * If sessionId is provided, resumes that session.
 * Auto-retries without session if the session is stale/expired.
 */
async function runClaude(prompt, sessionId) {
  if (busy) {
    throw new Error("Agent is busy with another request");
  }
  busy = true;

  try {
    const result = await spawnClaude(prompt, sessionId);
    return result;
  } catch (err) {
    // If session-related error, retry without session
    if (sessionId && /session|conversation/i.test(err.message)) {
      console.log(`[claude] Session ${sessionId} expired, starting fresh`);
      const result = await spawnClaude(prompt, null);
      return result;
    }
    throw err;
  } finally {
    busy = false;
  }
}

function cancelClaude() {
  if (currentChild) {
    cancelledFlag = true;
    currentChild.kill("SIGTERM");
    return true;
  }
  return false;
}

module.exports = { runClaude, isBusy, cancelClaude };
