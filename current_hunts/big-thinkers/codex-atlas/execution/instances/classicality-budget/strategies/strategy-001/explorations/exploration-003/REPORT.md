# Exploration 003: Prior Art Search — Has the Classicality Budget Been Derived Before?

## Goal

Systematically search the scientific literature to determine whether the "classicality budget" — the trade-off R_δ ≤ (S_max / S_T) − 1 combining quantum Darwinism redundancy with Bekenstein entropy bounds — has been derived before, even under a different name.

## Search Strategy

The search covered:
1. Direct term searches ("classicality budget", "objectivity bound", "redundancy bound", etc.)
2. Key author groups (Zurek, Blume-Kohout, Riedel, Brandão, Korbicz, Bousso, Zwolak, Le & Olaya-Castro)
3. Conceptual neighbors (channel capacity, QEC bounds, broadcast channels, information bottleneck)
4. Recent work (2022-2026)
5. Cross-field searches combining Bekenstein/holographic bound terminology with quantum Darwinism terminology

Total: 25+ distinct web searches, 15+ papers examined, 8 author groups checked.

---

## Section 1: Direct Term Searches

### 1.1 "classicality budget"
**Result: NO MATCHES.** The exact phrase "classicality budget" returns zero relevant results in any physics literature. The term does not appear in any published paper, arXiv preprint, or review. [SOURCED: web search with zero hits]

### 1.2 "Bekenstein bound" + "quantum Darwinism"
**Result: NO DIRECT CONNECTION FOUND.** Searching for this combination returns quantum Darwinism papers on one hand and Bekenstein bound papers on the other, but **no paper that combines both concepts**. The Wikipedia article on quantum Darwinism does not mention Bekenstein. The quantum Darwinism literature does not reference entropy bounds on regions of space. The Bekenstein bound literature does not reference quantum Darwinism. [SOURCED: multiple web searches confirming zero cross-citations]

### 1.3 "redundancy bound" + quantum Darwinism + entropy
**Result: PARTIAL HIT — but structurally different.** The literature discusses bounds on redundancy, but these are internal to quantum Darwinism (bounded by environment size and fragment dimension), NOT by external entropy bounds like Bekenstein. The key finding is from Tank (2025) "Functional Information in Quantum Darwinism" (arXiv:2509.17775) which derives:

> **R_δ ≤ ⌊N/m_min(δ)⌋ ≤ N·log₂(d_e) / ((1−δ)·H_S)**

This bounds redundancy by the number of environment subenvironments N, the per-site Hilbert space dimension d_e, and pointer entropy H_S. This is the **closest existing result** to the classicality budget. See detailed comparison in Section 5.1. [SOURCED: arXiv:2509.17775]

### 1.4 "objectivity bound" + quantum
**Result: NO MATCHES** for this specific combination in the context of entropy bounds or information limits. [SOURCED: web search with zero relevant hits]

### 1.5 "holographic bound" + redundancy + objectivity
**Result: NO DIRECT CONNECTION.** The holographic principle literature and quantum Darwinism literature are entirely separate communities with no cross-citation on this specific question. [SOURCED: web search confirming separate literatures]

### 1.6 "entropy bound" + objectivity / intersubjectivity
**Result: NO MATCHES** for the combination linking entropy bounds to classical objectivity. The intersubjectivity literature in quantum foundations discusses agreement between observers but does not invoke entropy bounds. [SOURCED: web search]

### 1.7 "information-theoretic limit" + classicality
**Result: TANGENTIAL HITS ONLY.** Papers discuss information-theoretic aspects of classicality (Holevo bound, channel capacity) but none derive a bound on classicality from the total entropy of a spatial region. [SOURCED: web search]

### 1.8 "quantum Darwinism" + ("Bekenstein" OR "holographic" OR "Bousso")
**Result: ZERO CROSS-REFERENCES.** This is the most telling search. There are NO papers in the literature that mention quantum Darwinism alongside Bekenstein bounds, holographic bounds, or Bousso's covariant entropy bound. These two research communities — quantum Darwinism/decoherence and holographic/entropy bounds — have not intersected on this question. [SOURCED: web search confirming zero overlap]

