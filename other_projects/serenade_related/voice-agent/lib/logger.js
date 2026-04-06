const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

/**
 * Log an agent interaction to Supabase.
 * Fire-and-forget — never throws or blocks the response.
 */
async function logInteraction(question, claudeResult) {
  if (!SUPABASE_URL || !SUPABASE_KEY) {
    console.log("[logger] Supabase not configured, skipping log");
    return;
  }

  try {
    const fullOutput = claudeResult.fullOutput || {};

    // Extract tool call summary from the full output
    let toolCallsSummary = null;
    if (fullOutput.num_turns > 0) {
      toolCallsSummary = {
        num_turns: fullOutput.num_turns || 0,
        stop_reason: fullOutput.stop_reason || null,
        cost_usd: fullOutput.total_cost_usd || 0,
        model: fullOutput.model || null,
      };
    }

    const row = {
      question,
      session_id: claudeResult.sessionId,
      result: claudeResult.result,
      full_output: fullOutput,
      duration_ms: claudeResult.durationMs,
      stop_reason: fullOutput.stop_reason || null,
      num_turns: fullOutput.num_turns || null,
      tool_calls_summary: toolCallsSummary,
    };

    const res = await fetch(`${SUPABASE_URL}/rest/v1/agent_logs`, {
      method: "POST",
      headers: {
        apikey: SUPABASE_KEY,
        Authorization: `Bearer ${SUPABASE_KEY}`,
        "Content-Type": "application/json",
        Prefer: "return=minimal",
      },
      body: JSON.stringify(row),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error(`[logger] Failed to log: ${res.status} ${err}`);
    } else {
      console.log(`[logger] Logged interaction (${claudeResult.durationMs}ms)`);
    }
  } catch (err) {
    console.error(`[logger] Error: ${err.message}`);
  }
}

module.exports = { logInteraction };
