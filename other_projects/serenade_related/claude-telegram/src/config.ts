import { existsSync, readFileSync } from "fs";
import { resolve } from "path";

// Load .env file manually (no dotenv dependency)
const envPath = resolve(import.meta.dirname, "../.env");
if (existsSync(envPath)) {
  for (const line of readFileSync(envPath, "utf-8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIndex = trimmed.indexOf("=");
    if (eqIndex === -1) continue;
    const key = trimmed.slice(0, eqIndex);
    const value = trimmed.slice(eqIndex + 1);
    if (!process.env[key]) process.env[key] = value;
  }
}

function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    console.error(`Missing required env var: ${name}`);
    console.error(`Copy .env.example to .env and fill in the values.`);
    process.exit(1);
  }
  return value;
}

export const config = {
  telegramBotToken: required("TELEGRAM_BOT_TOKEN"),
  allowedUserId: Number(required("TELEGRAM_ALLOWED_USER_ID")),
  claudeWorkingDir:
    process.env.CLAUDE_WORKING_DIR || "/Users/seanross/kingdom_of_god/serenade/serve_boldly",
  claudeModel: process.env.CLAUDE_MODEL || "claude-sonnet-4-6",
  supabaseUrl: required("SUPABASE_URL"),
  supabaseAnonKey: required("SUPABASE_ANON_KEY"),
};