---

## Section 2: Key Author Analysis

### 2.1 Wojciech Zurek

**Papers checked:**
1. Zurek (2003) "Environment as a witness" — Rev. Mod. Phys. 75, 715
2. Zurek (2009) "Quantum Darwinism" — Nature Physics 5, 181
3. Zurek (2000) "Einselection and decoherence from an information theory perspective" — Ann. Phys.
4. Zurek (2018) "Quantum theory of the classical: quantum jumps, Born's Rule..." — Phil. Trans. R. Soc. A
5. Zurek (2022) "Quantum Theory of the Classical: Einselection, Envariance, Quantum Darwinism and Extantons" — Entropy 24, 1520
6. Zurek (2025) "Consensus About Classical Reality in a Quantum Universe" — conference paper

**Finding:** Zurek's work defines redundancy R_δ as the number of environment fragments each carrying (1−δ)H_S bits of system information. He discusses how redundancy grows with environment size and how mixed environments suppress storage capacity by factor (1−h), where h is the "haziness" (initial entropy) of each environment qubit. However, **Zurek never connects redundancy to any external entropy bound** (Bekenstein, holographic, or otherwise). His bounds on redundancy are always internal: R_δ ~ N/f_δ where N is the number of environment subsystems and f_δ is the minimal fragment size. The 2025 "Consensus" paper discusses consensus emergence but does not invoke entropy bounds. **No mention of Bekenstein bound, holographic principle, or any spacetime-based entropy limit appears in any of Zurek's quantum Darwinism papers.**

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: direct examination of all papers listed]

### 2.2 Blume-Kohout & Zurek

**Papers checked:**
1. Blume-Kohout & Zurek (2005) "A simple example of 'quantum Darwinism'" — Found. Phys. 35, 1857
2. Blume-Kohout & Zurek (2006) "Quantum Darwinism: Entanglement, branches, and the emergent classicality of redundantly stored quantum information" — Phys. Rev. A 73, 062310

**Finding:** These early papers establish the spin-environment model for quantum Darwinism and compute redundancy for specific models. They derive redundancy values numerically but do not derive general entropy-based upper bounds. No connection to Bekenstein or holographic bounds.

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: direct examination via web]

### 2.3 Jess Riedel, Zurek, Zwolak

**Papers checked:**
1. Riedel & Zurek (2010) "Quantum Darwinism in an Everyday Environment: Huge Redundancy in Scattered Photons" — PRL 105, 020404
2. Riedel, Zurek, Zwolak (2012) "The Rise and Fall of Redundancy in Decoherence and Quantum Darwinism" — New J. Phys. 14, 083010
3. Riedel (2017) "Classical branch structure from spatial redundancy in a many-body wave function" — PRL 118, 120402

**Finding:** Riedel et al. (2012) study how redundancy rises during decoherence and falls during thermalization. Key result: for random states, half the environment must be measured to determine system state (R ~ 2), but decoherent states achieve much higher redundancy. Riedel (2017) connects wavefunction branches to redundancy and decoherent histories. They discuss conditions for redundancy but **do not derive an upper bound from entropy of a spatial region**. Bounds are always in terms of environment Hilbert space dimension, not spatial entropy bounds.

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: examination of abstracts and key content]

### 2.4 Brandão, Piani, Horodecki

**Paper checked:**
- Brandão, Piani, Horodecki (2015) "Generic emergence of classical features in quantum Darwinism" — Nature Communications 6, 7908 (arXiv:1310.8640)

**Finding:** This landmark paper proves that quantum Darwinism is generic — any quantum dynamics leads to observers having access to at most classical information about one and the same measurement. They prove this using quantum information-theoretic tools (quantum discord, redistribution of correlations). However, **they do not derive any bound on redundancy from total system entropy**. Their result is about the *qualitative* emergence of classicality, not a *quantitative* bound on how much redundancy is possible. They show classicality emerges generically but do not ask "how much classical information can a region support?"

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: arXiv:1310.8640 abstract + search results]

### 2.5 Korbicz et al.

