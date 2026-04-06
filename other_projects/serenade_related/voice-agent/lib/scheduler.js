const { spawn } = require("child_process");
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;
const REPO_DIR = process.env.REPO_DIR || "/data/serenade-remote-copy";
const AUTH_TOKEN = process.env.AUTH_TOKEN;
const CHECK_INTERVAL_MS = 30 * 1000; // 30 seconds
const JOB_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes per job

let runningJob = null;
let intervalId = null;

// --- Supabase helpers ---

async function supabaseQuery(method, path, body) {
  const url = `${SUPABASE_URL}/rest/v1/${path}`;
  const headers = {
    apikey: SUPABASE_KEY,
    Authorization: `Bearer ${SUPABASE_KEY}`,
    "Content-Type": "application/json",
    Prefer: method === "PATCH" ? "return=representation" : "return=minimal",
  };
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Supabase ${method} ${path}: ${res.status} ${err}`);
  }
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

async function fetchReadyJobs() {
  // Jobs that are ready to run:
  // 1. Queued, run_at has passed (or is null), no dependency
  // 2. Queued, dependency is completed, run_at has passed (or is null)
  const now = new Date().toISOString();
  const url = `agent_scheduled_jobs?status=eq.queued&order=created_at.asc`;
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${url}`, {
    headers: {
      apikey: SUPABASE_KEY,
      Authorization: `Bearer ${SUPABASE_KEY}`,
    },
  });
  if (!res.ok) return [];
  const jobs = await res.json();

  const ready = [];
  for (const job of jobs) {
    // Check run_at
    if (job.run_at && new Date(job.run_at) > new Date()) continue;

    // Check dependency
    if (job.depends_on) {
      const depRes = await fetch(
        `${SUPABASE_URL}/rest/v1/agent_scheduled_jobs?id=eq.${job.depends_on}&select=status`,
        {
          headers: {
            apikey: SUPABASE_KEY,
            Authorization: `Bearer ${SUPABASE_KEY}`,
          },
        }
      );
      if (!depRes.ok) continue;
      const deps = await depRes.json();
      if (!deps.length) continue;

      if (deps[0].status === "failed") {
        // Dependency failed — fail this job too
        await supabaseQuery(
          "PATCH",
          `agent_scheduled_jobs?id=eq.${job.id}`,
          { status: "failed", error: `Dependency ${job.depends_on} failed`, completed_at: new Date().toISOString() }
        );
        console.log(`[scheduler] Job ${job.id} (${job.title}) failed — dependency failed`);
        if (job.telegram_on_complete) {
          sendTelegram(`❌ Scheduled build failed: ${job.title}\nReason: Dependency failed`);
        }
        continue;
      }

      if (deps[0].status !== "completed") continue; // Not done yet
    }

    ready.push(job);
  }

  return ready;
}

// --- Git helpers ---

function gitExec(cmd) {
  return execSync(cmd, { cwd: REPO_DIR, timeout: 30000, shell: true }).toString().trim();
}

function prepareRepoBranch(branch) {
  // Fetch latest
  gitExec("git fetch origin");
  // Make sure we're on a clean state
  gitExec("git checkout main");
  gitExec("git pull origin main");
  // Create or reset the branch
  try {
    gitExec(`git branch -D ${branch}`);
  } catch {}
  gitExec(`git checkout -b ${branch}`);
  console.log(`[scheduler] Branch ${branch} ready (from latest main)`);
}

function pushBranch(branch) {
  gitExec(`git push origin ${branch} --force`);
  console.log(`[scheduler] Pushed branch ${branch}`);
}

function restoreVoiceAgentBranch() {
  try {
    gitExec("git checkout main");
    try { gitExec("git branch -D voice-agent"); } catch {}
    gitExec("git checkout -b voice-agent");
  } catch (err) {
    console.error(`[scheduler] Failed to restore voice-agent branch: ${err.message}`);
  }
}

// --- Claude runner for scheduled jobs ---

