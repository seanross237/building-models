const cronParser = require("cron-parser");
const { fetchRows } = require("./supabase");
const { executeTask } = require("./executor");

let tasks = [];         // loaded from Supabase
let runQueue = [];      // tasks ready to execute
let running = null;     // currently executing task
let tickInterval = null;
let refreshInterval = null;

function computeNextRun(schedule) {
  try {
    const interval = cronParser.parseExpression(schedule, { utc: true });
    return interval.next().toDate();
  } catch (err) {
    console.error(`[scheduler] Invalid cron "${schedule}": ${err.message}`);
    return null;
  }
}

async function refreshTasks() {
  try {
    const rows = await fetchRows("runner_tasks?enabled=eq.true&order=name.asc");
    tasks = rows.map(task => ({
      ...task,
      _nextRun: computeNextRun(task.schedule),
    })).filter(t => t._nextRun !== null);
    console.log(`[scheduler] Loaded ${tasks.length} enabled tasks`);
    for (const t of tasks) {
      console.log(`[scheduler]   ${t.name}: next run at ${t._nextRun.toISOString()}`);
    }
  } catch (err) {
    console.error(`[scheduler] Failed to refresh tasks: ${err.message}`);
  }
}

async function tick() {
  const now = new Date();

  // Check which tasks are due
  for (const task of tasks) {
    if (!task._nextRun) continue;
    if (task._nextRun <= now) {
      // Avoid double-queuing
      const alreadyQueued = runQueue.some(t => t.id === task.id);
      const alreadyRunning = running?.id === task.id;
      if (!alreadyQueued && !alreadyRunning) {
        console.log(`[scheduler] Task "${task.name}" is due, queuing`);
        runQueue.push({ ...task });
      }
      // Advance to next run time
      task._nextRun = computeNextRun(task.schedule);
    }
  }

  // Execute next in queue if nothing running
  if (!running && runQueue.length > 0) {
    const task = runQueue.shift();
    running = task;
    try {
      await executeTask(task);
    } catch (err) {
      // Error already logged and stored by executor
    } finally {
      running = null;
      // Check again immediately in case more tasks are queued
      setImmediate(tick);
    }
  }
}

function start() {
  const { isConfigured } = require("./supabase");
  if (!isConfigured()) {
    console.log("[scheduler] Supabase not configured, scheduler disabled");
    return;
  }

  console.log("[scheduler] Starting...");

  // Load tasks immediately, then refresh every 5 minutes
  refreshTasks();
  refreshInterval = setInterval(refreshTasks, 5 * 60 * 1000);

  // Check for due tasks every 30 seconds
  tickInterval = setInterval(tick, 30 * 1000);
  // Also check after initial load
  setTimeout(tick, 5000);
}

function getStatus() {
  return {
    running: running ? { id: running.id, name: running.name } : null,
    queued: runQueue.map(t => ({ id: t.id, name: t.name })),
    tasks: tasks.map(t => ({
      id: t.id,
      name: t.name,
      nextRun: t._nextRun?.toISOString(),
    })),
  };
}

// Trigger a task manually (bypasses schedule)
async function triggerTask(task) {
  task._trigger = "manual";
  if (running) {
    console.log(`[scheduler] Queuing manual trigger for "${task.name}" (another task is running)`);
    runQueue.push(task);
  } else {
    running = task;
    try {
      await executeTask(task);
    } catch (err) {
      // Already handled
    } finally {
      running = null;
      setImmediate(tick);
    }
  }
}

module.exports = { start, getStatus, triggerTask };
