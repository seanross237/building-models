import { Bot } from "grammy";
import { config } from "./config.js";
import { sendMessage, clearSession, cancelActive } from "./claude.js";
import { chunkMessage } from "./formatter.js";
import { saveNote, getSummaryStats } from "./supabase.js";

export function createBot(): Bot {
  const bot = new Bot(config.telegramBotToken);

  // Per-chat request queue: one query at a time, queue the rest
  const queues = new Map<number, Promise<void>>();

  function enqueue(chatId: number, fn: () => Promise<void>): void {
    const prev = queues.get(chatId) ?? Promise.resolve();
    const next = prev.then(fn, fn); // always run even if prev failed
    queues.set(chatId, next);
    next.then(() => {
      // Clean up if this was the last item
      if (queues.get(chatId) === next) queues.delete(chatId);
    });
  }

  // Auth middleware: reject messages not from allowed user
  bot.use(async (ctx, next) => {
    if (ctx.from?.id !== config.allowedUserId) {
      console.log(
        `[bot] Rejected message from user ${ctx.from?.id} (${ctx.from?.username})`
      );
      return; // silently drop
    }
    await next();
  });

  // /start command
  bot.command("start", async (ctx) => {
    await ctx.reply(
      "Serenade Bot ready.\n\n" +
        "Routes:\n" +
        '• "summary" or "summary 6" — site activity stats\n' +
        '• "claude ..." — send to Claude Code\n' +
        "• anything else — saved as a note\n\n" +
        "/reset — start fresh Claude conversation\n" +
        "/cancel — interrupt active Claude query"
    );
  });

  // /reset command — clear session
  bot.command("reset", async (ctx) => {
    clearSession(ctx.chat.id);
    await ctx.reply("Session cleared. Next message starts a fresh conversation.");
  });

  // /cancel command — abort active query
  bot.command("cancel", async (ctx) => {
    const cancelled = cancelActive(ctx.chat.id);
    await ctx.reply(cancelled ? "Cancelling..." : "Nothing active to cancel.");
  });

  // Text message handler with keyword routing
  bot.on("message:text", async (ctx) => {
    const text = ctx.message.text;
    if (!text) return;

    const lowerText = text.trim().toLowerCase();
    const userId = ctx.from?.id ?? 0;
    const chatId = ctx.chat.id;

    // ─── Route 1: Summary / Stats ──────────────────────────────────────
    const summaryMatch = lowerText.match(
      /^(?:summary|\/stats)\s*(\d+)?\s*(hours?)?$/
    );
    if (summaryMatch) {
      let hours = 3;
      if (summaryMatch[1]) {
        hours = Math.min(Math.max(parseInt(summaryMatch[1], 10), 1), 168);
      }

      // Save to inbox (fire-and-forget)
      saveNote(text, userId, chatId);

      enqueue(chatId, async () => {
        try {
          const stats = await getSummaryStats(hours);
          await ctx.reply(stats);
        } catch (err) {
          console.error("[bot] Error fetching summary:", err);
          await ctx.reply("Failed to fetch summary stats.");
        }
      });
      return;
    }

    // ─── Route 2: Claude (message contains "claude") ───────────────────
    if (lowerText.includes("claude")) {
      // Strip first occurrence of "claude" (case-insensitive) and clean up
      const cleanedText = text
        .replace(/claude/i, "")
        .replace(/^\s*[,:\-—]+\s*/, "")
        .trim();

      if (!cleanedText) {
        await ctx.reply("Send a message after 'claude', e.g.: claude what's my latest commit");
        return;
      }

      enqueue(chatId, async () => {
        const typingInterval = setInterval(() => {
          ctx.replyWithChatAction("typing").catch(() => {});
        }, 4000);

        await ctx.replyWithChatAction("typing").catch(() => {});

        try {
          const response = await sendMessage(chatId, cleanedText);
          const chunks = chunkMessage(response);

          for (const chunk of chunks) {
            await ctx.reply(chunk);
          }
        } catch (err) {
          console.error("[bot] Error handling Claude message:", err);
          await ctx.reply("Something went wrong. Try again or /reset.");
        } finally {
          clearInterval(typingInterval);
        }
      });
      return;
    }

    // ─── Route 3: Notes (fallback) ─────────────────────────────────────
    enqueue(chatId, async () => {
      try {
        await saveNote(text, userId, chatId);
        await ctx.reply("📝 Noted.");
      } catch (err) {
        console.error("[bot] Error saving note:", err);
        await ctx.reply("Failed to save note.");
      }
    });
  });

  return bot;
}
