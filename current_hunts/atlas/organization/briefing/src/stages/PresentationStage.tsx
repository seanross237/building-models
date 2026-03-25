import { useState, useEffect, useCallback } from "react";
import {
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  Atom,
  Workflow,
  Swords,
  Layers,
  BarChart3,
  GitBranch,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Target,
  Lightbulb,
  Rocket,
  Presentation as PresentationIcon,
  type LucideIcon,
} from "lucide-react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface Slide {
  title: string;
  subtitle?: string;
  icon: LucideIcon;
  iconColor: string;
  content: React.ReactNode;
}

interface PresentationDef {
  title: string;
  subtitle: string;
  date: string;
  color: string;
  slides: Slide[];
}

// ─── Reusable Components ─────────────────────────────────────────────────────

function StatCard({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className="bg-white/[0.04] border border-white/[0.06] rounded-xl p-3 text-center">
      <div className="text-lg font-bold" style={{ color }}>{value}</div>
      <div className="text-[10px] text-gray-500 mt-0.5">{label}</div>
    </div>
  );
}

function Callout({ color, label, children }: { color: string; label: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl p-3" style={{ background: `${color}08`, border: `1px solid ${color}25` }}>
      <div className="text-[10px] font-medium uppercase tracking-wider mb-1" style={{ color }}>{label}</div>
      <div className="text-xs text-gray-300 leading-relaxed">{children}</div>
    </div>
  );
}

function GreenCheck({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex gap-2 items-start text-[11px]">
      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 mt-0.5 shrink-0" />
      <span className="text-gray-300">{children}</span>
    </div>
  );
}

function RedX({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex gap-2 items-start text-[11px]">
      <XCircle className="h-3.5 w-3.5 text-red-400 mt-0.5 shrink-0" />
      <span className="text-gray-300">{children}</span>
    </div>
  );
}

function AmberWarn({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex gap-2 items-start text-[11px]">
      <AlertTriangle className="h-3.5 w-3.5 text-amber-400 mt-0.5 shrink-0" />
      <span className="text-gray-300">{children}</span>
    </div>
  );
}

// ─── Presentations ───────────────────────────────────────────────────────────

