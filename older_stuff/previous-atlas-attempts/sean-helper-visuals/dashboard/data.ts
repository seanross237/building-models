export type ProjectStatus = 'active' | 'completed' | 'reference'

export interface TheoryScore {
  name: string
  explorationScore: number
  verificationScore: number | null
  status: string
  iteration: number
}

export interface IterationData {
  iteration: number
  mode: string
  topic: string
  result: string
}

export interface ProcessPhase {
  name: string
  description: string
  color: string
}

export interface Project {
  id: string
  name: string
  shortName: string
  status: ProjectStatus
  dateStarted: string
  dateLastRan: string
  description: string
  keyStats: { label: string; value: string }[]
  methodology: {
    summary: string
    agentRoles: { name: string; role: string; icon: string }[]
    processPhases: ProcessPhase[]
    keyInnovation: string
    keyLesson: string
  }
  promisingLeads: { title: string; description: string; status: string }[]
  files: { label: string; path: string }[]
  theories?: TheoryScore[]
  accent: string
}

export const projects: Project[] = [
  {
    id: 'quantum-gravity',
    name: 'Quantum Gravity Research Loop',
    shortName: 'QG Loop',
    status: 'completed',
    dateStarted: 'March 20, 2026',
    dateLastRan: 'March 20, 2026',
    description: 'Our first research loop — explored 8 different theories by having 5 AI agents attack each one from different angles. Learned that ideas score high when first proposed but crumble under mathematical scrutiny. Only 1 of 8 theories survived verification.',
    keyStats: [
      { label: 'Total Iterations', value: '17' },
      { label: 'Theories Explored', value: '8' },
      { label: 'Survived Scrutiny', value: '1 of 8' },
      { label: 'Agent Calls', value: '~80' },
    ],
    methodology: {
      summary: 'The loop reads its accumulated knowledge, picks a research direction, brainstorms 3 candidate ideas, selects the best, then launches 5 parallel agents to develop and stress-test it. Each agent has a different job — one builds the math, one tries to break it, one checks the history, etc. After iteration 8, we added a second mode: "Verification" — where instead of exploring new ideas, the agents do deep mathematical checks on existing ones. This is where most theories fell apart.',
      agentRoles: [
        { name: 'Theorist', role: 'Builds the formal math — writes equations and proves things step by step', icon: '&#x1D4E3;' },
        { name: 'Experimentalist', role: 'Asks: "How would we actually test this?" — finds observable predictions', icon: '&#x1F52C;' },
        { name: 'Historian', role: 'Checks if this idea already exists or violates known results', icon: '&#x1F4DA;' },
        { name: 'Skeptic', role: 'Tries to DESTROY the theory — finds fatal flaws and hidden assumptions. The MVP.', icon: '&#x2694;' },
        { name: 'Synthesizer', role: 'Finds unexpected connections to other fields and ideas', icon: '&#x1F517;' },
      ],
      processPhases: [
        { name: 'Read State', description: 'Agent reads everything it has learned so far — past theories, dead ends, scores, and cross-connections', color: '#6366f1' },
        { name: 'Choose Direction', description: 'Picks which category to explore next (8 categories like "Spacetime Emergence" or "Radical Departures")', color: '#8b5cf6' },
        { name: 'Brainstorm 3 Ideas', description: 'Generates 3 candidate theories, each with a core idea, key mechanism, testable prediction, and potential fatal flaw', color: '#a855f7' },
        { name: 'Multi-Agent Deep Dive', description: '5 parallel agents each examine the best idea from their specialized angle', color: '#d946ef' },
        { name: 'Score & Synthesize', description: 'Combine all agent findings and score the theory on 6 criteria (novelty, consistency, testability, etc.)', color: '#ec4899' },
        { name: 'Update Knowledge', description: 'Write everything learned back to persistent state files so the next iteration can build on it', color: '#f43f5e' },
      ],
      keyInnovation: 'Dual-mode operation — the loop switches between "Exploration" (generating new ideas) and "Verification" (doing the math on existing ones). The handoff document recommends which mode to use next based on current scores.',
      keyLesson: '"Exploration inflates, verification deflates." Every idea looked brilliant when first proposed (scores 7+) and crumbled under math (scores dropped to 5-6.5). The Skeptic agent was the most valuable — always include one whose job is to disagree.',
    },
    promisingLeads: [
      {
        title: 'FDCG: Spacetime from particles that move in pairs',
        description: 'The leading theory proposes that spacetime is made of particles called "fractons" that can\'t move individually but can move in pairs. When these pairs condense (like water vapor condensing into liquid), the graviton — gravity\'s carrier particle — emerges naturally. The math actually reproduced Einstein\'s gravity equations. That\'s a real result.',
        status: 'Lead theory',
      },
      {
        title: 'Carroll = Fracton algebra connection',
        description: 'Discovered that "Carrollian" geometry (a known mathematical structure from the 1960s) is secretly the same math as fracton physics. This was independently confirmed by a 2023 published paper. When two different paths lead to the same math, that\'s usually a good sign.',
        status: 'Confirmed',
      },
      {
        title: 'Oppenheim prediction for gravitational noise',
        description: 'The theory makes a specific, testable prediction about gravitational noise that could be measured by future experiments. This is the kind of concrete prediction that separates real theories from handwaving.',
        status: 'Testable',
      },
    ],
    files: [
      { label: 'Research Protocol', path: '/data/quantum-gravity/PROMPT.md' },
      { label: 'Final Report', path: '/data/quantum-gravity/FINAL-REPORT.md' },
      { label: 'Theory Catalog', path: '/data/quantum-gravity/THEORIES.md' },
      { label: 'Handoff', path: '/data/quantum-gravity/HANDOFF.md' },
    ],
    theories: [
      { name: 'FDCG (Fracton Dipole Condensate Gravity)', explorationScore: 7.3, verificationScore: 6.8, status: 'SURVIVED', iteration: 6 },
      { name: 'Carrollian Geometrogenesis (CG)', explorationScore: 6.7, verificationScore: null, status: 'Untested', iteration: 7 },
      { name: 'Thermodynamic Geometry Duality (TGD)', explorationScore: 5.8, verificationScore: null, status: 'Untested', iteration: 4 },
      { name: 'NCG-Causal Geometry', explorationScore: 5.7, verificationScore: null, status: 'Untested', iteration: 3 },
      { name: 'Gravitational Decoherence (GDG)', explorationScore: 5.7, verificationScore: null, status: 'Untested', iteration: 8 },
      { name: 'Entanglement Phase Gravity (EPG)', explorationScore: 7.2, verificationScore: 5.5, status: 'Demolished', iteration: 2 },
      { name: 'DQCP Gravity', explorationScore: 7.3, verificationScore: 5.0, status: 'Demolished', iteration: 5 },
      { name: 'Causal Condensate Theory (CCT)', explorationScore: 5.0, verificationScore: null, status: 'Not novel', iteration: 1 },
    ],
    accent: '#3b82f6',
  },
  {
    id: 'dqcp',
    name: 'DQCP Formalization',
    shortName: 'DQCP',
    status: 'completed',
    dateStarted: 'March 20, 2026',
    dateLastRan: 'March 20, 2026',
    description: 'A focused loop designed to answer ONE specific question. Instead of exploring broadly, we gave the agents a yes/no question with clear success criteria. They answered it definitively in 4 iterations (out of a max of 15) and stopped early. Proof that focused questions resolve way faster than open-ended exploration.',
    keyStats: [
      { label: 'Iterations Used', value: '4 of 15' },
      { label: 'Final Verdict', value: 'Ruled Out' },
      { label: 'Confidence', value: '95%' },
      { label: 'Agents Used', value: '9' },
    ],
    methodology: {
      summary: 'Unlike the QG Loop (broad exploration), this loop had ONE job: answer a specific yes/no question. The process had 4 phases — Characterize the problem, Check the key criteria, Compute the details, Deliver a verdict. Instead of using fixed agent roles, we picked custom agents for each phase based on what expertise was needed. The loop was designed to stop early if the answer became obvious — and it did, at iteration 4 of 15.',
      agentRoles: [
        { name: 'Calculator', role: 'Does the actual math — step-by-step derivations and computations', icon: '&#x1F9EE;' },
        { name: 'Checker', role: 'Independently re-derives using a different method to verify results', icon: '&#x2705;' },
        { name: 'Literature Scout', role: 'Finds published research to compare against — are our results consistent?', icon: '&#x1F4D6;' },
        { name: 'Skeptic', role: 'Finds errors, hidden assumptions, and edge cases in the analysis', icon: '&#x2694;' },
        { name: 'Domain Expert', role: 'Compares against known examples in the same field to sanity-check', icon: '&#x1F9CA;' },
      ],
      processPhases: [
        { name: 'Phase 1: Characterize', description: 'Precisely define both sides of the question. What are we comparing? What would success vs. failure look like?', color: '#22d3ee' },
        { name: 'Phase 2: Check Key Criteria', description: 'Test the specific structural requirements. Does this thing have the properties it needs to work?', color: '#2dd4bf' },
        { name: 'Phase 3: Compute Details', description: 'If criteria pass, do the detailed math. If criteria fail, skip this phase.', color: '#4ade80' },
        { name: 'Phase 4: Verdict', description: 'Deliver a clear answer: Confirmed / Likely / Unlikely / Ruled Out. Include confidence level.', color: '#f97316' },
      ],
      keyInnovation: 'Designed to fail fast — if the answer is clearly NO, stop early instead of burning through all 15 iterations. Clear success/failure criteria defined upfront so the agents know when they are done.',
      keyLesson: 'A well-defined question with clear success/failure criteria can be answered in 4 iterations. Broad exploration of the same topic took 17. Focus beats breadth for answerable questions.',
    },
    promisingLeads: [
      {
        title: 'Novel calculation: Coleman-Weinberg for rank-2 gauge theories',
        description: 'While the main question was ruled out, the investigation produced a potentially unpublished calculation (Coleman-Weinberg effective potential for rank-2 gauge theories). This is a mathematical tool that could be useful for other researchers in the field.',
        status: 'Possibly novel',
      },
      {
        title: 'The transition is a "fracton Higgs" mechanism',
        description: 'The investigation determined the transition isn\'t a DQCP, but it IS a Higgs mechanism for fractons — similar to how the Higgs boson gives mass to particles, but for this exotic system. This is a genuinely interesting physical result in its own right.',
        status: 'Worth pursuing',
      },
    ],
    files: [
      { label: 'Research Protocol', path: '/data/dqcp/PROMPT.md' },
      { label: 'Results Catalog', path: '/data/dqcp/RESULTS.md' },
      { label: 'Final Verdict', path: '/data/dqcp/FINAL-VERDICT.md' },
      { label: 'Handoff', path: '/data/dqcp/HANDOFF.md' },
    ],
    accent: '#3b82f6',
  },
  {
    id: 'grand-unified',
    name: 'Grand Unified Theory Builder',
    shortName: 'GUT Builder',
    status: 'active',
    dateStarted: 'March 20, 2026',
    dateLastRan: 'March 21, 2026',
    description: 'Our most sophisticated loop — designed to go DEEP on one idea instead of exploring many. Uses a "living knowledge document" that accumulates everything the agents learn, so they never go in circles. Three-phase cycle: Theorize (brainstorm), Investigate (do the math), Verdict (update knowledge). Built on the winning theory from the QG Loop.',
    keyStats: [
      { label: 'Iteration', value: '1 of 50' },
      { label: 'Current Phase', value: 'Investigate' },
      { label: 'Established Results', value: '12' },
      { label: 'Dead Ends Found', value: '3' },
    ],
    methodology: {
      summary: 'Three-phase cycle: Phase A (Theorize) generates candidate approaches and has 3 evaluation agents pick the best. Phase B (Investigate) does the actual math with a Calculator, Checker, and Skeptic. Phase C (Verdict) updates the living knowledge document — if it worked, it goes in "Established Results"; if it failed, it goes in "Dead Ends" so the loop never revisits it. The knowledge document is the key innovation — it is the agent\'s memory across iterations.',
      agentRoles: [
        { name: 'Plausibility', role: 'Evaluates which candidate ideas have solid mathematical foundations', icon: '&#x1F3AF;' },
        { name: 'Novelty', role: 'Evaluates which candidates propose something genuinely new vs. rehashing old ideas', icon: '&#x2728;' },
        { name: 'Feasibility', role: 'Evaluates which candidates can actually be computed and tested', icon: '&#x1F527;' },
        { name: 'Calculator', role: 'Does the actual math in the Investigation phase', icon: '&#x1F9EE;' },
        { name: 'Skeptic', role: 'Always adversarial — finds errors, hidden assumptions, and logical gaps', icon: '&#x2694;' },
      ],
      processPhases: [
        { name: 'Phase A: Theorize', description: 'Survey the knowledge doc, identify an open question, brainstorm 3-5 candidates, have 3 agents evaluate, pick the best 1-2', color: '#10b981' },
        { name: 'Phase B: Investigate', description: 'Define a precise problem with clear success/failure conditions. Launch Calculator + Checker + Skeptic. May take multiple iterations.', color: '#34d399' },
        { name: 'Phase C: Verdict', description: 'If it worked: add to Established Results and identify the next frontier. If it failed: add to Dead Ends, return to Phase A with new constraints.', color: '#6ee7b7' },
      ],
      keyInnovation: 'The living knowledge document (GRAND-THEORY.md) is the agent\'s persistent memory. It accumulates established results, dead ends, open questions, and next steps. This prevents the agent from going in circles and lets it build on its own prior work.',
      keyLesson: 'Building on a foundation of prior results (12 established from earlier loops) gives the agent a huge head start. The persistent knowledge document is the most important piece of the architecture.',
    },
    promisingLeads: [
      {
        title: 'Nonlinear gravity reproduced from fractons',
        description: 'The theory now reproduces the full nonlinear version of Einstein\'s gravity (not just the simplified "linearized" version). Getting the full nonlinear theory to emerge is a major milestone — most competing approaches only manage the simplified version.',
        status: 'Established',
      },
      {
        title: 'Where do the other forces come from? Topological defects.',
        description: 'The leading candidate for where electromagnetism and the nuclear forces come from: topological defects (like cracks or twists) in the fracton "crystal" that makes up spacetime. Each type of defect could correspond to a different force.',
        status: 'Investigating',
      },
      {
        title: 'Skyrmions as the origin of matter',
        description: 'Skyrmions — stable topological structures that already appear in condensed matter physics — could explain where matter (protons, neutrons, electrons) comes from. The math of Skyrmions naturally produces the right kind of particle-like objects.',
        status: 'Promising',
      },
    ],
    files: [
      { label: 'Research Protocol', path: '/data/grand-unified/PROMPT.md' },
      { label: 'Knowledge Document', path: '/data/grand-unified/GRAND-THEORY.md' },
      { label: 'Calculations', path: '/data/grand-unified/CALCULATIONS.md' },
      { label: 'Handoff', path: '/data/grand-unified/HANDOFF.md' },
    ],
    accent: '#10b981',
  },
  {
    id: 'worldviews',
    name: 'Worldviews',
    shortName: 'Worldviews',
    status: 'reference',
    dateStarted: 'March 2026',
    dateLastRan: 'March 2026',
    description: 'Not an agent loop — a one-shot exhaustive enumeration exercise. We asked the AI to systematically generate 100 alternative approaches across 6 categories and score each one on 8 criteria. The takeaway: generating lots of ideas is easy; the top scorers were all ideas that already had real math behind them. Quantity does not beat rigor.',
    keyStats: [
      { label: 'Ideas Generated', value: '100' },
      { label: 'Categories', value: '6' },
      { label: 'Scoring Criteria', value: '8' },
      { label: 'Top Score', value: '27/35' },
    ],
    methodology: {
      summary: 'A systematic enumeration — not a loop. Started with 20 core concepts, generated 4 alternative interpretations of each, plus 8 theories of time. Combined these into 100 worldviews across 6 categories: Pure (8), Pairwise Hybrids (28), Focused Deep Dives (20), Problem-Targeted (20), Adversarial (12), Wild Cards (12). Each scored on 8 criteria (max 35 points). No agents, no iterations — just one big generation + evaluation pass.',
      agentRoles: [],
      processPhases: [
        { name: 'Identify Core Concepts', description: 'Define 20 foundational concepts that any approach needs to address', color: '#6b7280' },
        { name: 'Generate Alternatives', description: 'For each concept, brainstorm 4 alternative interpretations. Plus 8 different theories of time.', color: '#9ca3af' },
        { name: 'Combine into 100 Ideas', description: 'Systematically combine alternatives into 100 worldviews across 6 categories (pure, hybrid, deep dive, targeted, adversarial, wild card)', color: '#d1d5db' },
        { name: 'Score & Rank', description: '8 criteria: Does it match reality? Is it self-consistent? Is it simple? Is the math precise? Can it explain things? Does it make new predictions? Does it unify things? Is it compatible with what we know?', color: '#e5e7eb' },
      ],
      keyInnovation: 'Exhaustive enumeration forces you to consider approaches you never would have thought of. Instead of cherry-picking favorites, generate ALL combinations systematically.',
      keyLesson: 'Generating lots of ideas is cheap. The top scorers all turned out to be ideas that already had real mathematical foundations behind them. Breadth without depth is incomplete — rigor always wins.',
    },
    promisingLeads: [
      {
        title: '8 alternative theories of time — unformalised',
        description: 'The enumeration produced 8 genuinely different theories of time that nobody has tried to formalize with actual math yet. These are concrete starting points for future research loops.',
        status: 'Unexplored',
      },
      {
        title: 'CPT Boundary Condition (top-ranked worldview)',
        description: 'The highest-scoring worldview is actual published physics by Boyle, Finn, and Turok. It proposes that the Big Bang is a mirror — the universe extends backward in time symmetrically. This theory naturally predicts dark matter and has computed, testable predictions.',
        status: 'Published physics',
      },
      {
        title: 'Adversarial combinations as stress-tests',
        description: 'The 12 "adversarial" worldviews (deliberately paradoxical combinations) could serve as powerful stress-tests for any future theory. If a theory can survive these contradictions, it\'s probably robust.',
        status: 'Future use',
      },
    ],
    files: [
      { label: 'Worldview Manifest', path: '/data/worldviews/worldview_manifest.md' },
      { label: 'Core Tenets', path: '/data/worldviews/core_tenets_of_physics.md' },
      { label: 'Tenet Stability', path: '/data/worldviews/tenet_stability_assessment.md' },
      { label: 'Assessment Criteria', path: '/data/worldviews/theory-assessment-criteria.md' },
      { label: 'Rankings', path: '/data/worldviews/RANKINGS.md' },
    ],
    accent: '#6b7280',
  },
]

export function getProject(id: string): Project | undefined {
  return projects.find(p => p.id === id)
}

export function getStatusLabel(status: ProjectStatus): string {
  switch (status) {
    case 'active': return 'Active'
    case 'completed': return 'Completed'
    case 'reference': return 'Reference'
  }
}

export function getStatusColor(status: ProjectStatus): string {
  switch (status) {
    case 'active': return '#10b981'
    case 'completed': return '#3b82f6'
    case 'reference': return '#6b7280'
  }
}