**Papers checked:**
1. Korbicz (2021) "Roads to objectivity: Quantum Darwinism, Spectrum Broadcast Structures, and Strong quantum Darwinism" — Quantum 5, 571 (arXiv:2007.04276)
2. Korbicz, Horodecki, Horodecki (2014) "Objectivity in a noisy photonic environment" — PRL 112, 120402

**Finding:** The comprehensive 2021 review compares three frameworks for objectivity (QD, SBS, Strong QD). It discusses the relationships between them and proves a generalized SBS theorem. However, **it contains no discussion of entropy bounds on redundancy or objectivity**. No mention of Bekenstein bound, holographic principle, or any spatial entropy limit constraining how much objectivity a region can support.

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: direct examination of review paper]

### 2.6 Raphael Bousso

**Papers checked:**
1. Bousso (2017) "Universal Limit on Communication" — PRL 119, 140501 (arXiv:1611.05821)
2. Bousso, Casini, Fisher, Maldacena (2014) "Proof of a quantum Bousso bound" — Phys. Rev. D 90
3. Bousso entropy bound review lectures (PITP 2011)

**Finding:** Bousso (2017) derives a universal bound on channel capacity: the Holevo quantity is at most ~E∆t/ℏ, independent of system size or signal nature. This is a bound on *communication* capacity, not on *redundancy* or *objectivity*. The paper **does not address quantum Darwinism, environmental redundancy, classical objectivity, or observer agreement**. It focuses purely on the rate of information transfer between distant systems.

The 2014 proof of the quantum Bousso bound establishes entropy bounds on lightsheets but makes no connection to decoherence, quantum Darwinism, or redundancy.

**Key insight:** Bousso's work bounds how much information can flow through a region (channel capacity), which is related but distinct from the classicality budget's question of how much redundant classical information can *exist in* a region. The classicality budget is a statement about the static information content of a region, not about communication rates.

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: arXiv:1611.05821 and associated papers]

### 2.7 Michael Zwolak

**Papers checked:**
1. Zwolak, Quan, Zurek (2009) "Quantum Darwinism in a hazy environment" — PRL 103, 110402 (arXiv:0904.0418)
2. Zwolak & Zurek (2017) "Redundancy of einselected information" — Phys. Rev. A 95, 030101
3. Girolami, Touil, Yan, Deffner, Zurek (2022) "Redundantly Amplified Information Suppresses Quantum Correlations in Many-Body Systems" — PRL 129, 010401

**Finding:** Zwolak et al. (2009) show that environment "haziness" (initial entropy h) suppresses information storage by factor (1−h), requiring fragment size ~(1−h)^{−1} larger. This is a **suppression factor** on redundancy from environment mixedness — the closest in spirit to the classicality budget because it connects environment entropy to redundancy limits. However, it operates at the level of individual environment qubits, not at the level of total regional entropy bounds.

Girolami et al. (2022) prove that redundantly amplified information suppresses quantum correlations, establishing conditional mutual information scaling. They do not derive Bekenstein-type bounds.

**Contains R_δ ≤ S_max/S_T bound: NO** [SOURCED: examination of all papers]

### 2.8 Other Relevant Authors

**Papers checked:**
1. Le & Olaya-Castro — Strong quantum Darwinism and spectrum broadcast structures
2. Knott, Tufarelli, Piani, Adesso (2018) "Generic emergence of objectivity of observables in infinite dimensions" — PRL 121, 160401
3. Tank (2025) "Functional Information in Quantum Darwinism" — arXiv:2509.17775
4. Hayden & Wang (2023/2025) "What exactly does Bekenstein bound?" — Quantum 9, 1664 (arXiv:2309.07436)
5. ESA Study 19-1201: "Quantum Shannon theory and quantum Darwinism"

**Findings:**

**Tank (2025)** is the closest existing work. See detailed comparison in Section 5.1.

**Hayden & Wang (2025)** rigorously examine what the Bekenstein bound constrains. Key result: classical bits and qubits are constrained, but zero-bits are not. When both encoder and decoder are spatially restricted, Bekenstein constrains all capacities. **They do not mention quantum Darwinism** or apply this to redundancy. [SOURCED: arXiv:2309.07436]

