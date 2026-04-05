const { execSync } = require("child_process");
const { ensureRepo, checkoutBranch, commitAndPush, getRepoDir } = require("./repos");
const { runClaude } = require("./claude");
const { query } = require("./supabase");
const telegram = require("./telegram");

async function executeTask(task) {
  const startTime = Date.now();
  const dateStr = new Date().toISOString().split("T")[0];

  // Create run record
  const runs = await query("POST", "runner_runs", {
    task_id: task.id,
    task_name: task.name,
    status: "running",
    trigger: task._trigger || "schedule",
    started_at: new Date().toISOString(),
  });
  const run = runs[0];
  console.log(`[executor] Starting task "${task.name}" (run ${run.id})`);

  try {
    // 1. Clone/update repo
    const repoDir = ensureRepo(task.repo);
    const branch = task.branch || "main";
    checkoutBranch(repoDir, branch);

    let preCommandOutput = null;
    let claudeSummary = null;
    let claudeCost = null;
    let claudeTurns = null;
    let claudeModel = null;

    // 2. Run pre_command if specified
    if (task.pre_command) {
      console.log(`[executor] Running pre_command: ${task.pre_command}`);
      try {
        const timeoutMs = (task.max_runtime_minutes || 30) * 60 * 1000;
        preCommandOutput = execSync(task.pre_command, {
          cwd: repoDir,
          timeout: timeoutMs,
          shell: true,
          env: { ...process.env, HOME: process.env.HOME || "/home/agent" },
        }).toString();
        console.log(`[executor] pre_command output:\n${preCommandOutput.slice(0, 500)}`);
      } catch (err) {
        const output = err.stdout?.toString() || err.stderr?.toString() || err.message;
        throw new Error(`pre_command failed: ${output.slice(0, 500)}`);
      }
    }

    // 3. Run Claude if prompt specified
    if (task.prompt) {
      console.log(`[executor] Running Claude (model: ${task.model || "sonnet"})...`);
      const timeoutMs = (task.max_runtime_minutes || 30) * 60 * 1000;
      const result = await runClaude(task.prompt, repoDir, {
        model: task.model || "sonnet",
        maxTurns: task.max_turns || 50,
        timeoutMs,
      });
      claudeSummary = result.result?.slice(0, 2000);
      claudeCost = result.costUsd;
      claudeTurns = result.numTurns;
      claudeModel = result.model;
      console.log(`[executor] Claude done in ${Math.round(result.durationMs / 1000)}s`);
    }

    // 4. Commit and push if there are changes
    const commitTo = task.commit_to || branch;
    const commitMsg = (task.commit_message_template || `agent-runner: ${task.name} {date}`)
      .replace("{date}", dateStr);
    const sha = commitAndPush(repoDir, commitMsg, commitTo);

    // 5. Mark completed
    const durationMs = Date.now() - startTime;
    await query("PATCH", `runner_runs?id=eq.${run.id}`, {
      status: "completed",
      completed_at: new Date().toISOString(),
      pre_command_output: preCommandOutput?.slice(0, 5000),
      claude_summary: claudeSummary,
      commit_sha: sha,
      duration_ms: durationMs,
      claude_cost_usd: claudeCost,
      claude_num_turns: claudeTurns,
      claude_model: claudeModel,
    });

    console.log(`[executor] Task "${task.name}" completed in ${Math.round(durationMs / 1000)}s`);

    // 6. Telegram notification
    if (task.telegram_on_complete) {
      const costStr = claudeCost ? ` ($${claudeCost.toFixed(2)})` : "";
      const shaStr = sha ? `\nCommit: ${sha}` : "\nNo changes to commit";
      telegram.send(
        `Agent Runner: ${task.name}\n` +
        `Duration: ${Math.round(durationMs / 1000)}s${costStr}${shaStr}\n` +
        `${claudeSummary ? `Summary: ${claudeSummary.slice(0, 200)}` : preCommandOutput ? `Output: ${preCommandOutput.slice(0, 200)}` : "Done"}`
      );
    }

    return run;
  } catch (err) {
    const durationMs = Date.now() - startTime;
    console.error(`[executor] Task "${task.name}" failed: ${err.message}`);

    await query("PATCH", `runner_runs?id=eq.${run.id}`, {
      status: "failed",
      completed_at: new Date().toISOString(),
      error: err.message.slice(0, 2000),
      duration_ms: durationMs,
    });

    if (task.telegram_on_failure !== false) {
      telegram.send(
        `Agent Runner FAILED: ${task.name}\n` +
        `Error: ${err.message.slice(0, 300)}`
      );
    }

    throw err;
  }
}

module.exports = { executeTask };