const presentations: PresentationDef[] = [
  {
    title: "Building a System That Learns to Research",
    subtitle: "5 attempts, 1 architecture, and what we know now",
    date: "March 23, 2026",
    color: "#a855f7",
    slides: [
      {
        title: "Building a System That Learns to Research",
        subtitle: "5 attempts, 1 architecture, and what we know now",
        icon: Atom,
        iconColor: "text-violet-400",
        content: (
          <div className="space-y-6 text-center">
            <p className="text-sm text-gray-400 max-w-md mx-auto leading-relaxed">
              This isn't about quantum gravity. It's about the machine that investigates it.
              How the autonomous research system evolved, where it stands, and what's next.
            </p>
            <div className="grid grid-cols-3 gap-3 max-w-sm mx-auto">
              <StatCard label="Attempts" value="5" color="#a855f7" />
              <StatCard label="Total Iterations" value="~50" color="#6366f1" />
              <StatCard label="Current Version" value="v3" color="#10b981" />
            </div>
          </div>
        ),
      },
      {
        title: "The Five Attempts",
        subtitle: "Each one taught us something different",
        icon: GitBranch,
        iconColor: "text-cyan-400",
        content: (
          <div className="space-y-2">
            {[
              { date: "Mar 18", name: "100 Worldviews", result: "Breadth survey. Top scorer had real math behind it.", color: "#10b981" },
              { date: "Mar 20", name: "QG Loop (17 iter)", result: "5 agents per theory. FDCG survived. \"Exploration inflates.\"", color: "#10b981" },
              { date: "Mar 20", name: "DQCP Deep Dive", result: "4 iterations to kill a 7.3-scoring theory. Fast failure.", color: "#10b981" },
              { date: "Mar 21", name: "GUT + 7 Sprints", result: "FDCG physics compelling, math fundamentally broken. All repairs failed.", color: "#ef4444" },
              { date: "Mar 21-23", name: "Agent Loop v3", result: "New architecture. First autonomous run: 90 min, 5 explorations, 0 failures.", color: "#10b981" },
            ].map((a, i) => (
              <div key={i} className="flex gap-3 bg-white/[0.03] border border-white/[0.06] rounded-lg p-2.5">
                <div className="w-14 text-[10px] text-gray-500 font-mono shrink-0 pt-0.5">{a.date}</div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-gray-200">{a.name}</span>
                    <span className="w-1.5 h-1.5 rounded-full shrink-0" style={{ background: a.color }} />
                  </div>
                  <div className="text-[10px] text-gray-500 mt-0.5 leading-relaxed">{a.result}</div>
                </div>
              </div>
            ))}
          </div>
        ),
      },
      {
        title: "How the Loop Evolved",
        subtitle: "Each attempt changed the design",
        icon: Workflow,
        iconColor: "text-blue-400",
        content: (
          <div className="space-y-2">
            {[
              { v: "v1", label: "Flat loop, 5 fixed agents", lesson: "Exploration inflates, verification deflates", color: "#6366f1" },
              { v: "v1.5", label: "Focused question, fast convergence", lesson: "4 iterations > 17 when the question is sharp", color: "#8b5cf6" },
              { v: "v2", label: "Living knowledge document", lesson: "Persistent memory prevents re-exploring dead ends", color: "#a855f7" },
              { v: "v2.5", label: "Sprint elimination format", lesson: "Systematic failure proof > exploration", color: "#c084fc" },
              { v: "v3", label: "Missionary / Strategizer / Explorer", lesson: "Separate strategy from execution. Clean context per task.", color: "#10b981" },
            ].map((step) => (
              <div key={step.v} className="flex gap-3 items-start">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-bold shrink-0" style={{ background: `${step.color}15`, color: step.color, border: `1px solid ${step.color}30` }}>
                  {step.v}
                </div>
                <div className="flex-1 bg-white/[0.03] border border-white/[0.06] rounded-lg p-2.5">
                  <div className="text-xs font-medium text-gray-200">{step.label}</div>
                  <div className="text-[10px] text-gray-500 mt-0.5 italic">"{step.lesson}"</div>
                </div>
              </div>
            ))}
          </div>
        ),
      },
      {
        title: "The One Agent That Matters",
        subtitle: "The Skeptic was the MVP in every single attempt",
        icon: Swords,
        iconColor: "text-red-400",
        content: (
          <div className="space-y-4">
            <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-center">
              <p className="text-lg font-bold text-red-400 mb-1">"Math or it didn't happen."</p>
              <p className="text-[10px] text-red-300/50">Design principle, not just a finding</p>
            </div>
            <div className="space-y-2">
              {[
                { attempt: "QG Loop", quote: "All theories scored 7+ in exploration, dropped to 5-6.5 under Skeptic scrutiny" },
                { attempt: "DQCP", quote: "Killed a promising theory in 4 iterations. 5 of 6 criteria didn't match." },
                { attempt: "Sprints", quote: "Caught literature results that changed the analysis. Found 6 independent proofs of failure." },
                { attempt: "Strategy 001", quote: "Novelty check revealed the constructed theory already existed (known since 1989)" },
              ].map((q) => (
                <div key={q.attempt} className="bg-white/[0.03] border border-white/[0.06] rounded-lg p-2.5">
                  <div className="text-[10px] text-red-400 font-medium mb-0.5">{q.attempt}</div>
                  <div className="text-[11px] text-gray-400 italic leading-relaxed">"{q.quote}"</div>
                </div>
              ))}
            </div>
            <Callout color="#ef4444" label="Takeaway">
              Adversarial agents prevent accumulation of plausible-sounding nonsense.
              Always include one whose job is to disagree.
            </Callout>
          </div>
        ),
      },
      {
        title: "The Current System (v3)",
        subtitle: "Missionary / Strategizer / Explorer",
        icon: Layers,
        iconColor: "text-emerald-400",
        content: (
          <div className="space-y-3">
            <div className="space-y-2">
              {[
                { level: "Missionary", desc: "Sets direction. Writes STRATEGY.md. Runs on demand.", color: "#f59e0b", arrow: true },
                { level: "Strategizer", desc: "Owns the loop. Designs explorations, reads reports, adapts. Runs autonomously via stop hook.", color: "#6366f1", arrow: true },
                { level: "Explorer", desc: "Single investigation. Clean context window. Disposable. Writes REPORT.md + summary.", color: "#10b981", arrow: false },
              ].map((a) => (
                <div key={a.level}>
                  <div className="flex gap-2.5 bg-white/[0.03] border border-white/[0.06] rounded-lg p-2.5">
                    <div className="w-2 rounded-full shrink-0" style={{ background: a.color }} />
                    <div>
                      <div className="text-xs font-medium text-gray-200">{a.level}</div>
                      <div className="text-[10px] text-gray-500 mt-0.5">{a.desc}</div>
                    </div>
                  </div>
                  {a.arrow && (
                    <div className="flex justify-center py-0.5">
                      <div className="w-px h-3 bg-white/10" />
                    </div>
                  )}
                </div>
              ))}
            </div>
            <div className="grid grid-cols-3 gap-2 text-center">
              {[
                { dir: "Down", desc: "Goals, strategy, context", color: "#f59e0b" },
                { dir: "Up", desc: "Reports, summaries, findings", color: "#10b981" },
                { dir: "Lateral", desc: "Library — any agent browses", color: "#6366f1" },
              ].map((f) => (
                <div key={f.dir} className="bg-white/[0.03] border border-white/[0.06] rounded-lg p-2">
                  <div className="text-[10px] font-medium" style={{ color: f.color }}>{f.dir}</div>
                  <div className="text-[9px] text-gray-500 mt-0.5">{f.desc}</div>
                </div>
              ))}
            </div>
            <Callout color="#10b981" label="Key Innovation">
              Explorers get a clean context window — no history, no strategy, just the goal.
              The Strategizer holds the thread. The library holds the knowledge.
            </Callout>
          </div>
        ),
      },
      {
        title: "First Run: The Numbers",
        subtitle: "Strategy 001 — Convergence-Driven Theory Construction",
        icon: BarChart3,
        iconColor: "text-cyan-400",
        content: (
          <div className="space-y-5">
            <div className="grid grid-cols-2 gap-3">
              <StatCard label="Runtime" value="90 min" color="#10b981" />
              <StatCard label="Explorations" value="5" color="#6366f1" />
              <StatCard label="Failures" value="0" color="#10b981" />
              <StatCard label="Context Used" value="16%" color="#10b981" />
              <StatCard label="Context Resets" value="0" color="#10b981" />
              <StatCard label="Report Lines" value="3,440" color="#f59e0b" />
            </div>
            <Callout color="#10b981" label="Highlight">
              The entire run completed in a single continuous session. The stop hook
              correctly detected completion, cleaned up state, and let the session end.
              Zero human intervention.
            </Callout>
          </div>
        ),
      },
      {
        title: "First Run: What Happened",
        subtitle: "5 explorations across 3 phases",
        icon: GitBranch,
        iconColor: "text-blue-400",
        content: (
          <div className="space-y-2">
            {[
              { n: 1, phase: "Constraints", title: "Spectral dimension constraints", result: "10 constraints. Ostrogradsky no-go: must choose nonlocality, Lorentz violation, or modified ghosts.", color: "#10b981" },
              { n: 2, phase: "Constraints", title: "Thermodynamic/entanglement constraints", result: "13 constraints. Ghost-free IDG gives correct BH entropy. Nonlocal gravity most favored.", color: "#10b981" },
              { n: 3, phase: "Synthesis", title: "Theory construction", result: "Built Kuzmin-Tomboulis-Modesto nonlocal gravity. Passed Tier 1 & 2. 19/21 constraints satisfied.", color: "#10b981" },
              { n: 4, phase: "Validation", title: "Novelty check", result: "NOT NOVEL — theory known since 1989. Methodology (convergent selection) is the novel contribution.", color: "#ef4444" },
              { n: 5, phase: "Pivot", title: "Asymptotic Safety bridge", result: "Same universality class but full identification fails. Partial success.", color: "#f59e0b" },
            ].map((exp) => (
              <div key={exp.n} className="flex gap-2.5 bg-white/[0.03] border border-white/[0.06] rounded-lg p-2.5">
                <div className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0" style={{ background: `${exp.color}20`, color: exp.color, border: `1px solid ${exp.color}40` }}>
                  {exp.n}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-gray-200">{exp.title}</span>
                    <span className="text-[9px] px-1.5 py-0.5 rounded bg-white/[0.04] text-gray-500">{exp.phase}</span>
                  </div>
                  <div className="text-[10px] text-gray-500 mt-0.5 leading-relaxed">{exp.result}</div>
                </div>
              </div>
            ))}
            <Callout color="#6366f1" label="Key Moment">
              When exploration 4 revealed the theory wasn't novel, the strategizer didn't give up.
              It identified the best remaining angle and pivoted. That's the system working.
            </Callout>
          </div>
        ),
      },
      {
        title: "What the System Got Right",
        icon: CheckCircle2,
        iconColor: "text-emerald-400",
        content: (
          <div className="space-y-2.5">
            <GreenCheck>Fully autonomous operation — zero human intervention during the run</GreenCheck>
            <GreenCheck>Strategic pivoting when the novelty check failed</GreenCheck>
            <GreenCheck>Background monitoring — explorers run in background, strategizer checks every 15 min</GreenCheck>
            <GreenCheck>Incremental report writing — explorers write as they work</GreenCheck>
            <GreenCheck>Decision logging — DECISIONS.md captured clear reasoning for every choice</GreenCheck>
            <GreenCheck>Stop hook — correctly detected completion, cleaned up state</GreenCheck>
            <div className="mt-3">
              <Callout color="#10b981" label="Bottom Line">
                The architecture works. A hierarchical agent system can autonomously
                extract constraints, synthesize theories, validate, and pivot — all in 90 minutes.
              </Callout>
            </div>
          </div>
        ),
      },
      {
        title: "What the System Got Wrong",
        icon: XCircle,
        iconColor: "text-red-400",
        content: (
          <div className="space-y-2.5">
            <RedX>Novelty check too late — built entire theory before discovering it existed (1989)</RedX>
            <RedX>No meta-learning — system didn't capture lessons about its own performance</RedX>
            <RedX>Token tracking broken — all explorations show 0 tokens used</RedX>
            <AmberWarn>Cosmological constant never seriously attempted</AmberWarn>
            <AmberWarn>Session binding race condition</AmberWarn>
            <AmberWarn>Library inbox unprocessed</AmberWarn>
            <div className="mt-3">
              <Callout color="#ef4444" label="Biggest Gap">
                The novelty gate is the highest-priority fix. Check "does this already exist?"
                before investing in full synthesis and validation.
              </Callout>
            </div>
          </div>
        ),
      },
      {
        title: "The Core Bet",
        subtitle: "Why convergence matters",
        icon: Target,
        iconColor: "text-amber-400",
        content: (
          <div className="space-y-4">
            <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 text-center">
              <p className="text-sm text-amber-200 leading-relaxed font-medium">
                "Cross-cutting convergence is not coincidental — it's the fingerprint of the correct theory."
              </p>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed">
              Seven independent QG programs all agree: spacetime dimensions drop from 4 to 2 at short distances.
            </p>
            <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-3">
              <div className="text-xs text-gray-200 font-medium mb-2">The strategy:</div>
              <div className="space-y-1.5 text-[11px] text-gray-400">
                <div className="flex gap-2"><span className="text-amber-400">1.</span> Extract constraints from convergent results</div>
                <div className="flex gap-2"><span className="text-amber-400">2.</span> Ask: what is the simplest structure that produces all of them?</div>
                <div className="flex gap-2"><span className="text-amber-400">3.</span> If known — methodology validates. If new — we found something.</div>
              </div>
            </div>
            <Callout color="#f59e0b" label="First Run Validated This">
              23 constraints from 2 convergent results uniquely selected one theory.
              It was known (Kuzmin-Tomboulis), which means the method works.
            </Callout>
          </div>
        ),
      },
      {
        title: "What's Next",
        subtitle: "Concrete moves for Strategy 002+",
        icon: Lightbulb,
        iconColor: "text-cyan-400",
        content: (
          <div className="space-y-3">
            {[
              { priority: "P0", title: "Add novelty gate", desc: "Literature check after constraint extraction, before synthesis.", color: "#ef4444" },
              { priority: "P0", title: "Populate meta-library", desc: "Teach the system about itself.", color: "#ef4444" },
              { priority: "P1", title: "Fix session binding", desc: "Pre-bind strategizer transcript path during setup.", color: "#f59e0b" },
              { priority: "P1", title: "Run the curator", desc: "Process the library inbox from the first run.", color: "#f59e0b" },
              { priority: "P2", title: "Strategy 002", desc: "Cosmological constant, AS-IDG bridge, or new convergent result. Missionary decides.", color: "#6366f1" },
            ].map((item) => (
              <div key={item.title} className="flex gap-2.5 bg-white/[0.03] border border-white/[0.06] rounded-lg p-2.5">
                <div className="px-1.5 py-0.5 rounded text-[9px] font-bold shrink-0 h-fit" style={{ background: `${item.color}20`, color: item.color, border: `1px solid ${item.color}40` }}>
                  {item.priority}
                </div>
                <div>
                  <div className="text-xs font-medium text-gray-200">{item.title}</div>
                  <div className="text-[10px] text-gray-500 mt-0.5 leading-relaxed">{item.desc}</div>
                </div>
              </div>
            ))}
          </div>
        ),
      },
      {
        title: "The system works.",
        subtitle: "Now make it learn.",
        icon: Rocket,
        iconColor: "text-violet-400",
        content: (
          <div className="space-y-6 text-center">
            <div className="grid grid-cols-3 gap-3 max-w-sm mx-auto">
              <StatCard label="Attempts" value="5" color="#a855f7" />
              <StatCard label="Architecture" value="v3" color="#10b981" />
              <StatCard label="Status" value="Works" color="#10b981" />
            </div>
            <p className="text-xs text-gray-500 max-w-sm mx-auto leading-relaxed">
              The autonomous research loop runs, makes decisions, pivots, and completes.
              The next frontier is meta-learning — making the system improve itself.
            </p>
          </div>
        ),
      },
    ],
  },
];

