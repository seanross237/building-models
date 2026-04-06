import { createClient } from "@supabase/supabase-js";
import { config } from "./config.js";

const supabase = createClient(config.supabaseUrl, config.supabaseAnonKey);

/** Save a note to telegram_inbox */
export async function saveNote(
  text: string,
  fromUserId: number,
  chatId: number
): Promise<void> {
  const { error } = await supabase.from("telegram_inbox").insert({
    message_text: text,
    from_user_id: fromUserId,
    chat_id: chatId,
  });
  if (error) {
    console.error("[supabase] Failed to save note:", error.message);
  }
}

function formatCents(cents: number): string {
  if (!cents) return "$0";
  return "$" + (cents / 100).toFixed(cents % 100 === 0 ? 0 : 2);
}

/** Fetch summary stats and format as a Telegram message */
export async function getSummaryStats(hours: number): Promise<string> {
  const { data, error } = await supabase.rpc("get_summary_stats_fast", {
    _hours: hours,
  });

  if (error) {
    return `❌ Error fetching stats: ${error.message}`;
  }

  let msg = `📊 Last ${hours} Hour${hours > 1 ? "s" : ""} Summary\n\n`;

  msg += `ACTIVITY\n`;
  msg += `• Forms: ${data.forms || 0}\n`;
  msg += `• Lyrics: ${data.lyrics || 0}\n`;
  msg += `• Songs: ${data.songs || 0}\n\n`;

  msg += `PAYMENTS\n`;
  msg += `• Unlocks: ${data.payments_total || 0} (${data.payments_paid || 0} paid, ${data.payments_free || 0} free)\n`;
  msg += `• Revenue: ${formatCents(data.revenue_cents)}`;
  if (data.payments_paid > 0) {
    const avg = Math.round(data.revenue_cents / data.payments_paid);
    msg += ` (${formatCents(avg)} avg, ${formatCents(data.max_payment_cents)} max)`;
  }
  msg += `\n`;

  return msg;
}
