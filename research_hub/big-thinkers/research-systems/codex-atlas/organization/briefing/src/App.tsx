import { useState, useEffect } from "react";
import {
  Heart,
  Mountain,
  Clock,
  Presentation,
  FolderTree,
  ArrowLeft,
} from "lucide-react";
import { DevotionStage } from "@/stages/DevotionStage";
import { MeditationStage } from "@/stages/MeditationStage";
import { TimelineStage } from "@/stages/TimelineStage";
import { PresentationStage } from "@/stages/PresentationStage";
import { FileStructure } from "@/stages/FileStructure";

const SECTIONS = [
  {
    id: "devotion",
    name: "Devotion",
    desc: "Scripture & reflection",
    icon: Heart,
    color: "#f43f5e",
    gradient: "from-rose-900/40 via-slate-950 to-slate-950",
  },
  {
    id: "meditation",
    name: "Meditation",
    desc: "Be still",
    icon: Mountain,
    color: "#3b82f6",
    gradient: "from-blue-900/40 via-slate-950 to-slate-950",
  },
  {
    id: "timeline",
    name: "Timeline",
    desc: "Work history",
    icon: Clock,
    color: "#10b981",
    gradient: "from-emerald-900/40 via-slate-950 to-slate-950",
  },
  {
    id: "presentation",
    name: "Presentation",
    desc: "The system so far",
    icon: Presentation,
    color: "#8b5cf6",
    gradient: "from-violet-900/40 via-slate-950 to-slate-950",
  },
  {
    id: "files",
    name: "File Structure",
    desc: "/science directory",
    icon: FolderTree,
    color: "#06b6d4",
    gradient: "from-cyan-900/40 via-slate-950 to-slate-950",
  },
];

function Hub({ onSelect }: { onSelect: (id: string) => void }) {
  return (
    <div className="fixed inset-0 bg-gradient-to-b from-slate-900 via-slate-950 to-black flex flex-col items-center justify-center animate-fade-in">
      <h1 className="text-2xl font-bold text-white/90 mb-1">
        Science Briefing
      </h1>
      <p className="text-sm text-slate-500 mb-10">
        Pick a section
      </p>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 max-w-lg px-6">
        {SECTIONS.map((s) => {
          const Icon = s.icon;
          return (
            <button
              key={s.id}
              onClick={() => onSelect(s.id)}
              className="group flex flex-col items-center gap-2.5 px-5 py-5 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.07] hover:border-white/[0.12] transition-all duration-200"
            >
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110"
                style={{ background: `${s.color}15`, border: `1px solid ${s.color}30` }}
              >
                <Icon className="w-5 h-5" style={{ color: s.color }} />
              </div>
              <div>
                <div className="text-sm font-semibold text-white/80 group-hover:text-white transition-colors">
                  {s.name}
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">
                  {s.desc}
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function StageWrapper({
  id,
  onBack,
  arrowKeyBack = false,
  children,
}: {
  id: string;
  onBack: () => void;
  arrowKeyBack?: boolean;
  children: React.ReactNode;
}) {
  const section = SECTIONS.find((s) => s.id === id);
  const gradient = section?.gradient || "from-slate-900 via-slate-950 to-slate-950";

  useEffect(() => {
    if (!arrowKeyBack) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") {
        onBack();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onBack, arrowKeyBack]);

  return (
    <div className={`fixed inset-0 bg-gradient-to-b ${gradient} flex flex-col`}>
      <div className="shrink-0 px-5 pt-5">
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white/[0.06] border border-white/[0.1] text-sm text-slate-300 hover:text-white hover:bg-white/[0.1] transition-all duration-200"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>
      </div>
      <div className="flex-1 flex items-center justify-center overflow-hidden">
        {children}
      </div>
    </div>
  );
}

export default function App() {
  const [view, setView] = useState<string | null>(null);

  if (!view) return <Hub onSelect={setView} />;

  const back = () => setView(null);

  return (
    <StageWrapper id={view} onBack={back} arrowKeyBack={!["timeline", "presentation"].includes(view)}>
      {view === "devotion" && <DevotionStage onNext={back} />}
      {view === "meditation" && <MeditationStage onNext={back} />}
      {view === "timeline" && <TimelineStage onNext={back} />}
      {view === "presentation" && <PresentationStage onNext={back} />}
      {view === "files" && <FileStructure />}
    </StageWrapper>
  );
}
