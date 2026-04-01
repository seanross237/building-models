
To determine if a run is healthy or stuck by inspecting the mission tree alone, you should examine the contents and activity within the primary directories: `for-orchestrator/`, `input/`, `output/`, and `system/`.

### `for-orchestrator/`

*   **Healthy Run:** Look for files that indicate successful handoffs, progress updates, or expected communication with an orchestrator. The presence of new or updated files here suggests the process is interacting correctly with its environment.
*   **Stuck Run:** An empty `for-orchestrator/` directory, or one containing stale information, might indicate that the process is not communicating as expected or has stalled in its interaction with other components.

### `input/`

*   **Healthy Run:** Observe if files in the `input/` directory are being processed. This could mean they are being moved, deleted, or that new files are being generated based on them. Active consumption of input is a sign of a healthy, progressing run.
*   **Stuck Run:** If files in `input/` remain untouched over an extended period, or if the directory is unexpectedly empty when input is expected, it suggests the process is not able to proceed.

### `output/`

*   **Healthy Run:** A healthy run will show regular updates or new files appearing in the `output/` directory. The content of these files might also reveal progress or successful completion of tasks.
*   **Stuck Run:** A lack of new content in `output/`, or the consistent appearance of incomplete results or error messages, points to a stuck or failed run.

### `system/`

*   **Healthy Run:** Check logs or state files within the `system/` directory. Activity like new log entries, progress messages, or successful completion markers indicates the system is operating normally.
*   **Stuck Run:** Error logs, repeated error messages, or a complete absence of recent activity in `system/` files can be strong indicators of a problem or a stalled process.

### General Indicators of a Stuck Run:

*   **Lack of Activity:** No new files, no modifications to existing files, and no log updates across these directories over a significant timeframe.
*   **Stale Timestamps:** Files in critical directories have not been modified for a prolonged period.
*   **Error Indicators:** The presence of specific error files, error messages in logs, or files explicitly marking a failed state.
*   **Incomplete Processing:** Input files remain unprocessed, or output files are consistently incomplete or malformed.

By monitoring these directories and the nature of their contents, one can infer the health and progress of a run.
