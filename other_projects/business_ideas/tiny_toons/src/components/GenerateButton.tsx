import { useState, useEffect } from "react";

interface GenerateButtonProps {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
}

const LOADING_MESSAGES = [
  "Warming up the studio...",
  "Writing the melody...",
  "Adding the beat...",
  "Mixing it together...",
  "Almost there...",
];

export function GenerateButton({ onClick, disabled, loading }: GenerateButtonProps) {
  const [elapsed, setElapsed] = useState(0);
  const [msgIndex, setMsgIndex] = useState(0);

  useEffect(() => {
    if (!loading) {
      setElapsed(0);
      setMsgIndex(0);
      return;
    }
    const timer = setInterval(() => setElapsed((t) => t + 1), 1000);
    return () => clearInterval(timer);
  }, [loading]);

  useEffect(() => {
    if (!loading) return;
    // Cycle through messages every 8 seconds
    const idx = Math.min(Math.floor(elapsed / 8), LOADING_MESSAGES.length - 1);
    setMsgIndex(idx);
  }, [elapsed, loading]);

  const formatTime = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  return (
    <div className="mx-5 mb-5">
      {loading ? (
        <div className="w-full rounded-2xl bg-white/80 backdrop-blur-sm border-2 border-purple-100 p-5 shadow-sm">
          {/* Animated dots */}
          <div className="flex justify-center gap-2 mb-4">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="w-3 h-3 rounded-full bg-gradient-to-r from-purple-400 to-pink-400 animate-bounce"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </div>

          {/* Message */}
          <p className="text-center text-purple-600 font-semibold text-base mb-1">
            {LOADING_MESSAGES[msgIndex]}
          </p>

          {/* Timer */}
          <p className="text-center text-purple-300 text-xs font-mono">
            {formatTime(elapsed)}
          </p>

          {/* Hint after 15s */}
          {elapsed >= 15 && (
            <p className="text-center text-purple-300 text-xs mt-3">
              First song takes a bit longer — hang tight!
            </p>
          )}
        </div>
      ) : (
        <button
          onClick={onClick}
          disabled={disabled}
          className="w-full py-4 rounded-2xl text-white font-bold text-lg tracking-wide bg-gradient-to-r from-purple-500 via-pink-400 to-purple-500 shadow-lg shadow-purple-300/40 hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
        >
          Generate My Song
        </button>
      )}
    </div>
  );
}
