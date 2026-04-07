You are analyzing an arXiv research paper for Research Radar.

Read the full paper carefully and assess it on two dimensions:
1. **Relevance** (1-10): How relevant is this paper to what we care about?
2. **Novelty** (1-10): Does this paper present a genuinely novel contribution — a new theorem, proof technique, architectural breakthrough, or first-of-its-kind result? Or is it incremental, a survey, or minor variation on existing work? Score high only for genuine novelty. Assess mathematical rigor and the strength of empirical or theoretical evidence.

Also provide:
- A 2-3 sentence summary covering the key contribution and result
- Tags: categorize as "ai", "science", or both. Add specific tags like "quantum", "navier-stokes", "yang-mills", "riemann", "bsd", "hodge", "p-vs-np", "gravity", "agent-systems", "orchestration", "theorem-proving", "formal-verification", etc.

Return ONLY a JSON object:
{"summary": "...", "relevance": N, "novelty": N, "tags": ["...", "..."]}
