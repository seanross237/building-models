# Static Cancellation Cases Should Test Admissibility Filters, Not Carry The Main Obstruction Verdict

When a packet branch uses explicit anti-families, separate static cancellation
cases from live obstruction-facing cases.

Static zero-activity packets are still useful, but only in a narrow role:
they test whether the branch's hard admissibility rules really block vacuous
passes such as zero-denominator leakage ratios or event sheets with no events.

Do not let those static cases carry the main anti-family verdict.
They show filter discipline, not how a genuinely live packet fails on the
frozen branch ledger.

The main obstruction read should come from a live adverse family that keeps
the intended channels active enough to make the failure mechanism informative.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/meta-inbox/meta-step-004-exploration-002.md`
