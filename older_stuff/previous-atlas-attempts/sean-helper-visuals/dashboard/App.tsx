import { Link } from 'react-router-dom'
import { projects, getStatusLabel, getStatusColor, type Project } from './data'

function StatusBadge({ status }: { status: Project['status'] }) {
  const color = getStatusColor(status)
  const label = getStatusLabel(status)
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium"
      style={{ background: `${color}15`, color, border: `1px solid ${color}30` }}
    >
      <span className="w-1.5 h-1.5 rounded-full" style={{ background: color }} />
      {label}
    </span>
  )
}

function ProjectCard({ project }: { project: Project }) {
  return (
    <Link
      to={`/project/${project.id}`}
      className="group flex items-center gap-5 rounded-xl border border-border bg-card px-5 py-4 transition-all hover:border-border-hover hover:bg-[#1a1a1a] hover:shadow-lg hover:shadow-black/20"
    >
      {/* Left: name + one-liner */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-3 mb-1">
          <h2 className="text-base font-semibold text-white group-hover:text-[color:var(--accent)] transition-colors truncate" style={{ '--accent': project.accent } as React.CSSProperties}>
            {project.name}
          </h2>
          <StatusBadge status={project.status} />
        </div>
        <div className="text-xs text-neutral-500">
          Started {project.dateStarted}{project.dateLastRan !== project.dateStarted ? ` · Last ran ${project.dateLastRan}` : ''}
        </div>
      </div>

      {/* Right: key stats as compact badges */}
      <div className="hidden md:flex items-center gap-2 shrink-0">
        {project.keyStats.slice(0, 3).map(stat => (
          <div key={stat.label} className="bg-[#0f0f0f] rounded-lg px-3 py-1.5 text-center">
            <div className="text-[10px] text-neutral-500 uppercase tracking-wider">{stat.label}</div>
            <div className="text-xs font-semibold text-white">{stat.value}</div>
          </div>
        ))}
      </div>

      {/* Arrow */}
      <svg className="w-4 h-4 text-neutral-600 group-hover:text-neutral-400 transition-colors shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
      </svg>
    </Link>
  )
}

function ComparisonTable() {
  return (
    <div className="mt-12 rounded-xl border border-border bg-card overflow-hidden">
      <div className="px-6 py-4 border-b border-border">
        <h2 className="text-lg font-semibold text-white">Loop Design Comparison</h2>
        <p className="text-[15px] text-neutral-500 mt-1">How each loop was architected and what we learned about building autonomous research systems</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-[15px]">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left px-6 py-3 text-neutral-400 font-medium">Design Aspect</th>
              <th className="text-left px-6 py-3 text-neutral-400 font-medium">QG Research Loop</th>
              <th className="text-left px-6 py-3 text-neutral-400 font-medium">DQCP Formalization</th>
              <th className="text-left px-6 py-3 text-neutral-400 font-medium">GUT Builder</th>
              <th className="text-left px-6 py-3 text-neutral-400 font-medium">Worldviews</th>
            </tr>
          </thead>
          <tbody className="text-neutral-300">
            <tr className="border-b border-border/50">
              <td className="px-6 py-3 font-medium text-white">Loop Strategy</td>
              <td className="px-6 py-3">Explore broadly, then verify</td>
              <td className="px-6 py-3">Answer one yes/no question</td>
              <td className="px-6 py-3">Go deep on one winning idea</td>
              <td className="px-6 py-3">One-shot enumeration (no loop)</td>
            </tr>
            <tr className="border-b border-border/50">
              <td className="px-6 py-3 font-medium text-white">Agent Architecture</td>
              <td className="px-6 py-3">Fixed 5 roles every iteration</td>
              <td className="px-6 py-3">Custom agents per phase</td>
              <td className="px-6 py-3">Phase-dependent roles</td>
              <td className="px-6 py-3">No agents (single pass)</td>
            </tr>
            <tr className="border-b border-border/50">
              <td className="px-6 py-3 font-medium text-white">State Management</td>
              <td className="px-6 py-3">state.json + THEORIES.md + HANDOFF.md</td>
              <td className="px-6 py-3">RESULTS.md + HANDOFF.md</td>
              <td className="px-6 py-3">Living knowledge doc (GRAND-THEORY.md)</td>
              <td className="px-6 py-3">Static output files</td>
            </tr>
            <tr className="border-b border-border/50">
              <td className="px-6 py-3 font-medium text-white">Iterations Used</td>
              <td className="px-6 py-3">17 of 30</td>
              <td className="px-6 py-3">4 of 15 (early stop)</td>
              <td className="px-6 py-3">1 of 50 (ongoing)</td>
              <td className="px-6 py-3">N/A</td>
            </tr>
            <tr className="border-b border-border/50">
              <td className="px-6 py-3 font-medium text-white">Continuation Method</td>
              <td className="px-6 py-3">Claude Code stop hook (bash)</td>
              <td className="px-6 py-3">Claude Code stop hook (bash)</td>
              <td className="px-6 py-3">Claude Code stop hook (bash)</td>
              <td className="px-6 py-3">Manual</td>
            </tr>
            <tr className="border-b border-border/50">
              <td className="px-6 py-3 font-medium text-white">Best Feature</td>
              <td className="px-6 py-3">Dual-mode (explore vs verify)</td>
              <td className="px-6 py-3">Fail-fast with early termination</td>
              <td className="px-6 py-3">Living knowledge prevents circles</td>
              <td className="px-6 py-3">Systematic coverage</td>
            </tr>
            <tr>
              <td className="px-6 py-3 font-medium text-white">Biggest Weakness</td>
              <td className="px-6 py-3">Score inflation in explore mode</td>
              <td className="px-6 py-3">Too narrow to discover new ideas</td>
              <td className="px-6 py-3">Early stage, unproven at scale</td>
              <td className="px-6 py-3">No verification of any claims</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <div className="min-h-screen bg-bg">
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-10">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-lg font-bold">
              R
            </div>
            <h1 className="text-3xl font-bold text-white tracking-tight">Science Research HQ</h1>
          </div>
        </div>

        {/* Project List — vertical, most recent first */}
        <div className="flex flex-col gap-3">
          {[...projects].sort((a, b) => {
            const order = ['grand-unified', 'dqcp', 'quantum-gravity', 'worldviews']
            return order.indexOf(a.id) - order.indexOf(b.id)
          }).map(project => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>

        {/* Comparison Table */}
        <ComparisonTable />

        {/* Key Lessons */}
        <div className="mt-12 rounded-xl border border-border bg-card p-6">
          <h2 className="text-lg font-semibold text-white mb-2">Lessons for Building Better Loops</h2>
          <p className="text-[15px] text-neutral-500 mb-5">What we learned about designing autonomous AI research systems</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              {
                title: 'Always include a Skeptic agent',
                body: 'Adversarial pressure is the single most valuable design choice. An agent whose entire job is to disagree and find fatal flaws prevents the loop from converging on ideas that sound good but don\'t hold up.',
                source: 'All projects',
              },
              {
                title: 'Force concrete outputs, not abstract proposals',
                body: 'Every idea scored 7+ during exploration and dropped to 5-6.5 when we asked "show me the math." Require concrete, verifiable outputs at every stage — not frameworks, not narratives, but actual calculations.',
                source: 'QG Loop',
              },
              {
                title: 'Focused questions resolve faster',
                body: 'The DQCP loop answered a specific yes/no question in 4 iterations. The QG Loop took 17 with a broad mandate. If you can frame your research question as a specific, answerable question — do it.',
                source: 'DQCP vs QG Loop',
              },
              {
                title: 'The living knowledge document prevents circles',
                body: 'A persistent document that accumulates established results, dead ends, and open questions is the most important piece of the architecture. Without it, agents re-explore the same dead ends across iterations.',
                source: 'GUT Builder',
              },
              {
                title: 'Stop hooks enable autonomy but are fragile',
                body: 'Claude Code\'s stop hook (a bash script that auto-restarts the agent when it finishes an iteration) is what makes the loops autonomous. But it\'s fragile — if the agent produces malformed state, the hook can break the loop.',
                source: 'All loops',
              },
              {
                title: 'Custom agents per problem outperform fixed roles',
                body: 'The DQCP loop picked different agents for each phase based on what expertise was needed. The QG Loop used the same 5 agents for everything. Tailoring agents to the specific task produced more targeted results.',
                source: 'DQCP',
              },
              {
                title: 'Dual-mode operation (explore vs verify) is powerful',
                body: 'Having the loop switch between "generate new ideas" mode and "stress-test existing ideas" mode catches score inflation early. Every loop should have a verification phase built in.',
                source: 'QG Loop',
              },
              {
                title: 'Enumeration without verification is incomplete',
                body: 'Generating 100 ideas is easy for AI. But the top scorers all turned out to be ideas that already had real math behind them. Breadth is cheap — depth and rigor are what matter.',
                source: 'Worldviews',
              },
            ].map((lesson, i) => (
              <div key={i} className="bg-[#0f0f0f] rounded-lg p-4">
                <div className="text-[15px] font-medium text-white mb-1">{lesson.title}</div>
                <div className="text-[13px] text-neutral-400 leading-relaxed mb-2">{lesson.body}</div>
                <div className="text-[10px] text-neutral-600 uppercase tracking-wider">Source: {lesson.source}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
