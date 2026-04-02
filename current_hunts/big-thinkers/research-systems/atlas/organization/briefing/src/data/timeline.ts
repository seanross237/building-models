export interface TimelineEntry {
  date: string;
  title: string;
  bullets: string[];
  methodology: string;
  stats?: { label: string; value: string; color: string }[];
  status: "completed" | "failed" | "milestone" | "mixed";
}

export const timeline: TimelineEntry[] = [
  {
    date: "Mar 18",
    title: "100 Worldviews Evaluated",
    bullets: [
      "Breadth-first survey: 20 physics tenets x 4 interpretations + 8 theories of time",
      "Scored all 100 on 8 criteria. Top scorer: CPT cosmological boundary condition (27/35)",
      "Unrelated frameworks genuinely converge on overlapping structures",
    ],
    methodology:
      "First use of systematic scoring rubric across a large candidate set. Proved breadth-first exploration is viable for narrowing the field.",
    stats: [
      { label: "Worldviews", value: "100", color: "#f59e0b" },
      { label: "Categories", value: "6", color: "#a855f7" },
      { label: "Top Score", value: "27/35", color: "#10b981" },
    ],
    status: "completed",
  },
  {
    date: "Mar 20",
    title: "Quantum Gravity Loop: 8 Theories",
    bullets: [
      "17 iterations with 5 parallel agents per theory (Theorist, Experimentalist, Historian, Skeptic, Synthesizer)",
      "FDCG emerged as leader at 6.8/10 — only theory to survive verification",
      "Added dual-mode operation: Exploration (generate ideas) → Verification (do the math)",
    ],
    methodology:
      "Key lesson: \"Exploration inflates, verification deflates.\" Every theory scored 7+ in exploration, dropped to 5-6.5 under math scrutiny. The Skeptic agent is the MVP.",
    stats: [
      { label: "Iterations", value: "17", color: "#6366f1" },
      { label: "Theories", value: "8", color: "#ec4899" },
      { label: "Survived", value: "1", color: "#10b981" },
      { label: "Agent Calls", value: "~80", color: "#f59e0b" },
    ],
    status: "completed",
  },
  {
    date: "Mar 20",
    title: "DQCP Ruled Out",
    bullets: [
      "Focused 4-iteration investigation: Is FDCG's transition a Deconfined Quantum Critical Point?",
      "Ruled out at 95% confidence — category mismatch, no 3+1D DQCP established",
      "Correct classification: fracton Higgs transition. FDCG itself remains valid.",
    ],
    methodology:
      "Fast failure. Took only 4 iterations to kill a theory that scored 7.3 in exploration. This is the system working correctly — adversarial agents prevent accumulation of plausible-sounding nonsense.",
    stats: [
      { label: "Iterations", value: "4", color: "#6366f1" },
      { label: "Confidence", value: "95%", color: "#ef4444" },
      { label: "Failures Found", value: "5", color: "#ef4444" },
    ],
    status: "completed",
  },
  {
    date: "Mar 21",
    title: "Grand Unification Attempt",
    bullets: [
      "Can FDCG constitute a grand unified theory? 8 iterations of autonomous investigation",
      "Physical picture is compelling: spacetime emerges from fracton dipole condensation",
      "Math breaks: Pretko rank-2 tensor gauge theory produces 5 DOF instead of 2 for GR",
    ],
    methodology:
      "Showed limits of exploration-only loops. The system could identify a compelling physical picture but couldn't repair fundamental mathematical inadequacy. Need better verification gates earlier in the pipeline.",
    stats: [
      { label: "Iterations", value: "8", color: "#6366f1" },
      { label: "DOF Found", value: "5", color: "#ef4444" },
      { label: "DOF Needed", value: "2", color: "#10b981" },
    ],
    status: "failed",
  },
  {
    date: "Mar 21",
    title: "7 Repair Sprints",
    bullets: [
      "Targeted attempts to fix FDCG's DOF problem: gauge enhancement, nematic condensation, RG flow, etc.",
      "Results: 0 PASS, 2 PARTIAL, 5 FAIL across all 7 sprints",
      "Confirmed FDCG cannot produce emergent GR by any known mechanism",
    ],
    methodology:
      "Rapid-fire sprint format works for exhaustive testing of repair paths. When all 7 fail, you have high confidence the direction is dead. Good use of agent time.",
    stats: [
      { label: "Sprints", value: "7", color: "#6366f1" },
      { label: "Passed", value: "0", color: "#ef4444" },
      { label: "Partial", value: "2", color: "#f59e0b" },
      { label: "Failed", value: "5", color: "#ef4444" },
    ],
    status: "failed",
  },
  {
    date: "Mar 21",
    title: "Agent Loop Architecture Designed",
    bullets: [
      "New hierarchical system: Missionary (sets direction) → Strategizer (runs loop) → Explorer (single investigation)",
      "Stop hook keeps Strategizer alive across context resets. Library accumulates knowledge.",
      "Domain-agnostic: first mission is quantum gravity, but architecture works for any research domain",
    ],
    methodology:
      "Major architectural shift. Previous loops were flat (one agent doing everything). New system separates strategic planning from tactical execution. Explorers get clean context windows.",
    stats: [
      { label: "Agent Levels", value: "3", color: "#a855f7" },
      { label: "Support Agents", value: "2", color: "#6366f1" },
    ],
    status: "milestone",
  },
  {
    date: "Mar 23",
    title: "First Run: Strategy 001",
    bullets: [
      "90 minutes, 5 explorations, 0 failures, 16% context used — entire run in one session",
      "Rediscovered Kuzmin-Tomboulis-Modesto nonlocal gravity (known since 1989). Methodology, not result, is the novel contribution.",
      "System pivoted well when novelty check failed — identified AS-IDG bridge as best remaining angle",
    ],
    methodology:
      "Autonomous operation works. Key gaps: novelty check too late (built whole theory before discovering it existed), no meta-learning captured, token tracking broken. Need novelty gate before full synthesis.",
    stats: [
      { label: "Runtime", value: "90 min", color: "#10b981" },
      { label: "Explorations", value: "5", color: "#6366f1" },
      { label: "Context Used", value: "16%", color: "#10b981" },
      { label: "Report Lines", value: "3,440", color: "#f59e0b" },
    ],
    status: "completed",
  },
];
