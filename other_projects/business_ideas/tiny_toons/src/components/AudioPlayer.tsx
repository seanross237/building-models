import { useRef, useState, useEffect } from "react";

interface AudioPlayerProps {
  audioUrl: string;
}

export function AudioPlayer({ audioUrl }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const onTime = () => setCurrentTime(audio.currentTime);
    const onMeta = () => setDuration(audio.duration);
    const onEnd = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", onTime);
    audio.addEventListener("loadedmetadata", onMeta);
    audio.addEventListener("ended", onEnd);
    return () => {
      audio.removeEventListener("timeupdate", onTime);
      audio.removeEventListener("loadedmetadata", onMeta);
      audio.removeEventListener("ended", onEnd);
    };
  }, [audioUrl]);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const restart = () => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.currentTime = 0;
    audio.play();
    setIsPlaying(true);
  };

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  // Generate random bar heights for the waveform visual
  const bars = Array.from({ length: 35 }, (_, i) => {
    const center = 17;
    const dist = Math.abs(i - center) / center;
    const base = 12 + (1 - dist) * 28;
    const wobble = Math.sin(i * 1.7) * 8;
    return Math.max(8, base + wobble);
  });

  return (
    <div className="mx-5 mb-4">
      <audio ref={audioRef} src={audioUrl} preload="metadata" />

      <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-5 shadow-sm border-2 border-purple-100">
        <div className="text-xs font-bold uppercase tracking-wider text-purple-500 mb-3">
          Your Song is Ready!
        </div>

        {/* Waveform */}
        <div className="relative h-14 rounded-xl overflow-hidden mb-2 flex items-center justify-center gap-[2px] px-2 bg-gradient-to-r from-purple-50 via-pink-50 to-purple-50">
          {bars.map((height, i) => {
            const barPosition = (i / bars.length) * 100;
            const isPlayed = barPosition < progress;
            return (
              <div
                key={i}
                className={`w-[3px] rounded-full transition-colors duration-150 ${
                  isPlayed
                    ? "bg-gradient-to-t from-purple-500 to-pink-400"
                    : "bg-purple-200/60"
                }`}
                style={{ height: `${height}px` }}
              />
            );
          })}
        </div>

        {/* Time labels */}
        <div className="flex justify-between text-xs text-purple-300 mb-4 px-1">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>

        {/* Controls */}
        <div className="flex justify-center items-center gap-6">
          <button
            onClick={restart}
            className="w-11 h-11 rounded-full bg-purple-50 border-2 border-purple-100 flex items-center justify-center text-purple-400 hover:bg-purple-100 transition-colors"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M1 4v6h6" />
              <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
            </svg>
          </button>

          <button
            onClick={togglePlay}
            className="w-14 h-14 rounded-full bg-gradient-to-br from-purple-500 to-pink-400 shadow-lg shadow-purple-300/40 flex items-center justify-center text-white hover:shadow-xl transition-shadow"
          >
            {isPlaying ? (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                <rect x="6" y="4" width="4" height="16" rx="1" />
                <rect x="14" y="4" width="4" height="16" rx="1" />
              </svg>
            ) : (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="6,3 20,12 6,21" />
              </svg>
            )}
          </button>

          <div className="w-11 h-11" /> {/* Spacer for symmetry */}
        </div>
      </div>
    </div>
  );
}