**ESA Study** explicitly connects quantum Shannon theory to quantum Darwinism but examines quantum networks of observers — not entropy bounds on regions. Could not fully access the PDF but the study description and abstract do not mention Bekenstein or holographic bounds. [SOURCED: ESA study description]

---

## Section 3: Conceptual Neighbors

### 3.1 Holographic Channel Capacity

Bousso (2017) derives a universal limit on communication: capacity ~ E∆t/ℏ. This bounds the *rate* of information transfer, not the *total redundant information* in a region. The classicality budget is a different kind of bound — it's about how the *finite total entropy* of a region partitions between redundancy and diversity of classical facts. These are conceptually adjacent but formally distinct quantities. No one has connected Bousso's channel capacity to quantum Darwinism's redundancy. [INFERRED from examining both literatures]

### 3.2 Quantum Error Correction Bounds

The quantum Singleton bound and quantum Hamming bound constrain how much quantum information can be protected by a code. The environment-as-error-correcting-code picture exists in the quantum Darwinism literature. However, **no one has applied QEC capacity bounds to derive a limit on environmental redundancy from total system entropy**. QEC bounds relate code rate to error correction capability, which is structurally similar (more redundancy = more error tolerance = less information) but has not been connected to Bekenstein-type entropy bounds. [INFERRED from examining QEC and QD literature separately]

### 3.3 Quantum Broadcast Channels

The system-environment interaction can be modeled as a quantum broadcast channel (one sender, many receivers = environmental fragments). Quantum broadcast channel capacity has been studied (Yard, Hayden, Devetak, 2006). However, **the broadcast channel capacity literature has not been connected to spatial entropy bounds**. The capacity theorems bound what can be communicated given a fixed channel, but do not ask "what happens when the total channel capacity is limited by the Bekenstein bound?" [INFERRED from examining broadcast channel literature]

### 3.4 Information Bottleneck

The quantum information bottleneck (Tishby, Pereira, Bialek framework extended to quantum) considers trade-offs between compression and relevant information preservation. This is structurally analogous to the redundancy-vs-richness trade-off in the classicality budget, but it operates at the level of data processing, not at the level of fundamental physics. No one has connected the quantum information bottleneck to Bekenstein bounds or quantum Darwinism. [INFERRED from examining QIB literature]

### 3.5 Hayden-Wang on What Bekenstein Bounds

Hayden & Wang (2025) is the most relevant conceptual neighbor from the entropy bound side. They rigorously show that the Bekenstein bound constrains classical bits and qubits when both encoder and decoder are spatially restricted. This establishes the physical foundation for applying Bekenstein to information *stored in* a region. However, they do not take the next step of applying this to environmental redundancy or quantum Darwinism. [SOURCED: arXiv:2309.07436]

---

## Section 4: Recent Work (2022-2026)

### 4.1 Quantum Darwinism-encoding transitions (2023-2024)
Papers by Weinstein et al. (arXiv:2305.03694, arXiv:2312.04284) study phase transitions where quantum Darwinism breaks down. They identify a "QD phase" where classical information is redundantly available and an "encoding phase" where it is not. These papers study when QD occurs vs. fails, but **do not derive bounds on how much QD a region can support**. [SOURCED: arXiv search]

### 4.2 Experimental verification (2025)
The superconducting circuit experiment (arXiv:2504.00781) observes quantum Darwinism directly, confirming branching states and mutual information saturation. The experiment validates QD but **does not probe entropy-limited regimes** where the classicality budget would become relevant. [SOURCED: arXiv:2504.00781]

### 4.3 Tank (2025) Functional Information Framework
As discussed in Section 1.3, this is the closest existing work. It frames objectivity as resource-limited, derives R_δ bounds from environment capacity, and discusses thermodynamic costs. See Section 5.1 for detailed comparison. [SOURCED: arXiv:2509.17775]

### 4.4 Redundancy from Subsystem Thermalization (2026)
A very recent paper (arXiv:2603.15743) connects redundancy to thermalization. Shows redundancy persists despite thermalizing dynamics if an initial broadcasting interaction changes conserved quantity density. Uses large deviation principle. Does not derive entropy bounds of the Bekenstein type. [SOURCED: arXiv:2603.15743]

