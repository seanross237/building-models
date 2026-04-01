import { Mountain, ArrowRight } from "lucide-react";

const meditation = {
  youtubeId: "inpok4MKVLM",
  title: "5-Minute Meditation You Can Do Anywhere",
  channel: "Goodful",
};

export function MeditationStage({ onNext }: { onNext: () => void }) {
  return (
    <div className="max-w-2xl w-full mx-auto px-6 py-8 overflow-y-auto max-h-[85vh] animate-fade-in">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center">
            <Mountain className="w-7 h-7 text-blue-400" />
          </div>
        </div>
        <div className="text-sm uppercase tracking-[0.3em] text-slate-500 mb-2 font-mono">
          Be Still
        </div>
        <h1 className="text-3xl font-bold text-blue-400 mb-2">
          Daily Meditation
        </h1>
      </div>

      {/* YouTube embed */}
      <div className="mb-6 rounded-2xl overflow-hidden border border-slate-700/50">
        <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
          <iframe
            className="absolute inset-0 w-full h-full"
            src={`https://www.youtube.com/embed/${meditation.youtubeId}`}
            title={meditation.title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      </div>

      {/* Video info */}
      <div className="mb-8 text-center">
        <h3 className="text-white/90 font-medium text-lg">
          {meditation.title}
        </h3>
        <p className="text-sm text-slate-500 mt-1">{meditation.channel}</p>
      </div>

      {/* Next */}
      <div className="flex justify-center">
        <button
          onClick={onNext}
          className="flex items-center gap-2 px-8 py-3 rounded-xl bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-all duration-300 font-medium"
        >
          Next Stage <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
