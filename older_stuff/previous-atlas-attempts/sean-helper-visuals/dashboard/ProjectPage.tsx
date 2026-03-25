import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { getProject, getStatusColor, getStatusLabel, type Project, type TheoryScore } from './data'

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

// --- Tab Component ---
function Tabs({ tabs, activeTab, onChange }: { tabs: string[]; activeTab: string; onChange: (tab: string) => void }) {
  return (
    <div className="flex gap-1 border-b border-border mb-6 overflow-x-auto">
      {tabs.map(tab => (
        <button
          key={tab}
          onClick={() => onChange(tab)}
          className={`px-4 py-2.5 text-sm font-medium whitespace-nowrap transition-colors border-b-2 -mb-px ${
            activeTab === tab
              ? 'text-white border-blue-500'
              : 'text-neutral-500 border-transparent hover:text-neutral-300 hover:border-neutral-600'
          }`}
        >
          {tab}
        </button>
      ))}
    </div>
  )
}

// --- Process Flow Diagram ---
function ProcessFlow({ phases }: { phases: Project['methodology']['processPhases'] }) {
  return (
    <div className="relative">
      {/* Connection line */}
      <div className="absolute left-6 top-8 bottom-8 w-px bg-gradient-to-b from-transparent via-neutral-700 to-transparent" />
      <div className="space-y-4">
        {phases.map((phase, i) => (
          <div key={phase.name} className="relative flex items-start gap-4">
            {/* Node */}
            <div
              className="relative z-10 w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-sm shrink-0 shadow-lg"
              style={{ background: phase.color, boxShadow: `0 0 20px ${phase.color}30` }}
            >
              {i + 1}
            </div>
            {/* Content */}
            <div className="pt-1 pb-2">
              <div className="text-[15px] font-semibold text-white mb-1">{phase.name}</div>
              <div className="text-[13px] text-neutral-400 leading-relaxed max-w-lg">{phase.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// --- Promising Leads Panel ---
function PromisingLeads({ leads }: { leads: Project['promisingLeads'] }) {
  if (leads.length === 0) return null

  const statusColors: Record<string, { bg: string; text: string }> = {
    'Lead theory': { bg: '#10b981', text: '#10b981' },
    'Confirmed': { bg: '#3b82f6', text: '#3b82f6' },
    'Testable': { bg: '#8b5cf6', text: '#8b5cf6' },
    'Possibly novel': { bg: '#f59e0b', text: '#f59e0b' },
    'Worth pursuing': { bg: '#22d3ee', text: '#22d3ee' },
    'Established': { bg: '#10b981', text: '#10b981' },
    'Investigating': { bg: '#f59e0b', text: '#f59e0b' },
    'Promising': { bg: '#22d3ee', text: '#22d3ee' },
    'Unexplored': { bg: '#a855f7', text: '#a855f7' },
    'Published physics': { bg: '#10b981', text: '#10b981' },
    'Future use': { bg: '#6b7280', text: '#6b7280' },
  }

  return (
    <div className="space-y-3">
      {leads.map((lead, i) => {
        const colors = statusColors[lead.status] ?? { bg: '#6b7280', text: '#6b7280' }
        return (
          <div key={i} className="rounded-xl border border-border bg-[#0f0f0f] p-5">
            <div className="flex items-start justify-between gap-3 mb-2">
              <div className="text-[15px] font-semibold text-white">{lead.title}</div>
              <span
                className="text-[10px] px-2 py-0.5 rounded-full font-medium shrink-0 uppercase tracking-wider"
                style={{ background: `${colors.bg}15`, color: colors.text, border: `1px solid ${colors.bg}30` }}
              >
                {lead.status}
              </span>
            </div>
            <div className="text-[13px] text-neutral-400 leading-relaxed">{lead.description}</div>
          </div>
        )
      })}
    </div>
  )
}

// --- Theory Score Chart (for QG Loop) ---
function TheoryScoreChart({ theories }: { theories: TheoryScore[] }) {
  const sorted = [...theories].sort((a, b) => {
    const aScore = b.verificationScore ?? b.explorationScore
    const bScore = a.verificationScore ?? a.explorationScore
    return aScore - bScore
  })

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-6 text-xs text-neutral-500 mb-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-sm bg-blue-500/40" />
          <span>Initial Score (when first proposed)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-sm bg-blue-500" />
          <span>After Mathematical Scrutiny</span>
        </div>
      </div>
      {sorted.map(theory => {
        const maxScore = 10
        const explPct = (theory.explorationScore / maxScore) * 100
        const verifPct = theory.verificationScore ? (theory.verificationScore / maxScore) * 100 : null

        const getStatusStyle = (status: string) => {
          if (status === 'SURVIVED') return { bg: '#10b981', text: '#10b981' }
          if (status === 'Demolished') return { bg: '#ef4444', text: '#ef4444' }
          if (status === 'Not novel') return { bg: '#6b7280', text: '#6b7280' }
          return { bg: '#f59e0b', text: '#f59e0b' }
        }
        const statusStyle = getStatusStyle(theory.status)

        return (
          <div key={theory.name} className="group">
            <div className="flex items-center justify-between mb-1.5">
              <div className="text-[15px] text-neutral-300 font-medium truncate max-w-[60%]">{theory.name}</div>
              <div className="flex items-center gap-2">
                <span
                  className="text-[10px] px-1.5 py-0.5 rounded font-medium"
                  style={{ background: `${statusStyle.bg}15`, color: statusStyle.text }}
                >
                  {theory.status}
                </span>
              </div>
            </div>
            <div className="relative h-6 bg-[#0f0f0f] rounded-lg overflow-hidden">
              {/* Initial score bar */}
              <div
                className="absolute top-0 left-0 h-full rounded-lg transition-all bg-blue-500/30"
                style={{ width: `${explPct}%` }}
              />
              {/* Post-scrutiny bar */}
              {verifPct !== null && (
                <div
                  className="absolute top-0 left-0 h-full rounded-lg transition-all bg-blue-500"
                  style={{ width: `${verifPct}%` }}
                />
              )}
              {/* Scores */}
              <div className="absolute inset-0 flex items-center px-3 text-xs font-medium text-white/80">
                {theory.explorationScore.toFixed(1)}
                {theory.verificationScore !== null && (
                  <span className="ml-1 text-neutral-400">
                    {' '}&#x2192; {theory.verificationScore.toFixed(1)}
                  </span>
                )}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

// --- DQCP Evidence Table ---
function DQCPEvidencePanel() {
  const criteria = [
    { criterion: 'Two Landau-type phases on both sides', status: 'FAIL', detail: 'One side has exotic "topological order" — not the simple kind of phase needed' },
    { criterion: 'Both sides confined, deconfined only at transition', status: 'FAIL', detail: 'Fractons are already deconfined in their own phase — breaks the pattern' },
    { criterion: 'New gauge field appears at transition', status: 'FAIL', detail: 'The gauge field was there from the start — it\'s fundamental, not emergent' },
    { criterion: 'Berry phase mechanism suppresses monopoles', status: 'FAIL', detail: 'No mechanism found for this in the fracton system' },
    { criterion: 'Enlarged symmetry at the critical point', status: 'FAIL', detail: 'No candidate symmetry enhancement identified' },
    { criterion: 'Known to work in the right dimension (3+1D)', status: 'FAIL', detail: 'No DQCP has ever been found in 3+1 dimensions' },
  ]

  const transitionOrder = [
    { outcome: 'Abrupt (first-order)', probability: 50, color: '#ef4444', key: 'Most analogies point here' },
    { outcome: 'Smooth (continuous)', probability: 30, color: '#22d3ee', key: 'Possible if special dynamics apply' },
    { outcome: 'Crossover (gradual)', probability: 15, color: '#f59e0b', key: 'If certain charges are equal' },
    { outcome: 'Something genuinely new', probability: 5, color: '#a855f7', key: 'Fracton physics is so exotic it breaks analogies' },
  ]

  return (
    <div className="space-y-8">
      {/* DQCP Criteria */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">Checklist: Does This Meet the Criteria?</h3>
        <p className="text-[13px] text-neutral-500 mb-4">5 of 6 required criteria fail — that is enough to rule it out regardless of anything else</p>
        <div className="space-y-2">
          {criteria.map(c => (
            <div key={c.criterion} className="flex items-start gap-3 rounded-lg bg-[#0f0f0f] px-4 py-3">
              <div className={`mt-0.5 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                c.status === 'FAIL' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'
              }`}>
                {c.status === 'FAIL' ? '\u2717' : '\u2713'}
              </div>
              <div>
                <div className="text-[15px] text-neutral-300 font-medium">{c.criterion}</div>
                <div className="text-[13px] text-neutral-500 mt-0.5">{c.detail}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Transition Order */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">What Kind of Transition Is It Instead?</h3>
        <p className="text-[13px] text-neutral-500 mb-4">Even though it is not a DQCP, the question of what kind of transition it IS remains genuinely uncertain</p>
        <div className="space-y-3">
          {transitionOrder.map(t => (
            <div key={t.outcome} className="flex items-center gap-3">
              <div className="w-20 text-right text-sm font-bold" style={{ color: t.color }}>
                {t.probability}%
              </div>
              <div className="flex-1 h-6 bg-[#0f0f0f] rounded-lg overflow-hidden relative">
                <div
                  className="h-full rounded-lg transition-all"
                  style={{ width: `${t.probability}%`, background: t.color, opacity: 0.6 }}
                />
                <div className="absolute inset-0 flex items-center px-3 text-xs text-neutral-300 font-medium">
                  {t.outcome}
                </div>
              </div>
              <div className="text-[13px] text-neutral-500 w-52 truncate">{t.key}</div>
            </div>
          ))}
        </div>
        <div className="mt-4 rounded-lg border border-red-500/20 bg-red-500/5 px-4 py-3">
          <div className="text-[15px] text-red-300 font-medium">Verdict: Ruled Out at 95% Confidence</div>
          <div className="text-[13px] text-neutral-400 mt-1">The structural failures are so comprehensive that the transition type does not matter for the DQCP question.</div>
        </div>
      </div>
    </div>
  )
}

// --- GUT Builder Active Status ---
function GUTActiveStatus() {
  return (
    <div className="space-y-6">
      {/* Current State */}
      <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-5">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <div className="text-[15px] font-semibold text-emerald-300">Active Research</div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-xs text-neutral-500 mb-1">Current Phase</div>
            <div className="text-[15px] text-white font-medium">Phase B: Investigate</div>
          </div>
          <div>
            <div className="text-xs text-neutral-500 mb-1">Current Approach</div>
            <div className="text-[15px] text-white font-medium">Multi-Species Fracton Compositeness</div>
          </div>
          <div>
            <div className="text-xs text-neutral-500 mb-1">Big Question</div>
            <div className="text-[15px] text-white font-medium">Can other forces of nature emerge from fractons?</div>
          </div>
          <div>
            <div className="text-xs text-neutral-500 mb-1">Current Test</div>
            <div className="text-[15px] text-white font-medium">Do the right kind of force-carrying particles emerge?</div>
          </div>
        </div>
      </div>

      {/* Research Roadmap */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">The Big Questions (Research Roadmap)</h3>
        <p className="text-[13px] text-neutral-500 mb-4">10 questions the loop is trying to answer, in order. Each one builds on the previous answers.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {[
            { q: 'What is spacetime made of?', status: 'partial', note: 'Partially answered: fracton dipole condensate' },
            { q: 'Where do the other forces come from?', status: 'active', note: 'Currently investigating' },
            { q: 'Where does matter come from?', status: 'open', note: 'Skyrmions are a candidate' },
            { q: 'Why do the forces have the strengths they do?', status: 'open', note: 'Not yet addressed' },
            { q: 'What is dark matter?', status: 'open', note: 'Not yet addressed' },
            { q: 'Why is the vacuum energy so small?', status: 'open', note: 'Not yet addressed' },
            { q: 'What is time?', status: 'open', note: 'Not yet addressed' },
            { q: 'What happens inside black holes?', status: 'open', note: 'Not yet addressed' },
            { q: 'Why does quantum mechanics work?', status: 'open', note: 'Not yet addressed' },
            { q: 'What was the Big Bang?', status: 'open', note: 'Not yet addressed' },
          ].map((item, i) => {
            const statusColors = {
              partial: { bg: 'bg-yellow-500/10', text: 'text-yellow-400', dot: 'bg-yellow-400' },
              active: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', dot: 'bg-emerald-400 animate-pulse' },
              open: { bg: 'bg-neutral-500/10', text: 'text-neutral-500', dot: 'bg-neutral-600' },
            }
            const s = statusColors[item.status as keyof typeof statusColors]
            return (
              <div key={i} className={`rounded-lg ${s.bg} px-4 py-3 flex items-start gap-3`}>
                <div className={`w-2 h-2 mt-1.5 rounded-full shrink-0 ${s.dot}`} />
                <div>
                  <div className={`text-[15px] font-medium ${s.text}`}>{item.q}</div>
                  <div className="text-[13px] text-neutral-500 mt-0.5">{item.note}</div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Established Results Summary */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">What the Loop Has Established So Far (12 Results)</h3>
        <p className="text-[13px] text-neutral-500 mb-4">These are results that survived scrutiny and are now treated as established foundations for future iterations.</p>
        <div className="space-y-2">
          {[
            'Gravity emerges from fracton dipole condensation (the core mechanism)',
            'The graviton propagator matches Einstein\'s gravity (linearized version)',
            'Gauge symmetry enhancement proven mathematically via Stueckelberg decomposition',
            'S-wave condensation is preferred (75-80% confidence)',
            'Extra scalar particle gets a large mass, hiding it from experiments',
            'Effective Lorentz symmetry emerges at low energies (80-85% confidence)',
            'Specific prediction for gravitational noise (Oppenheim point)',
            'Speed of light and Newton\'s constant derive from condensate properties',
            'The theory only works in 4 dimensions (matching our universe)',
            'Carroll algebra = fracton algebra (confirmed by 2023 published paper)',
            'DQCP ruled out — transition is a fracton Higgs mechanism (70%)',
            'Phase transition: 50% abrupt, 30% smooth, 15% gradual crossover',
          ].map((result, i) => (
            <div key={i} className="flex items-start gap-3 rounded-lg bg-[#0f0f0f] px-4 py-2.5">
              <div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">
                {'\u2713'}
              </div>
              <div className="text-[15px] text-neutral-300">{result}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// --- Worldviews Overview ---
function WorldviewsOverview() {
  const tiers = [
    {
      name: 'Tier 1: Most Promising',
      range: '27-24 pts',
      count: 8,
      color: '#fbbf24',
      examples: [
        'CPT Boundary Condition (actual published physics)',
        'Computation + Holographic hybrid',
        'The Relational Universe',
        'Noncommutative Geometry reinterpretation',
      ],
    },
    { name: 'Tier 2: Strong Contenders', range: '23 pts', count: 11, color: '#a3e635', examples: ['Derive gravity from something deeper', 'Resolve the Firewall Paradox'] },
    { name: 'Tier 3: Above Average', range: '22-21 pts', count: 16, color: '#22d3ee', examples: ['Pure Holographic', 'Solve the Black Hole Information Paradox'] },
    { name: 'Tier 4: Average', range: '20 pts', count: 18, color: '#6b7280', examples: ['Pure Thermodynamic', 'Solve the Measurement Problem'] },
    { name: 'Tier 5: Below Average', range: '19-18 pts', count: 20, color: '#525252', examples: ['Pure Computational', 'Derive quantum mechanics from something deeper'] },
    { name: 'Tier 6: Weak', range: '17-15 pts', count: 27, color: '#404040', examples: ['Various adversarial and wild card combinations'] },
  ]

  const categories = [
    { name: 'Pure Worldviews', count: 8, desc: '8 single-lens approaches (Computational, Information, Thermodynamic, Topological, Holographic, Error-Correcting, Categorical, Complexified)' },
    { name: 'Pairwise Hybrids', count: 28, desc: 'Every possible pair of the 8 pure worldviews combined' },
    { name: 'Focused Deep Dives', count: 20, desc: 'One radical reinterpretation of a single concept, everything else standard' },
    { name: 'Problem-Targeted', count: 20, desc: 'Optimized to solve specific open problems (black holes, measurement, vacuum energy, etc.)' },
    { name: 'Adversarial', count: 12, desc: 'Deliberately paradoxical combinations that force creative tension' },
    { name: 'Wild Cards', count: 12, desc: 'Unconventional meta-combinations and thought experiments' },
  ]

  const criteria = [
    'Matches reality (pass/fail)',
    'Self-consistent (/5)',
    'Simplicity (/5)',
    'Math precision (/5)',
    'Explanatory power (/5)',
    'New predictions (/5)',
    'Unifying power (/5)',
    'Compatible with known physics (/5)',
  ]

  return (
    <div className="space-y-8">
      {/* Categories */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">6 Categories of Worldviews</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {categories.map(cat => (
            <div key={cat.name} className="rounded-lg bg-[#0f0f0f] px-4 py-3">
              <div className="flex items-center justify-between mb-1">
                <div className="text-[15px] font-medium text-white">{cat.name}</div>
                <div className="text-xs text-neutral-500">{cat.count} worldviews</div>
              </div>
              <div className="text-[13px] text-neutral-400">{cat.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Scoring Criteria */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">How Each Was Scored (max 35 points)</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          {criteria.map((c, i) => (
            <div key={i} className="rounded-lg bg-[#0f0f0f] px-3 py-2.5 text-[13px] text-neutral-300">
              {c}
            </div>
          ))}
        </div>
      </div>

      {/* Tier Breakdown */}
      <div>
        <h3 className="text-base font-semibold text-white mb-3">Score Distribution</h3>
        <div className="space-y-3">
          {tiers.map(tier => (
            <div key={tier.name}>
              <div className="flex items-center justify-between mb-1.5">
                <div className="text-[15px] text-neutral-300 font-medium">{tier.name}</div>
                <div className="text-xs text-neutral-500">{tier.count} worldviews &middot; {tier.range}</div>
              </div>
              <div className="relative h-5 bg-[#0f0f0f] rounded-lg overflow-hidden">
                <div
                  className="h-full rounded-lg transition-all"
                  style={{ width: `${tier.count}%`, background: tier.color, opacity: 0.6 }}
                />
              </div>
              <div className="mt-1 text-[13px] text-neutral-500">
                e.g. {tier.examples.join(', ')}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Key Finding */}
      <div className="rounded-lg border border-yellow-500/20 bg-yellow-500/5 px-5 py-4">
        <div className="text-[15px] font-medium text-yellow-300 mb-1">Key Finding</div>
        <div className="text-[13px] text-neutral-300 leading-relaxed">
          The top-scoring worldviews are all grounded in <strong className="text-white">existing, formalized research programs</strong> with real mathematical machinery — not creative speculation. The #1 worldview (CPT Boundary Condition by Boyle-Finn-Turok) has <strong className="text-white">published, computed, testable predictions</strong>. Lesson: generating ideas is easy; the ones worth pursuing are the ones with actual math behind them.
        </div>
      </div>
    </div>
  )
}

// --- Markdown File Viewer ---
function MarkdownViewer({ path, label }: { path: string; label: string }) {
  const [content, setContent] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [expanded, setExpanded] = useState(false)

  const load = async () => {
    if (content !== null) {
      setExpanded(!expanded)
      return
    }
    setLoading(true)
    try {
      const res = await fetch(path)
      if (res.ok) {
        setContent(await res.text())
        setExpanded(true)
      } else {
        setContent('*File not found. Run `npm run sync` to copy data files.*')
        setExpanded(true)
      }
    } catch {
      setContent('*Error loading file. Run `npm run sync` to copy data files.*')
      setExpanded(true)
    }
    setLoading(false)
  }

  return (
    <div className="rounded-xl border border-border overflow-hidden">
      <button
        onClick={load}
        className="w-full flex items-center justify-between px-5 py-3.5 bg-card hover:bg-[#1a1a1a] transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <svg className="w-4 h-4 text-neutral-500" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
          <span className="text-[15px] font-medium text-white">{label}</span>
        </div>
        <div className="flex items-center gap-2">
          {loading && <div className="w-4 h-4 border-2 border-neutral-600 border-t-neutral-300 rounded-full animate-spin" />}
          <svg
            className={`w-4 h-4 text-neutral-500 transition-transform ${expanded ? 'rotate-180' : ''}`}
            fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </button>
      {expanded && content && (
        <div className="px-5 py-4 border-t border-border bg-[#0d0d0d] max-h-[600px] overflow-y-auto">
          <div className="prose">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  )
}

// --- QG Iteration Timeline ---
function QGTimeline() {
  const iterations = [
    { iter: 1, mode: 'Explore', theory: 'CCT', score: 5.0, note: 'First attempt — turned out to be a relabeling of existing work' },
    { iter: 2, mode: 'Explore', theory: 'EPG', score: 7.2, note: 'Scored high initially — later demolished under scrutiny' },
    { iter: 3, mode: 'Explore', theory: 'NCG-Causal', score: 5.7, note: 'Noncommutative causal geometry' },
    { iter: 4, mode: 'Explore', theory: 'TGD', score: 5.8, note: 'Thermodynamic approach to geometry' },
    { iter: 5, mode: 'Explore', theory: 'DQCP', score: 7.3, note: 'Highest initial score — led to the fracton connection' },
    { iter: 6, mode: 'Explore', theory: 'FDCG', score: 7.3, note: 'The one that survived — fracton dipole condensate gravity' },
    { iter: 7, mode: 'Explore', theory: 'CG', score: 6.7, note: 'Carroll = fracton algebra connection discovered' },
    { iter: 8, mode: 'Explore', theory: 'GDG', score: 5.7, note: 'Gravitational decoherence — last exploration iteration' },
    { iter: 9, mode: 'Verify', theory: 'FDCG', score: 6.5, note: 'First math check: graviton propagator reproduced' },
    { iter: 10, mode: 'Verify', theory: 'FDCG', score: 6.5, note: 'Gauge enhancement: contested, then proven' },
    { iter: 11, mode: 'Verify', theory: 'FDCG', score: 7.0, note: 'Condensation type: s-wave preferred (75-80%)' },
    { iter: 12, mode: 'Verify', theory: 'FDCG', score: 6.5, note: 'Found a problem: extra scalar particle needs explaining' },
    { iter: 13, mode: 'Verify', theory: 'DQCP', score: 5.0, note: 'DQCP demolished: fails 5 of 6 structural criteria' },
    { iter: 14, mode: 'Verify', theory: 'EPG', score: 5.5, note: 'EPG demolished: fundamental math problem with spin' },
    { iter: 15, mode: 'Verify', theory: 'FDCG', score: 7.0, note: 'Lorentz symmetry: effectively emerges at 75-80%' },
    { iter: 16, mode: 'Verify', theory: 'FDCG', score: 6.8, note: 'Speed of light calculation: double suppression mechanism' },
    { iter: 17, mode: 'Final', theory: 'ALL', score: null, note: 'Final report. FDCG leads. 1 of 8 survived.' },
  ]

  return (
    <div className="space-y-1">
      <div className="flex items-center gap-4 text-xs text-neutral-500 mb-3 px-2">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-1.5 rounded bg-indigo-500" />
          <span>Exploration (new ideas)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-1.5 rounded bg-amber-500" />
          <span>Verification (math checks)</span>
        </div>
      </div>
      {iterations.map(it => {
        const isExplore = it.mode === 'Explore'
        const isFinal = it.mode === 'Final'
        const barColor = isFinal ? '#6b7280' : isExplore ? '#6366f1' : '#f59e0b'
        const scorePct = it.score ? (it.score / 10) * 100 : 0

        return (
          <div key={it.iter} className="flex items-center gap-3 group hover:bg-[#111] rounded-lg px-2 py-1.5 transition-colors">
            <div className="text-xs text-neutral-600 w-6 text-right font-mono">{it.iter}</div>
            <div
              className="w-14 text-[10px] text-center py-0.5 rounded font-medium"
              style={{ background: `${barColor}20`, color: barColor }}
            >
              {it.mode}
            </div>
            <div className="text-xs text-neutral-400 w-16 truncate font-medium">{it.theory}</div>
            <div className="flex-1 h-4 bg-[#0f0f0f] rounded overflow-hidden relative">
              {it.score && (
                <div
                  className="h-full rounded"
                  style={{ width: `${scorePct}%`, background: barColor, opacity: 0.5 }}
                />
              )}
              <div className="absolute inset-0 flex items-center px-2 text-[10px] text-neutral-400">
                {it.score ? `${it.score.toFixed(1)}` : '--'}
              </div>
            </div>
            <div className="text-xs text-neutral-500 w-72 truncate hidden lg:block">{it.note}</div>
          </div>
        )
      })}
    </div>
  )
}

// --- Agent Roles Panel ---
function AgentRolesPanel({ roles }: { roles: Project['methodology']['agentRoles'] }) {
  if (roles.length === 0) return <div className="text-[15px] text-neutral-500">No agents — this was a one-shot generation and scoring exercise, not an iterative loop.</div>

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      {roles.map(agent => (
        <div key={agent.name} className="rounded-lg bg-[#0f0f0f] p-4 border border-border/50">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg" dangerouslySetInnerHTML={{ __html: agent.icon }} />
            <span className="text-[15px] font-semibold text-white">{agent.name}</span>
          </div>
          <div className="text-[13px] text-neutral-400 leading-relaxed">{agent.role}</div>
        </div>
      ))}
    </div>
  )
}

// ============================================================
// MAIN PROJECT PAGE
// ============================================================

export default function ProjectPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const project = getProject(projectId ?? '')

  const [activeTab, setActiveTab] = useState('Overview')

  if (!project) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-bold text-white mb-2">Project Not Found</div>
          <Link to="/" className="text-blue-400 hover:text-blue-300 text-sm">Back to Science Research HQ</Link>
        </div>
      </div>
    )
  }

  const tabs = project.id === 'worldviews'
    ? ['Overview', 'Methodology', 'Rankings', 'Promising Leads', 'Documents']
    : project.id === 'dqcp'
    ? ['Overview', 'Methodology', 'Evidence', 'Process', 'Promising Leads', 'Documents']
    : project.id === 'grand-unified'
    ? ['Overview', 'Methodology', 'Status', 'Process', 'Promising Leads', 'Documents']
    : ['Overview', 'Methodology', 'Theories', 'Process', 'Promising Leads', 'Documents']

  return (
    <div className="min-h-screen bg-bg">
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-neutral-500 hover:text-neutral-300 transition-colors mb-4">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Science Research HQ
          </Link>
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white mb-2">{project.name}</h1>
              <p className="text-[15px] text-neutral-400 max-w-2xl leading-relaxed">{project.description}</p>
              <div className="flex items-center gap-4 mt-2 text-[13px] text-neutral-600">
                <span>Started {project.dateStarted}</span>
                <span>&middot;</span>
                <span>Last ran {project.dateLastRan}</span>
              </div>
            </div>
            <StatusBadge status={project.status} />
          </div>

          {/* Key Stats */}
          <div className="flex gap-4 mt-4">
            {project.keyStats.map(stat => (
              <div key={stat.label} className="bg-card rounded-lg px-4 py-2.5 border border-border">
                <div className="text-[10px] text-neutral-500 uppercase tracking-wider mb-0.5">{stat.label}</div>
                <div className="text-[15px] font-bold text-white">{stat.value}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Tabs */}
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

        {/* Tab Content */}
        <div className="min-h-[400px]">
          {/* OVERVIEW TAB */}
          {activeTab === 'Overview' && (
            <div className="space-y-6">
              {/* What was the goal? */}
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-3">How This Loop Works</h2>
                <p className="text-[15px] text-neutral-400 leading-relaxed">{project.methodology.summary}</p>
              </div>

              {/* Key Innovation + Key Lesson */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div className="rounded-xl border border-border bg-card p-6">
                  <div className="text-xs text-neutral-500 uppercase tracking-wider mb-2">What Made This Loop Different</div>
                  <p className="text-[15px] text-neutral-300 leading-relaxed">{project.methodology.keyInnovation}</p>
                </div>
                <div className="rounded-xl border border-border bg-card p-6">
                  <div className="text-xs text-neutral-500 uppercase tracking-wider mb-2">Biggest Takeaway</div>
                  <p className="text-[15px] text-neutral-300 leading-relaxed">{project.methodology.keyLesson}</p>
                </div>
              </div>

              {/* Process Flow (compact) */}
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-4">Process Flow</h2>
                <ProcessFlow phases={project.methodology.processPhases} />
              </div>
            </div>
          )}

          {/* METHODOLOGY TAB */}
          {activeTab === 'Methodology' && (
            <div className="space-y-6">
              {/* Loop Structure */}
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-3">Loop Architecture</h2>
                <p className="text-[15px] text-neutral-400 leading-relaxed mb-6">{project.methodology.summary}</p>

                <h3 className="text-[15px] font-semibold text-white mb-3">Agent Roles</h3>
                <AgentRolesPanel roles={project.methodology.agentRoles} />
              </div>

              {/* Process Diagram */}
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-4">Iteration Cycle</h2>
                <ProcessFlow phases={project.methodology.processPhases} />
              </div>

              {/* State Files */}
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-3">State Files (How the Loop Remembers)</h2>
                <p className="text-[13px] text-neutral-500 mb-4">Each loop uses persistent files to maintain context across iterations. These are the agent's "memory."</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {project.files.map(file => (
                    <div key={file.path} className="rounded-lg bg-[#0f0f0f] px-4 py-3 border border-border/50">
                      <div className="text-[15px] font-medium text-white mb-1">{file.label}</div>
                      <div className="text-[11px] text-neutral-600 font-mono">{file.path}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Innovation + Lesson */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-5">
                  <div className="text-xs font-medium text-emerald-400 uppercase tracking-wider mb-2">Design Innovation</div>
                  <p className="text-[15px] text-neutral-300 leading-relaxed">{project.methodology.keyInnovation}</p>
                </div>
                <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-5">
                  <div className="text-xs font-medium text-amber-400 uppercase tracking-wider mb-2">Design Lesson</div>
                  <p className="text-[15px] text-neutral-300 leading-relaxed">{project.methodology.keyLesson}</p>
                </div>
              </div>
            </div>
          )}

          {/* THEORIES TAB (QG Loop) */}
          {activeTab === 'Theories' && project.theories && (
            <div className="space-y-6">
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-1">Theory Scoreboard</h2>
                <p className="text-[13px] text-neutral-500 mb-6">8 theories were explored. The light bars show how they scored when first proposed. The solid bars show how they scored after mathematical scrutiny. Only one survived above 6.5.</p>
                <TheoryScoreChart theories={project.theories} />
              </div>

              {/* Key Insight */}
              <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-5">
                <div className="text-[15px] font-medium text-amber-300 mb-1">"Ideas look brilliant until you check the math"</div>
                <div className="text-[13px] text-neutral-300 leading-relaxed">
                  Every theory scored 7+ when first proposed — the agents were enthusiastic about each one. But when the Verification mode asked "show me the actual equations," scores dropped to 5-6.5. Two theories were completely demolished: DQCP Gravity (7.3 down to 5.0) and EPG (7.2 down to 5.5). <strong className="text-white">The only theory that survived was the one built on concrete math at every step.</strong> This is the single most important lesson for loop design: always build in a verification phase.
                </div>
              </div>
            </div>
          )}

          {/* EVIDENCE TAB (DQCP) */}
          {activeTab === 'Evidence' && project.id === 'dqcp' && (
            <div className="rounded-xl border border-border bg-card p-6">
              <h2 className="text-base font-semibold text-white mb-1">Evidence Assessment</h2>
              <p className="text-[13px] text-neutral-500 mb-6">The agents checked 6 structural criteria and found 5 failures. Then they analyzed what type of transition it IS instead.</p>
              <DQCPEvidencePanel />
            </div>
          )}

          {/* STATUS TAB (GUT) */}
          {activeTab === 'Status' && project.id === 'grand-unified' && (
            <GUTActiveStatus />
          )}

          {/* RANKINGS TAB (Worldviews) */}
          {activeTab === 'Rankings' && project.id === 'worldviews' && (
            <WorldviewsOverview />
          )}

          {/* PROCESS TAB */}
          {activeTab === 'Process' && (
            <div className="space-y-6">
              {project.id === 'quantum-gravity' && (
                <div className="rounded-xl border border-border bg-card p-6">
                  <h2 className="text-base font-semibold text-white mb-1">Iteration Timeline</h2>
                  <p className="text-[13px] text-neutral-500 mb-4">17 iterations total. First 8 explored new ideas (purple). Next 8 verified existing ones with math (amber). Notice how scores drop in verification mode.</p>
                  <QGTimeline />
                </div>
              )}

              {project.id === 'dqcp' && (
                <div className="rounded-xl border border-border bg-card p-6">
                  <h2 className="text-base font-semibold text-white mb-4">How the Investigation Unfolded</h2>
                  <p className="text-[13px] text-neutral-500 mb-6">4 phases designed to reach a verdict as fast as possible. Phase 3 was skipped entirely because the failures were already conclusive.</p>
                  <div className="space-y-6">
                    {[
                      {
                        phase: 'Phase 1: Define the Problem (Iterations 1-2)',
                        result: 'Precisely defined both sides of the question. Identified what the system looks like before and after the transition, and what properties each side has.',
                        confidence: '90%',
                        agents: '5 specialized agents: one for each side, one for literature, one skeptic, one analogy-mapper',
                        color: '#22d3ee',
                      },
                      {
                        phase: 'Phase 2: Check the Requirements (Iteration 3)',
                        result: '5 of 6 required criteria failed. The analogy mapping showed only 4 of 12 expected parallels matched. Confidence in a "yes" answer dropped to 12%.',
                        confidence: '88%',
                        agents: 'Skeptic led with 7 structural objections. Domain Expert and Literature Scout confirmed.',
                        color: '#2dd4bf',
                      },
                      {
                        phase: 'Phase 3: Detailed Math (Skipped)',
                        result: 'Skipped — the structural failures from Phase 2 were enough to reach a verdict without detailed calculations. This is the fail-fast design working as intended.',
                        confidence: 'N/A',
                        agents: 'N/A',
                        color: '#4ade80',
                      },
                      {
                        phase: 'Phase 4: Final Verdict (Iteration 4)',
                        result: 'Ruled Out at 95% confidence. The probability of the original hypothesis being correct dropped to 3.6%. However, the investigation did identify what kind of transition it IS instead.',
                        confidence: '95%',
                        agents: '4 agents debated the transition type from different angles, then converged on a probability distribution.',
                        color: '#f97316',
                      },
                    ].map((p, i) => (
                      <div key={i} className="flex gap-4">
                        <div
                          className="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-sm shrink-0"
                          style={{ background: p.color }}
                        >
                          {i + 1}
                        </div>
                        <div className="flex-1">
                          <div className="text-[15px] font-semibold text-white mb-1">{p.phase}</div>
                          <div className="text-[13px] text-neutral-400 leading-relaxed mb-2">{p.result}</div>
                          <div className="flex gap-4 text-[13px]">
                            <span className="text-neutral-500">Confidence: <span className="text-neutral-300">{p.confidence}</span></span>
                            <span className="text-neutral-500">Agents: <span className="text-neutral-300">{p.agents}</span></span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {project.id === 'grand-unified' && (
                <div className="rounded-xl border border-border bg-card p-6">
                  <h2 className="text-base font-semibold text-white mb-4">Three-Phase Cycle</h2>
                  <div className="space-y-6">
                    <div className="flex items-center justify-center gap-4 flex-wrap mb-8">
                      {[
                        { name: 'Phase A\nTheorize', color: '#10b981', active: false },
                        { name: 'Phase B\nInvestigate', color: '#34d399', active: true },
                        { name: 'Phase C\nVerdict', color: '#6ee7b7', active: false },
                      ].map((phase, i) => (
                        <div key={i} className="flex items-center gap-3">
                          <div
                            className={`w-28 h-28 rounded-2xl flex items-center justify-center text-center text-sm font-bold text-white shadow-lg ${
                              phase.active ? 'ring-2 ring-offset-2 ring-offset-bg' : 'opacity-60'
                            }`}
                            style={{
                              background: phase.color,
                              boxShadow: phase.active ? `0 0 30px ${phase.color}40` : 'none',
                            }}
                          >
                            <span className="whitespace-pre-line">{phase.name}</span>
                          </div>
                          {i < 2 && (
                            <svg className="w-6 h-6 text-neutral-600" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                            </svg>
                          )}
                        </div>
                      ))}
                    </div>

                    <div className="text-[15px] text-neutral-400 leading-relaxed">
                      <strong className="text-white">Iteration 1 (Complete):</strong> Phase A generated 4 candidate approaches for the question "where do the other forces come from?" Three evaluation agents (Plausibility, Novelty, Feasibility) unanimously selected <strong className="text-white">Multi-Species Fracton Compositeness</strong> — the idea that multiple types of fractons, when they condense, break both spatial and internal symmetries simultaneously, potentially producing force-carrying particles.
                    </div>
                    <div className="text-[15px] text-neutral-400 leading-relaxed">
                      <strong className="text-white">Next (Iteration 2):</strong> Phase B investigation — compute whether 2 species of fractons can produce the right kind of force-carrying particles (spin-1 Goldstone bosons). This is the critical test: success means forces emerge from fractons, failure means back to Phase A with new constraints.
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* PROMISING LEADS TAB */}
          {activeTab === 'Promising Leads' && (
            <div className="space-y-6">
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-1">What's Worth Investigating Further</h2>
                <p className="text-[13px] text-neutral-500 mb-6">The most exciting findings from this project — things that survived scrutiny or opened new doors.</p>
                <PromisingLeads leads={project.promisingLeads} />
              </div>

              {/* Loop Design Findings */}
              <div className="rounded-xl border border-border bg-card p-6">
                <h2 className="text-base font-semibold text-white mb-1">Loop Design Findings</h2>
                <p className="text-[13px] text-neutral-500 mb-4">What we learned about building better autonomous research loops from running this one.</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {project.id === 'quantum-gravity' && [
                    { title: 'What worked', items: ['5-agent parallel evaluation catches blind spots', 'Dual-mode (explore/verify) exposes score inflation', 'The Skeptic agent prevented groupthink'] },
                    { title: 'What to change next time', items: ['Start verification earlier (not at iteration 9)', 'Require math proof in exploration mode too', 'Use the handoff document for more structured mode transitions'] },
                  ].map((section, i) => (
                    <div key={i} className="rounded-lg bg-[#0f0f0f] p-4">
                      <div className="text-[15px] font-medium text-white mb-2">{section.title}</div>
                      <ul className="space-y-1.5">
                        {section.items.map((item, j) => (
                          <li key={j} className="text-[13px] text-neutral-400 flex items-start gap-2">
                            <span className="text-neutral-600 mt-0.5">{i === 0 ? '\u2713' : '\u2192'}</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                  {project.id === 'dqcp' && [
                    { title: 'What worked', items: ['Fail-fast design saved 11 iterations', 'Custom agents per phase outperformed fixed roles', 'Clear verdict criteria made the decision objective'] },
                    { title: 'What to change next time', items: ['Could have been even faster with parallel criteria checking', 'The "skip phase" logic should be automated, not agent-decided', 'Add a "serendipity" check before closing — we almost missed the novel calculation'] },
                  ].map((section, i) => (
                    <div key={i} className="rounded-lg bg-[#0f0f0f] p-4">
                      <div className="text-[15px] font-medium text-white mb-2">{section.title}</div>
                      <ul className="space-y-1.5">
                        {section.items.map((item, j) => (
                          <li key={j} className="text-[13px] text-neutral-400 flex items-start gap-2">
                            <span className="text-neutral-600 mt-0.5">{i === 0 ? '\u2713' : '\u2192'}</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                  {project.id === 'grand-unified' && [
                    { title: 'What worked', items: ['Living knowledge document prevents going in circles', 'Building on 12 prior established results gives a head start', 'Three-phase cycle is clean and easy to follow'] },
                    { title: 'What to change next time', items: ['Knowledge document may get too large for context — need a summary layer', 'Dead ends need richer documentation of WHY they failed', 'Need a mechanism for the loop to question its own established results'] },
                  ].map((section, i) => (
                    <div key={i} className="rounded-lg bg-[#0f0f0f] p-4">
                      <div className="text-[15px] font-medium text-white mb-2">{section.title}</div>
                      <ul className="space-y-1.5">
                        {section.items.map((item, j) => (
                          <li key={j} className="text-[13px] text-neutral-400 flex items-start gap-2">
                            <span className="text-neutral-600 mt-0.5">{i === 0 ? '\u2713' : '\u2192'}</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                  {project.id === 'worldviews' && [
                    { title: 'What worked', items: ['Systematic enumeration ensures complete coverage', 'Scoring criteria made comparison objective', 'Revealed that rigor always beats speculation'] },
                    { title: 'What to change next time', items: ['Run a verification loop on the top 8 worldviews', 'Use the 8 theories of time as inputs to a focused research loop', 'Use adversarial worldviews as stress-tests for future theories'] },
                  ].map((section, i) => (
                    <div key={i} className="rounded-lg bg-[#0f0f0f] p-4">
                      <div className="text-[15px] font-medium text-white mb-2">{section.title}</div>
                      <ul className="space-y-1.5">
                        {section.items.map((item, j) => (
                          <li key={j} className="text-[13px] text-neutral-400 flex items-start gap-2">
                            <span className="text-neutral-600 mt-0.5">{i === 0 ? '\u2713' : '\u2192'}</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* DOCUMENTS TAB */}
          {activeTab === 'Documents' && (
            <div className="space-y-3">
              <p className="text-[13px] text-neutral-500 mb-4">Click to expand and read the actual research documents produced by the loop. Data is synced from the project directories.</p>
              {project.files.map(file => (
                <MarkdownViewer key={file.path} path={file.path} label={file.label} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
