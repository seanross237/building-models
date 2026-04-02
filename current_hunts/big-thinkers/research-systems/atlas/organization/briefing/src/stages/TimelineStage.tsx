import { useState, useRef, useEffect } from "react";
import {
  ArrowRight,
  CheckCircle2,
  XCircle,
  Flag,
  AlertTriangle,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import { timeline, type TimelineEntry } from "@/data/timeline";

const statusConfig = {
  completed: { icon: CheckCircle2, color: "#10b981", label: "Completed" },
  failed: { icon: XCircle, color: "#ef4444", label: "Failed" },
  milestone: { icon: Flag, color: "#a855f7", label: "Milestone" },
  mixed: { icon: AlertTriangle, color: "#f59e0b", label: "Mixed" },
};

const DOT_COLORS = [
  "#3b82f6", "#f43f5e", "#f59e0b", "#14b8a6", "#a855f7",
  "#f97316", "#06b6d4", "#ec4899", "#84cc16", "#6366f1",
];

function CardContent({ entry, index }: { entry: TimelineEntry; index: number }) {
  const [expanded, setExpanded] = useState(false);
  const status = statusConfig[entry.status];
  const StatusIcon = status.icon;
  const previewCount = 3;
  const previewBullets = entry.bullets.slice(0, previewCount);
  const restBullets = entry.bullets.slice(previewCount);
  const hasMore = restBullets.length > 0;

  return (
    <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] px-3 py-2.5 text-xs w-full backdrop-blur-sm">
      {/* Title + status */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <h3 className="text-[11px] font-semibold text-white/90 leading-tight">
          {entry.title}
        </h3>
        <span
          className="flex items-center gap-1 shrink-0 text-[9px] font-medium px-1.5 py-0.5 rounded-full"
          style={{
            background: `${status.color}15`,
            color: status.color,
          }}
        >
          <StatusIcon className="w-2.5 h-2.5" />
          {status.label}
        </span>
      </div>

      {/* Bullets */}
      <ul className="space-y-0.5 mb-1.5">
        {previewBullets.map((b, i) => (
          <li key={i} className="text-[10px] text-slate-400 leading-snug flex gap-1.5">
            <span className="shrink-0 mt-0.5" style={{ color: DOT_COLORS[index % DOT_COLORS.length] }}>
              &bull;
            </span>
            <span>{b}</span>
          </li>
        ))}
      </ul>

      {expanded && (
        <>
          <ul className="space-y-0.5 mb-1.5">
            {restBullets.map((b, i) => (
              <li key={i} className="text-[10px] text-slate-400 leading-snug flex gap-1.5">
                <span className="shrink-0 mt-0.5" style={{ color: DOT_COLORS[index % DOT_COLORS.length] }}>
                  &bull;
                </span>
                <span>{b}</span>
              </li>
            ))}
          </ul>

          {/* Stats */}
          {entry.stats && (
            <div className="flex flex-wrap gap-1.5 mb-1.5">
              {entry.stats.map((stat) => (
                <div
                  key={stat.label}
                  className="bg-white/[0.04] border border-white/[0.06] rounded-lg px-2 py-1 text-center"
                >
                  <div className="text-[10px] font-bold" style={{ color: stat.color }}>
                    {stat.value}
                  </div>
                  <div className="text-[8px] text-slate-600">{stat.label}</div>
                </div>
              ))}
            </div>
          )}

          {/* Methodology */}
          <div
            className="rounded-lg p-2 mt-1"
            style={{ background: `${DOT_COLORS[index % DOT_COLORS.length]}08`, border: `1px solid ${DOT_COLORS[index % DOT_COLORS.length]}18` }}
          >
            <div className="text-[8px] font-medium uppercase tracking-wider mb-0.5" style={{ color: DOT_COLORS[index % DOT_COLORS.length] }}>
              Methodology
            </div>
            <p className="text-[10px] text-slate-400 leading-relaxed">
              {entry.methodology}
            </p>
          </div>
        </>
      )}

      {(hasMore || entry.stats || entry.methodology) && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-1 flex items-center gap-0.5 text-[9px] text-slate-600 hover:text-slate-400 transition-colors"
        >
          {expanded ? (
            <><ChevronDown className="w-2.5 h-2.5" /> less</>
          ) : (
            <><ChevronRight className="w-2.5 h-2.5" /> more</>
          )}
        </button>
      )}
    </div>
  );
}

export function TimelineStage({ onNext }: { onNext: () => void }) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const colW = 220;
  const gap = 16;

  // Auto-scroll to the right (most recent) on load
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = scrollRef.current.scrollWidth;
    }
  }, []);

  return (
    <div className="w-full flex flex-col h-full max-h-[85vh] animate-fade-in">
      {/* Header */}
      <div className="text-center mb-4 shrink-0">
        <div className="text-sm text-emerald-300/50 uppercase tracking-widest mb-1 font-mono">
          Work Timeline
        </div>
        <p className="text-xs text-slate-500">
          {timeline.length} entries &middot; scroll to explore
        </p>
      </div>

      {/* Horizontal timeline */}
      <div ref={scrollRef} className="flex-1 overflow-x-auto px-6 pb-4">
        <div
          className="grid"
          style={{
            gridTemplateColumns: `repeat(${timeline.length}, ${colW}px)`,
            gridTemplateRows: "1fr auto 1fr",
            gap: `0 ${gap}px`,
            minWidth: timeline.length * (colW + gap),
          }}
        >
          {/* Row 1: above cards (even indices) */}
          {timeline.map((entry, i) => (
            <div
              key={entry.date + "-above-" + i}
              className="flex items-end pb-3"
              style={{ gridRow: 1, gridColumn: i + 1 }}
            >
              {i % 2 === 0 ? <CardContent entry={entry} index={i} /> : null}
            </div>
          ))}

          {/* Row 2: timeline line + dots + dates */}
          {timeline.map((entry, i) => {
            const dotColor = DOT_COLORS[i % DOT_COLORS.length];
            return (
              <div
                key={entry.date + "-mid-" + i}
                className="relative flex flex-col items-center justify-center py-2"
                style={{ gridRow: 2, gridColumn: i + 1 }}
              >
                {/* Horizontal line segment */}
                <div
                  className="absolute top-1/2 -translate-y-1/2 h-[2px]"
                  style={{
                    left: i === 0 ? "50%" : `-${gap / 2}px`,
                    right: i === timeline.length - 1 ? "50%" : `-${gap / 2}px`,
                    background: "linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.12), rgba(255,255,255,0.06))",
                  }}
                />
                {/* Dot */}
                <div
                  className="relative w-3 h-3 rounded-full border-2 border-slate-900 shadow-sm z-10"
                  style={{ backgroundColor: dotColor }}
                />
                {/* Date */}
                <div className="text-center mt-1.5">
                  <div className="text-[10px] font-semibold text-slate-400 leading-tight">
                    {entry.date}
                  </div>
                </div>
              </div>
            );
          })}

          {/* Row 3: below cards (odd indices) */}
          {timeline.map((entry, i) => (
            <div
              key={entry.date + "-below-" + i}
              className="flex items-start pt-3"
              style={{ gridRow: 3, gridColumn: i + 1 }}
            >
              {i % 2 !== 0 ? <CardContent entry={entry} index={i} /> : null}
            </div>
          ))}
        </div>
      </div>

      {/* Done button */}
      <div className="shrink-0 flex justify-center pb-4">
        <button
          onClick={onNext}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-all duration-300 text-xs font-medium"
        >
          Done <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
