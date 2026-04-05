const express = require("express");
const { query, fetchRows } = require("./lib/supabase");
const scheduler = require("./lib/scheduler");
const { listRepos } = require("./lib/repos");

const app = express();
const PORT = process.env.PORT || 3000;
const AUTH_TOKEN = process.env.AUTH_TOKEN;
const startedAt = new Date();

app.use(express.json());

// --- Auth middleware ---

function requireAuth(req, res, next) {
  if (!AUTH_TOKEN) return next();
  const header = req.headers.authorization;
  if (!header || header !== `Bearer ${AUTH_TOKEN}`) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  next();
}

// --- Health ---

app.get("/api/health", (req, res) => {
  const status = scheduler.getStatus();
  res.json({
    status: "ok",
    uptime: Math.round((Date.now() - startedAt.getTime()) / 1000),
    running: status.running,
    queued: status.queued.length,
    tasks: status.tasks.length,
  });
});

// --- Tasks CRUD ---

app.get("/api/tasks", requireAuth, async (req, res) => {
  try {
    const filter = req.query.enabled !== undefined
      ? `&enabled=eq.${req.query.enabled}`
      : "";
    const tasks = await fetchRows(`runner_tasks?order=name.asc${filter}`);
    res.json({ tasks });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/api/tasks", requireAuth, async (req, res) => {
  try {
    const {
      name, description, repo, schedule, branch, commit_to,
      prompt, pre_command, commit_message_template,
      telegram_on_complete, telegram_on_failure,
      enabled, max_runtime_minutes, model, max_turns,
    } = req.body;

    if (!name || !repo || !schedule) {
      return res.status(400).json({ error: "name, repo, and schedule are required" });
    }

    const task = {
      name,
      description: description || null,
      repo,
      schedule,
      branch: branch || "main",
      commit_to: commit_to || branch || "main",
      prompt: prompt || null,
      pre_command: pre_command || null,
      commit_message_template: commit_message_template || null,
      telegram_on_complete: telegram_on_complete !== false,
      telegram_on_failure: telegram_on_failure !== false,
      enabled: enabled !== false,
      max_runtime_minutes: max_runtime_minutes || 30,
      model: model || "sonnet",
      max_turns: max_turns || 50,
    };

    const created = await query("POST", "runner_tasks", task);
    console.log(`[api] Task created: ${name} (${created[0]?.id})`);
    res.json({ task: created[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.patch("/api/tasks/:id", requireAuth, async (req, res) => {
  try {
    const updates = {};
    const allowed = [
      "name", "description", "repo", "schedule", "branch", "commit_to",
      "prompt", "pre_command", "commit_message_template",
      "telegram_on_complete", "telegram_on_failure",
      "enabled", "max_runtime_minutes", "model", "max_turns",
    ];
    for (const key of allowed) {
      if (req.body[key] !== undefined) updates[key] = req.body[key];
    }
    updates.updated_at = new Date().toISOString();

    const result = await query("PATCH", `runner_tasks?id=eq.${req.params.id}`, updates);
    res.json({ task: result?.[0] || { id: req.params.id, ...updates } });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete("/api/tasks/:id", requireAuth, async (req, res) => {
  try {
    await query("DELETE", `runner_tasks?id=eq.${req.params.id}`);
    res.json({ deleted: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// --- Trigger task manually ---

app.post("/api/tasks/:id/trigger", requireAuth, async (req, res) => {
  try {
    const tasks = await fetchRows(`runner_tasks?id=eq.${req.params.id}`);
    if (!tasks.length) {
      return res.status(404).json({ error: "Task not found" });
    }
    const task = tasks[0];
    console.log(`[api] Manual trigger: ${task.name}`);

    // Fire and forget — don't block the HTTP response
    scheduler.triggerTask(task);
    res.json({ triggered: true, task: task.name });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// --- Runs ---

app.get("/api/runs", requireAuth, async (req, res) => {
  try {
    let filter = "runner_runs?order=created_at.desc&limit=50";
    if (req.query.task_id) filter += `&task_id=eq.${req.query.task_id}`;
    if (req.query.status) filter += `&status=eq.${req.query.status}`;
    const runs = await fetchRows(filter);
    res.json({ runs });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/api/runs/:id", requireAuth, async (req, res) => {
  try {
    const runs = await fetchRows(`runner_runs?id=eq.${req.params.id}`);
    if (!runs.length) return res.status(404).json({ error: "Run not found" });
    res.json({ run: runs[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// --- Repos ---

app.get("/api/repos", requireAuth, (req, res) => {
  res.json({ repos: listRepos() });
});

// --- Scheduler status ---

app.get("/api/status", requireAuth, (req, res) => {
  res.json(scheduler.getStatus());
});

// --- Start ---

app.listen(PORT, () => {
  console.log(`[server] Agent runner listening on port ${PORT}`);
  scheduler.start();
});