// ─── Presentation List ───────────────────────────────────────────────────────

function PresentationList({ onSelect }: { onSelect: (idx: number) => void }) {
  return (
    <div className="w-full max-w-lg mx-auto px-6 py-8 animate-fade-in">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-14 h-14 rounded-2xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center">
            <PresentationIcon className="w-7 h-7 text-violet-400" />
          </div>
        </div>
        <div className="text-sm uppercase tracking-[0.3em] text-slate-500 mb-2 font-mono">
          Presentations
        </div>
        <p className="text-xs text-slate-600">
          {presentations.length} available
        </p>
      </div>

      <div className="space-y-3">
        {presentations.map((p, i) => (
          <button
            key={i}
            onClick={() => onSelect(i)}
            className="w-full text-left flex gap-4 items-center p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.07] hover:border-white/[0.12] transition-all duration-200 group"
          >
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 transition-transform group-hover:scale-110"
              style={{ background: `${p.color}15`, border: `1px solid ${p.color}30` }}
            >
              <PresentationIcon className="w-5 h-5" style={{ color: p.color }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-white/80 group-hover:text-white transition-colors truncate">
                {p.title}
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">
                {p.date} &middot; {p.slides.length} slides
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-slate-400 transition-colors shrink-0" />
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── Slide Viewer ────────────────────────────────────────────────────────────

function SlideViewer({
  presentation,
  onBack,
}: {
  presentation: PresentationDef;
  onBack: () => void;
}) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [direction, setDirection] = useState<"left" | "right" | null>(null);
  const { slides } = presentation;

  const isLast = currentSlide === slides.length - 1;
  const isFirst = currentSlide === 0;

  const goTo = useCallback((idx: number, dir: "left" | "right") => {
    if (idx < 0 || idx >= slides.length) return;
    setDirection(dir);
    setCurrentSlide(idx);
    setTimeout(() => setDirection(null), 300);
  }, [slides.length]);

  const next = useCallback(() => {
    if (isLast) { onBack(); return; }
    goTo(currentSlide + 1, "right");
  }, [currentSlide, isLast, goTo, onBack]);

  const prev = useCallback(() => goTo(currentSlide - 1, "left"), [currentSlide, goTo]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); next(); }
      if (e.key === "ArrowLeft") { e.preventDefault(); prev(); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [next, prev]);

  const slide = slides[currentSlide];
  const Icon = slide.icon;
  const animClass =
    direction === "right" ? "animate-slide-right" :
    direction === "left" ? "animate-slide-left" : "";

  return (
    <div className="w-full max-w-lg mx-auto flex flex-col h-full max-h-[85vh] px-4">
      <div className={`text-center mb-4 shrink-0 ${animClass}`}>
        <Icon className={`h-8 w-8 ${slide.iconColor} mx-auto mb-2`} />
        <h2 className="text-xl font-bold text-white">{slide.title}</h2>
        {slide.subtitle && (
          <p className="text-xs text-gray-500 mt-0.5">{slide.subtitle}</p>
        )}
      </div>

      <div className={`flex-1 overflow-y-auto px-1 ${animClass}`}>
        {slide.content}
      </div>

      <div className="mt-4 shrink-0 flex items-center justify-between">
        <button
          onClick={isFirst ? onBack : prev}
          className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-200 transition-colors px-3 py-2"
        >
          <ChevronLeft className="h-3.5 w-3.5" />
          {isFirst ? "All presentations" : "Back"}
        </button>

        <div className="flex gap-1">
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={() => goTo(i, i > currentSlide ? "right" : "left")}
              className={`h-1.5 rounded-full transition-all ${
                i === currentSlide
                  ? "w-4 bg-violet-400"
                  : "w-1.5 bg-white/20 hover:bg-white/40"
              }`}
            />
          ))}
        </div>

        <button
          onClick={next}
          className="flex items-center gap-1 text-xs text-gray-300 hover:text-white transition-colors px-3 py-2 rounded-lg bg-white/[0.06] hover:bg-white/[0.12]"
        >
          {isLast ? "Done" : "Next"}
          {isLast ? <ArrowRight className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
        </button>
      </div>
    </div>
  );
}

// ─── Stage Component ─────────────────────────────────────────────────────────

export function PresentationStage({ onNext }: { onNext: () => void }) {
  const [selected, setSelected] = useState<number | null>(null);

  if (selected !== null) {
    return (
      <SlideViewer
        presentation={presentations[selected]}
        onBack={() => setSelected(null)}
      />
    );
  }

  if (presentations.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full animate-fade-in">
        <PresentationIcon className="w-10 h-10 text-violet-400/40 mb-4" />
        <h2 className="text-xl font-semibold text-slate-400 mb-2">No presentations</h2>
        <p className="text-sm text-slate-600 mb-8 max-w-sm text-center">
          Presentations are built on request to get you back up to speed.
        </p>
        <button
          onClick={onNext}
          className="flex items-center gap-2 px-8 py-3 rounded-xl bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-all duration-300"
        >
          Back <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  return <PresentationList onSelect={setSelected} />;
}
