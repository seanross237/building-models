# Adversarial Logic System — Learnings

**Date:** 2026-03-27
**Source:** Runs 001-005 + 10 hypothesis pipelines

## The Judge Is Essential

An intermediary judge between the adversary and the architect prevents overcorrection. Without it, the architect over-reacts to overstated attacks and abandons viable parts of a theory.

**Evidence:**
- Run 001: The adversary rated 4 attacks "Fatal." The judge downgraded all 4 to "Major" — the adversary was applying standards that no physicalist theory of consciousness could meet (treating the hard problem as a flaw specific to this theory rather than a shared challenge across all physicalism).
- Run 002 (prose): Judge caught attack dependencies — one attack was only valid if another attack landed first.
- Run 004: Judge correctly recalibrated 3 of 7 severity ratings.

**The mechanism:** Adversaries are incentivized to be maximally aggressive. Without a judge, the architect receives unfiltered attacks and tries to address all of them, including overstated ones. This leads to the same overcorrection pattern seen in the Rhyme-Eval experiment (Gen 3 cratered because the updater tried to fix too many things at once).

## Structured Notation > Prose

Structured logical notation (numbered premises, explicit derivations) produces more rigorous theories than prose and makes flaws mechanically findable.

**Evidence:**
- Run 001 (structured): 16 attacks found, 8 mandatory fixes. The adversary could point to exact premise IDs where logic failed.
- Run 002 (prose): 12 attacks found, only 3 mandatory fixes. The run summary noted "prose made logical weaknesses easier to hide behind eloquence."
- The adversarial process naturally pushed the prose theory toward quasi-formal criteria anyway.

## Novelty Audits Are Critical When Hunting for New Ideas

Without an explicit novelty audit, agents repackage known results and present them as new. The audit forces the adversary to check each prediction against: can you get this from standard theory alone? Has someone published this?

**Evidence:**
- Run 005 (novel synthesis): All 3 initial predictions ruled NOT NOVEL by the audit. Without the audit, they would have been accepted.
- H1-H10 individual pipelines: Every hypothesis that scored high on plausibility scored low on novelty — because high plausibility meant it was essentially already known.

## The System Extracts Nuggets, Not Theories

The adversarial pipeline is better at refining than generating. It kills every bold theory but extracts specific actionable threads from the wreckage. Those threads are where novelty actually lives.

**Surviving nuggets from 10 hypothesis runs:**
- H6's classicality budget (Bekenstein + quantum Darwinism = finite classical reality capacity)
- H8's Compton-Unruh resonance (mechanism for modified inertia)
- H4's NREM PCI decomposition (testable with existing data)
- H5's Anthropic Entropy Threshold (simulation program)
- H10's GUP universality (mathematical question answerable by calculation)
- H9's z_temporal (computable crossover epoch)

## Adversaries Have a Domain Bias

When attacking theories in philosophy-heavy domains (consciousness, time), adversaries tend to treat domain-wide open problems (the hard problem) as theory-specific flaws. An attack taxonomy might fix this by forcing category labels — but we haven't tested that parameter yet.
