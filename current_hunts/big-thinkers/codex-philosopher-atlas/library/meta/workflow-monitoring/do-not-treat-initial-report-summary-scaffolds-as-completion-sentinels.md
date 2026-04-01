# Do Not Treat Initial Report Summary Scaffolds As Completion Sentinels

Explorer-session monitoring should not rely on sentinel-file existence alone
when the session writes `REPORT-SUMMARY.md` as an initial scaffold.

A summary file can appear before the substantive report is complete, so a
workflow should distinguish between "artifact created" and "usable findings are
present." Otherwise session state can look complete while the actual report is
still pending or only partially written.

The stronger reusable rule is to wait for either an explicit terminal status or
a non-placeholder summary check that confirms substantive findings are present.
Sentinel existence by itself is too weak when the workflow creates placeholder
artifacts early.

Filed from:
- `missions/beyond-de-giorgi/meta-inbox/meta-step-003-exploration-001.md`
- `missions/beyond-de-giorgi/meta-inbox/meta-step-003-exploration-002.md`