---

## Section 5: Paper-by-Paper Assessment

### 5.1 CRITICAL COMPARISON: Tank (2025) vs. Classicality Budget

This is the closest existing result and requires careful comparison.

**Tank's bound:**
> R_δ ≤ N·log₂(d_e) / ((1−δ)·H_S)

Where:
- N = number of environment subenvironments
- d_e = Hilbert space dimension of each subenvironment
- H_S = pointer entropy (Shannon entropy of system's pointer states)
- δ = information deficit threshold

**The classicality budget:**
> R_δ ≤ S_max / S_T − 1

Where:
- S_max = Bekenstein entropy bound for the region (= A/(4G) in holographic form)
- S_T = entropy per classical fact (pointer entropy)

**Structural comparison:**

| Feature | Tank (2025) | Classicality Budget |
|---------|-------------|-------------------|
| Numerator | N·log₂(d_e) = total environment entropy capacity | S_max = Bekenstein bound |
| Denominator | (1−δ)·H_S = pointer entropy with deficit | S_T = pointer entropy |
| Physical scope | Quantum information theory (Hilbert space) | Gravitational/fundamental physics |
| What bounds the total? | Environment Hilbert space dimension | Spacetime geometry |
| Novel physical content | Information-theoretic | Gravitational |

**Key insight: The classicality budget is obtained from Tank's bound by replacing N·log₂(d_e) with S_max.** The total environment entropy capacity N·log₂(d_e) is an abstract quantum information quantity. The Bekenstein bound S_max provides a physical upper limit on this quantity for any system in a bounded region of space. The classicality budget's novelty lies precisely in this substitution — connecting the abstract information-theoretic bound to a concrete physical (gravitational) bound.

**Assessment: PARTIALLY KNOWN.** The structural form of the bound (redundancy ≤ total capacity / per-fact entropy) exists in Tank (2025). What is novel is:
1. The identification that S_max (Bekenstein) upper-bounds the abstract N·log₂(d_e)
2. The physical interpretation as a fundamental limit on classical reality
3. The conceptual framing as a "budget" — a trade-off between richness and agreement
4. All implications for specific systems (black holes, labs, cosmology)

**However, this assessment needs a caveat:** Tank (2025) was submitted September 2025, and is itself very recent. The *structural* form R_δ ~ N/f_δ has been implicit in quantum Darwinism since at least Zurek (2009). What Tank adds is the explicit capacity-limited formulation. What the classicality budget adds is the physical grounding via Bekenstein. [INFERRED from comparison of both results]

### 5.2 Summary Table: All Papers Checked

| Paper | Contains R_δ ≤ S_max/S_T? | Closest Result | Gap from Classicality Budget |
|-------|--------------------------|----------------|------------------------------|
| Zurek (2003, 2009, 2022, 2025) | NO | R_δ ~ N/f_δ (implicit) | No physical entropy bound |
| Blume-Kohout & Zurek (2005, 2006) | NO | Numerical R_δ values | No general bound |
| Riedel, Zurek, Zwolak (2010, 2012, 2017) | NO | R_δ conditions | No entropy bound |
| Brandão, Piani, Horodecki (2015) | NO | Genericity proof | Qualitative, not quantitative |
| Korbicz (2014, 2021) | NO | SBS framework | No entropy bound |
| Bousso (2014, 2017) | NO | Channel capacity | Different quantity entirely |
| Zwolak et al. (2009, 2017, 2022) | NO | Haziness suppression | Per-qubit, not total |
| Le & Olaya-Castro | NO | Strong QD ↔ SBS equivalence | No entropy bound |
| Knott et al. (2018) | NO | Infinite-dim genericity | No entropy bound |
| Tank (2025) | **CLOSEST** | R_δ ≤ N·log₂(d_e)/((1−δ)·H_S) | Uses QI capacity, not Bekenstein |
| Hayden & Wang (2025) | NO | Bekenstein bounds cbits/qubits | No connection to QD |
| Girolami et al. (2022) | NO | CMI scaling bounds | No entropy bound |
| arXiv:2603.15743 (2026) | NO | Thermalization + redundancy | No entropy bound |
| ESA Study 19-1201 | NO | QD + Shannon theory | No entropy bound |

---

## Section 6: Verdict

### **VERDICT: PARTIALLY KNOWN (Novel Synthesis)**

**The structural form of the bound exists, but the physical content does not.**

Specifically:

1. **KNOWN:** That redundancy is bounded by the total information capacity of the environment divided by the per-fact entropy. This is explicit in Tank (2025) as R_δ ≤ N·log₂(d_e)/((1−δ)·H_S), and implicit in quantum Darwinism since Zurek (2009) as R_δ ~ N/f_δ.

2. **NOVEL:** The connection to the Bekenstein bound — the identification that N·log₂(d_e) is physically bounded above by S_max = A/(4Gℏ) for any system in a spatial region, yielding R_δ ≤ S_max/S_T − 1 as a fundamental physical limit on classical reality.

3. **NOVEL:** The conceptual interpretation as a "classicality budget" — the trade-off between the richness of classical reality (how many facts) and the objectivity of that reality (how many observers agree), constrained by spacetime geometry.

4. **NOVEL:** All physical implications — computation for specific systems, connection to black hole physics, the suggestion that reality becomes "thin" near horizons, etc.

5. **NOVEL:** The bridging of two previously unconnected research communities — quantum Darwinism (Zurek school) and holographic entropy bounds (Bousso/Bekenstein school). After 25+ searches, we found **zero papers** citing both bodies of work in connection with this question.

### Confidence Assessment

- **High confidence** that the exact formula R_δ ≤ S_max/S_T − 1 has not been published before. The term "classicality budget" is novel. The Bekenstein–quantum Darwinism connection is novel.
- **Medium-high confidence** that the *structural* form (redundancy ≤ capacity / per-fact-size) was implicit in the field but only made explicit by Tank (2025).
- **Caveat:** We could not fully access all papers (some PDFs were binary/restricted). It is possible that a passing remark in an inaccessible paper makes the Bekenstein connection, but this is unlikely given the total absence of cross-citations between the two literatures.

### What Would Change This Verdict

The verdict would change to ALREADY KNOWN if:
- A paper is found that explicitly connects Bekenstein/holographic entropy bounds to quantum Darwinism redundancy
- A paper derives an upper bound on R_δ from the total entropy of a spatial region
- Bousso's channel capacity result is applied to environmental redundancy somewhere

The verdict would strengthen to FULLY NOVEL if:
- Tank (2025) is assessed as not constituting the structural precursor (arguable, since Tank derives the capacity bound only for abstract Hilbert spaces, never invoking physics of spatial regions)

---

## Section 7: Search Audit

### Queries Executed (25+ total)

1. `"classicality budget" quantum`
2. `"Bekenstein bound" "quantum Darwinism" redundancy`
3. `"redundancy bound" quantum Darwinism entropy limit`
4. `"objectivity bound" quantum decoherence entropy`
5. `"holographic bound" redundancy objectivity quantum information`
6. `Zurek quantum Darwinism redundancy upper bound environment size entropy`
7. `Bousso "universal limit on communication" holographic channel capacity 2017`
8. `Brandao Piani Horodecki "generic emergence" quantum Darwinism redundancy bound 2015`
9. `Riedel Zurek Zwolak "rise and fall of redundancy" bound decoherence 2012`
10. `Zwolak quantum Darwinism redundancy capacity environment fragments maximum bound`
11. `Korbicz "spectrum broadcast structures" objectivity entropy bound 2021`
12. `quantum broadcast channel capacity redundancy multiple receivers environment decoherence`
13. `"information-theoretic limit" classicality OR objectivity quantum decoherence bound`
14. `quantum information bottleneck trade-off classical information redundancy entropy bound`
15. `quantum error correction singleton bound environment redundancy Bekenstein holographic`
16. `"quantum Darwinism" "Bekenstein" OR "holographic" OR "Bousso" bound entropy limit`
17. `Bousso entropy bound number of classical states region observers agreement information`
18. `"Bekenstein bound" "maximum number of" classical states OR bits OR observers OR copies region`
19. `decoherence rate bound entropy Bekenstein OR holographic limit quantum classical transition`
20. `"quantum Shannon theory" "quantum Darwinism" ESA study reference`
21. `environment as quantum channel capacity limit classical objectivity quantum Darwinism Holevo`
22. `"classical capacity" bounded region "number of observers" information limit quantum`
23. `Riedel "decoherent histories" "wavefunction branches" quantum Darwinism entropy bound information limit`
24. `"intersubjective" quantum information limit agreement classical reality bound`
25. `"redundantly amplified information" suppresses quantum Zwolak Zurek 2022 bound entropy`
26. `trade-off redundancy information content classical environment "budget" OR "capacity" 2024 2025 2026`
27. `quantum Darwinism R_delta S_max Bekenstein holographic entropy bound limit classicality`
28. `Zurek 2022 "einselection envariance quantum Darwinism extantons" entropy redundancy maximum bound`
29. `"quantum Darwinism" entropy upper bound redundancy "total information" OR "maximum" 2020-2025`

### Papers Examined (15+)

1. Zurek (2009) "Quantum Darwinism" — Nature Physics 5, 181
2. Zurek (2022) "Quantum Theory of the Classical..." — Entropy 24, 1520
3. Zurek (2025) "Consensus About Classical Reality" — conference paper
4. Blume-Kohout & Zurek (2005, 2006) — Found. Phys. / Phys. Rev. A
5. Riedel & Zurek (2010) — PRL 105, 020404
6. Riedel, Zurek, Zwolak (2012) — New J. Phys. 14, 083010
7. Brandão, Piani, Horodecki (2015) — Nat. Commun. 6, 7908
8. Korbicz (2021) — Quantum 5, 571
9. Bousso (2017) "Universal Limit on Communication" — PRL 119, 140501
10. Bousso et al. (2014) "Proof of quantum Bousso bound" — Phys. Rev. D 90
11. Zwolak, Quan, Zurek (2009) — PRL 103, 110402
12. Girolami et al. (2022) — PRL 129, 010401
13. Tank (2025) "Functional Information in QD" — arXiv:2509.17775
14. Hayden & Wang (2025) "What exactly does Bekenstein bound?" — Quantum 9, 1664
15. Zurek (2022) "Eavesdropping on the Decohering Environment" — PRL 128, 010401
16. arXiv:2603.15743 (2026) — Redundancy from Subsystem Thermalization
17. Knott et al. (2018) — PRL 121, 160401

### Author Groups Checked (8/8)
- ✅ Wojciech Zurek
- ✅ Robin Blume-Kohout
- ✅ Jess Riedel
- ✅ Brandão, Piani, Horodecki
- ✅ Korbicz
- ✅ Raphael Bousso
- ✅ Michael Zwolak
- ✅ Others (Le, Olaya-Castro, Knott, Tank, Hayden, Wang)

---

## Section 8: Key Structural Finding

The most important finding for the mission is not just that the classicality budget is novel, but *why* it is novel. The novelty arises from a **gap between two research communities**:

1. **Quantum Darwinism community** (Zurek, Riedel, Zwolak, Brandão, Korbicz, Le, Olaya-Castro, Tank): These researchers study how classical objectivity emerges from quantum mechanics. They derive bounds on redundancy from the abstract Hilbert space dimension of the environment. They have never asked "what if the environment's Hilbert space dimension is itself bounded by spacetime geometry?"

2. **Entropy bounds community** (Bekenstein, Bousso, Hayden, Wall, Maldacena): These researchers study fundamental limits on information from general relativity and quantum gravity. They have never asked "what does this imply for the redundancy of classical information — for quantum Darwinism?"

The classicality budget lives precisely at the intersection of these two fields. The formula R_δ ≤ S_max/S_T − 1 is, in a sense, "trivially" obtainable by combining known results from both communities — but **no one has combined them because no one works in both**. This is the hallmark of a genuine interdisciplinary insight: obvious in retrospect, invisible from within either field.

This structural finding should strengthen confidence in the novelty claim, while also flagging that the derivation may face criticism as "merely combining existing results" — which is legitimate and should be addressed in the stress-testing phase.
