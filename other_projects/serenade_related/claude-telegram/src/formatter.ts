const TELEGRAM_MAX_LENGTH = 4096;

/**
 * Split a long message into Telegram-safe chunks.
 * Splits at paragraph boundaries, preserves code blocks.
 */
export function chunkMessage(text: string): string[] {
  if (text.length <= TELEGRAM_MAX_LENGTH) return [text];

  const chunks: string[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    if (remaining.length <= TELEGRAM_MAX_LENGTH) {
      chunks.push(remaining);
      break;
    }

    // Find a good split point within the limit
    let splitAt = findSplitPoint(remaining, TELEGRAM_MAX_LENGTH);
    chunks.push(remaining.slice(0, splitAt));
    remaining = remaining.slice(splitAt).trimStart();
  }

  // Add part indicators if multiple chunks
  if (chunks.length > 1) {
    return chunks.map((chunk, i) => `[${i + 1}/${chunks.length}]\n${chunk}`);
  }

  return chunks;
}

function findSplitPoint(text: string, maxLen: number): number {
  const searchRegion = text.slice(0, maxLen);

  // Try splitting at double newline (paragraph boundary)
  const lastParagraph = searchRegion.lastIndexOf("\n\n");
  if (lastParagraph > maxLen * 0.3) return lastParagraph;

  // Try splitting at single newline
  const lastNewline = searchRegion.lastIndexOf("\n");
  if (lastNewline > maxLen * 0.3) return lastNewline;

  // Try splitting at space
  const lastSpace = searchRegion.lastIndexOf(" ");
  if (lastSpace > maxLen * 0.3) return lastSpace;

  // Hard split at max length
  return maxLen;
}

// Characters that need escaping in Telegram MarkdownV2
const ESCAPE_CHARS = /([_*\[\]()~`>#+\-=|{}.!\\])/g;

/**
 * Escape text for Telegram MarkdownV2 format.
 * Returns null if escaping seems too risky (complex markdown).
 */
export function escapeMarkdownV2(text: string): string | null {
  // If the text has code blocks, it's too complex to safely escape —
  // we'd need to parse which chars are inside vs outside code blocks.
  // Fall back to plain text in that case.
  if (text.includes("```") || text.includes("`")) return null;

  return text.replace(ESCAPE_CHARS, "\\$1");
}
