import { config } from "./config.js";
import { createBot } from "./bot.js";

console.log("[telegram-bot] Starting...");
console.log(`[telegram-bot] Working dir: ${config.claudeWorkingDir}`);
console.log(`[telegram-bot] Model: ${config.claudeModel}`);
console.log(`[telegram-bot] Allowed user: ${config.allowedUserId}`);

const bot = createBot();

// Graceful shutdown
function shutdown(signal: string) {
  console.log(`[telegram-bot] ${signal} received, shutting down...`);
  bot.stop();
  process.exit(0);
}
process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));

bot.start({
  onStart: () => console.log("[telegram-bot] Bot is running."),
});
