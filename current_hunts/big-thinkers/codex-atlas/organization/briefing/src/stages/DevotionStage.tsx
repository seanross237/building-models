import { Heart, ArrowRight } from "lucide-react";
import { devotion } from "@/data/devotion";

export function DevotionStage({ onNext }: { onNext: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full max-w-xl mx-auto px-6 animate-fade-in">
      <Heart className="w-8 h-8 text-rose-400/60 mb-4" />
      <div className="text-sm text-rose-300/50 uppercase tracking-widest mb-10 font-mono">
        Center Yourself
      </div>

      {/* Scripture */}
      <div className="text-center mb-10">
        <p className="text-2xl sm:text-3xl font-bold text-white/90 leading-snug mb-4">
          "{devotion.scripture.text}"
        </p>
        <p className="text-sm text-rose-300/60 font-medium tracking-wide">
          {devotion.scripture.reference}
        </p>
      </div>

      {/* Reflection */}
      <div className="mb-12 p-5 rounded-2xl bg-rose-500/5 border border-rose-500/15 text-rose-200/70 text-sm leading-relaxed max-w-md text-center">
        {devotion.reflection}
      </div>

      <button
        onClick={onNext}
        className="flex items-center gap-2 px-8 py-3.5 rounded-xl bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-all duration-300"
      >
        Continue <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  );
}