function runScheduledClaude(prompt, branch) {
  return new Promise((resolve, reject) => {
    const systemPrompt = [
      `You are running a scheduled build job. Work autonomously — there is no human to ask questions.`,
      `You are on branch "${branch}". Make all your changes, then commit and describe what you did.`,
      `Be thorough but focused. Follow the spec exactly. If something is ambiguous, make the safe choice.`,
      `When done, provide a summary of all changes made.`,
    ].join("\n");

    const args = [
      "-p",
      prompt,
      "--output-format", "json",
      "--model", "sonnet",
      "--dangerously-skip-permissions",
      "--append-system-prompt", systemPrompt,
      "--max-turns", "50",
    ];

    const env = { ...process.env };
    delete env.CLAUDECODE;

    const startTime = Date.now();
    const child = spawn("claude", args, {
      cwd: REPO_DIR,
      env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => { stdout += chunk.toString(); });
    child.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error(`Job timed out after ${JOB_TIMEOUT_MS / 60000} minutes`));
    }, JOB_TIMEOUT_MS);

    child.on("close", (code) => {
      clearTimeout(timer);
      const durationMs = Date.now() - startTime;

      if (code !== 0 && !stdout) {
        return reject(new Error(`Claude exited with code ${code}: ${stderr.trim()}`));
      }

      try {
        const parsed = JSON.parse(stdout);
        resolve({
          result: parsed.result || "Completed without text output",
          sessionId: parsed.session_id,
          durationMs,
          numTurns: parsed.num_turns,
          costUsd: parsed.total_cost_usd,
          model: parsed.model,
        });
      } catch {
        resolve({
          result: stdout.trim() || stderr.trim() || "Completed",
          durationMs,
        });
      }
    });

    child.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

// --- Telegram ---

async function sendTelegram(message) {
  try {
    await fetch(`${SUPABASE_URL}/functions/v1/telegram-me`, {
      method: "POST",
      headers: {
        apikey: SUPABASE_KEY,
        Authorization: `Bearer ${SUPABASE_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
  } catch (err) {
    console.error(`[scheduler] Telegram failed: ${err.message}`);
  }
}

// --- Job execution ---

async function executeJob(job) {
  console.log(`[scheduler] Starting job ${job.id}: ${job.title}`);
  runningJob = job;

  // Mark as running
  await supabaseQuery("PATCH", `agent_scheduled_jobs?id=eq.${job.id}`, {
    status: "running",
    started_at: new Date().toISOString(),
  });

  const branch = job.branch || `scheduled/${job.id.slice(0, 8)}`;

  try {
    // Prepare git branch
    prepareRepoBranch(branch);

    // Read the spec file
    const specPath = path.join(REPO_DIR, job.spec_file);
    if (!fs.existsSync(specPath)) {
      throw new Error(`Spec file not found: ${job.spec_file}`);
    }
    const specContent = fs.readFileSync(specPath, "utf-8");

    const prompt = [
      `# Scheduled Build: ${job.title}`,
      ``,
      `Execute the following build spec. Read it carefully and follow all instructions.`,
      ``,
      `---`,
      ``,
      specContent,
    ].join("\n");

    // Run Claude
    const result = await runScheduledClaude(prompt, branch);

    // Commit and push
    try {
      gitExec("git add -A");
      const commitMsg = `Scheduled build: ${job.title}\n\nSpec: ${job.spec_file}\nJob ID: ${job.id}\n\nCo-Authored-By: Claude Sonnet <noreply@anthropic.com>`;
      gitExec(`git commit -m "${commitMsg.replace(/"/g, '\\"')}" --allow-empty`);
      pushBranch(branch);
    } catch (gitErr) {
      console.log(`[scheduler] Git commit/push note: ${gitErr.message}`);
    }

    // Mark completed
    await supabaseQuery("PATCH", `agent_scheduled_jobs?id=eq.${job.id}`, {
      status: "completed",
      completed_at: new Date().toISOString(),
      result: {
        summary: result.result?.slice(0, 2000),
        branch,
        duration_ms: result.durationMs,
        num_turns: result.numTurns,
        cost_usd: result.costUsd,
        model: result.model,
      },
    });

    console.log(`[scheduler] Job ${job.id} completed in ${Math.round(result.durationMs / 1000)}s`);

    if (job.telegram_on_complete) {
      const costStr = result.costUsd ? ` ($${result.costUsd.toFixed(2)})` : "";
      sendTelegram(
        `✅ Scheduled build complete: ${job.title}\n` +
        `Branch: ${branch}\n` +
        `Duration: ${Math.round(result.durationMs / 1000)}s${costStr}\n` +
        `Summary: ${result.result?.slice(0, 300) || "Done"}`
      );
    }
  } catch (err) {
    console.error(`[scheduler] Job ${job.id} failed: ${err.message}`);

    await supabaseQuery("PATCH", `agent_scheduled_jobs?id=eq.${job.id}`, {
      status: "failed",
      completed_at: new Date().toISOString(),
      error: err.message,
    });

    if (job.telegram_on_complete) {
      sendTelegram(`❌ Scheduled build failed: ${job.title}\nError: ${err.message.slice(0, 300)}`);
    }
  } finally {
    runningJob = null;
    // Restore voice-agent branch for normal operations
    restoreVoiceAgentBranch();
  }
}

// --- Main loop ---

async function checkJobs() {
  if (!SUPABASE_URL || !SUPABASE_KEY) return;
  if (runningJob) return; // One at a time

  try {
    const ready = await fetchReadyJobs();
    if (ready.length > 0) {
      // Run the first ready job
      await executeJob(ready[0]);
    }
  } catch (err) {
    console.error(`[scheduler] Check failed: ${err.message}`);
  }
}

function startScheduler() {
  if (!SUPABASE_URL || !SUPABASE_KEY) {
    console.log("[scheduler] Supabase not configured, scheduler disabled");
    return;
  }
  console.log(`[scheduler] Started — checking every ${CHECK_INTERVAL_MS / 1000}s`);
  intervalId = setInterval(checkJobs, CHECK_INTERVAL_MS);
  // Also check immediately on startup
  setTimeout(checkJobs, 5000);
}

function getRunningJob() {
  return runningJob;
}

// --- API route handlers ---

async function listJobs(req, res) {
  try {
    const status = req.query.status;
    let url = "agent_scheduled_jobs?order=created_at.desc&limit=20";
    if (status) url += `&status=eq.${status}`;
    const result = await fetch(`${SUPABASE_URL}/rest/v1/${url}`, {
      headers: {
        apikey: SUPABASE_KEY,
        Authorization: `Bearer ${SUPABASE_KEY}`,
      },
    });
    const jobs = await result.json();
    res.json({ jobs, running: runningJob?.id || null });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function createJob(req, res) {
  try {
    const { title, spec_file, branch, run_at, depends_on, telegram_on_complete } = req.body;
    if (!title || !spec_file) {
      return res.status(400).json({ error: "title and spec_file are required" });
    }

    const job = {
      title,
      spec_file,
      branch: branch || null,
      run_at: run_at || null,
      depends_on: depends_on || null,
      telegram_on_complete: telegram_on_complete !== false,
    };

    const result = await fetch(`${SUPABASE_URL}/rest/v1/agent_scheduled_jobs`, {
      method: "POST",
      headers: {
        apikey: SUPABASE_KEY,
        Authorization: `Bearer ${SUPABASE_KEY}`,
        "Content-Type": "application/json",
        Prefer: "return=representation",
      },
      body: JSON.stringify(job),
    });

    if (!result.ok) {
      const err = await result.text();
      return res.status(500).json({ error: err });
    }

    const created = await result.json();
    console.log(`[scheduler] Job created: ${title} (${created[0]?.id})`);
    res.json({ job: created[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function cancelJob(req, res) {
  try {
    const { id } = req.params;
    await supabaseQuery("PATCH", `agent_scheduled_jobs?id=eq.${id}&status=eq.queued`, {
      status: "cancelled",
      completed_at: new Date().toISOString(),
    });
    res.json({ cancelled: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function retryJob(req, res) {
  try {
    const { id } = req.params;
    await supabaseQuery("PATCH", `agent_scheduled_jobs?id=eq.${id}`, {
      status: "queued",
      started_at: null,
      completed_at: null,
      result: null,
      error: null,
    });
    res.json({ retried: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

module.exports = {
  startScheduler,
  getRunningJob,
  listJobs,
  createJob,
  cancelJob,
  retryJob,
};
