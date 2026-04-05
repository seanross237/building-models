const { spawn } = require("child_process");

function runClaude(prompt, repoDir, { model = "sonnet", maxTurns = 50, timeoutMs = 30 * 60 * 1000 } = {}) {
  return new Promise((resolve, reject) => {
    const systemPrompt = [
      "You are running an automated scheduled task. Work autonomously — there is no human to ask questions.",
      "Be thorough but focused. If something is ambiguous, make the safe choice.",
      "When done, provide a concise summary of what you did.",
    ].join("\n");

    const args = [
      "-p",
      prompt,
      "--output-format", "json",
      "--model", model,
      "--dangerously-skip-permissions",
      "--append-system-prompt", systemPrompt,
      "--max-turns", String(maxTurns),
    ];

    const env = { ...process.env };
    delete env.CLAUDECODE;

    const startTime = Date.now();
    const child = spawn("claude", args, {
      cwd: repoDir,
      env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => { stdout += chunk.toString(); });
    child.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error(`Claude timed out after ${Math.round(timeoutMs / 60000)} minutes`));
    }, timeoutMs);

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

module.exports = { runClaude };
