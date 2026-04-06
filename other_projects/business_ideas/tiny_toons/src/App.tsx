import { useState, useCallback } from "react";
import { MessageInput } from "./components/MessageInput";
import { StylePicker } from "./components/StylePicker";
import { GenerateButton } from "./components/GenerateButton";
import { AudioPlayer } from "./components/AudioPlayer";
import { ActionButtons } from "./components/ActionButtons";
import { MusicNotes } from "./components/MusicNotes";
import { generateSong } from "./lib/api";

type AppState = "compose" | "generating" | "ready";

function App() {
  const [message, setMessage] = useState("");
  const [style, setStyle] = useState("Pop");
  const [state, setState] = useState<AppState>("compose");
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const canGenerate = message.trim().length > 0 && style.length > 0;

  const handleGenerate = useCallback(async () => {
    if (!canGenerate) return;
    setState("generating");
    setError(null);

    try {
      const result = await generateSong({ message: message.trim(), style });
      setAudioUrl(result.audioUrl);
      setState("ready");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setState("compose");
    }
  }, [message, style, canGenerate]);

  const handleRegenerate = useCallback(() => {
    setAudioUrl(null);
    setState("compose");
    // Auto-trigger generation again
    setTimeout(() => handleGenerate(), 100);
  }, [handleGenerate]);

  const handleShare = useCallback(async () => {
    if (!audioUrl) return;

    // Try native share API first (works great on mobile browsers)
    if (navigator.share) {
      try {
        const response = await fetch(audioUrl);
        const blob = await response.blob();
        const file = new File([blob], "tiny-toon.mp3", { type: "audio/mpeg" });
        await navigator.share({
          title: "Check out this song I made!",
          text: `I turned my message into a song with Tiny Toons`,
          files: [file],
        });
        return;
      } catch {
        // Fall through to clipboard
      }
    }

    // Fallback: copy link
    try {
      await navigator.clipboard.writeText(audioUrl);
      alert("Link copied to clipboard!");
    } catch {
      // Last resort: open in new tab
      window.open(audioUrl, "_blank");
    }
  }, [audioUrl]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-100 via-pink-50 to-purple-100 relative">
      <MusicNotes />

      <div className="relative z-10 max-w-md mx-auto">
        {/* Header */}
        <div className="text-center pt-12 pb-6 px-6">
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-purple-500 via-pink-400 to-amber-400 bg-clip-text text-transparent">
            Tiny Toons
          </h1>
          <p className="text-purple-400 text-sm mt-1 font-medium">
            Turn your message into a song
          </p>
        </div>

        {/* Message Input */}
        <MessageInput
          value={message}
          onChange={setMessage}
          disabled={state === "generating"}
        />

        {/* Style Picker */}
        <StylePicker
          value={style}
          onChange={setStyle}
          disabled={state === "generating"}
        />

        {/* Generate Button */}
        {state !== "ready" && (
          <GenerateButton
            onClick={handleGenerate}
            disabled={!canGenerate}
            loading={state === "generating"}
          />
        )}

        {/* Error */}
        {error && (
          <div className="mx-5 mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-500 text-sm text-center font-medium">
            {error}
          </div>
        )}

        {/* Player + Actions (shown when song is ready) */}
        {state === "ready" && audioUrl && (
          <>
            <AudioPlayer audioUrl={audioUrl} />
            <ActionButtons
              onRegenerate={handleRegenerate}
              onShare={handleShare}
            />
          </>
        )}
      </div>
    </div>
  );
}

export default App;
