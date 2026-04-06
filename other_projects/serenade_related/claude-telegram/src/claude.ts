import { query, AbortError } from "@anthropic-ai/claude-agent-sdk";
import { config } from "./config.js";

// Strip env vars that prevent nested Claude Code sessions
const cleanEnv = { ...process.env };
delete cleanEnv.CLAUDECODE;

// Track session IDs per Telegram chat for conversation continuity
const sessions = new Map<number, string>();

// Track active AbortControllers per chat for cancellation
const activeControllers = new Map<number, AbortController>();

export function clearSession(chatId: number): void {
  sessions.delete(chatId);
}

export function cancelActive(chatId: number): boolean {
  const controller = activeControllers.get(chatId);
  if (controller) {
    controller.abort();
    activeControllers.delete(chatId);
    return true;
  }
  return false;
}

export async function sendMessage(
  chatId: number,
  prompt: string
): Promise<string> {
  const abortController = new AbortController();
  activeControllers.set(chatId, abortController);

  try {
    const sessionId = sessions.get(chatId);

    const conversation = query({
      prompt,
      options: {
        abortController,
        cwd: config.claudeWorkingDir,
        model: config.claudeModel,
        permissionMode: "bypassPermissions",
        allowDangerouslySkipPermissions: true,
        systemPrompt: { type: "preset", preset: "claude_code" },
        settingSources: ["user", "project", "local"],
        env: cleanEnv,
        ...(sessionId ? { resume: sessionId } : {}),
      },
    });

    let resultText = "";
    let capturedSessionId: string | null = null;

    for await (const message of conversation) {
      // Capture session ID from any message
      if ("session_id" in message && message.session_id && !capturedSessionId) {
        capturedSessionId = message.session_id;
      }

      if (message.type === "assistant" && message.message?.content) {
        for (const block of message.message.content) {
          if ("text" in block && block.text) {
            resultText += block.text + "\n";
          }
        }
      }

      if (message.type === "result") {
        if (message.subtype === "success" && "result" in message) {
          // Use the result text if we didn't collect assistant text
          if (!resultText.trim()) {
            resultText = (message as any).result || "Done (no text output).";
          }
        } else if ("errors" in message) {
          const errors = (message as any).errors as string[];
          resultText =
            resultText.trim() ||
            `Error: ${errors.join(", ") || "Unknown error"}`;
        }
      }
    }

    // Save session ID for continuity
    if (capturedSessionId) {
      sessions.set(chatId, capturedSessionId);
    }

    return resultText.trim() || "Done (no text output).";
  } catch (err: any) {
    if (err instanceof AbortError || abortController.signal.aborted) {
      return "Cancelled.";
    }
    console.error("[claude] Error:", err);
    return `Error: ${err.message || "Unknown error"}`;
  } finally {
    activeControllers.delete(chatId);
  }
}
