A run can be considered healthy if the mission tree shows consistent progress and activity. Observable indicators include:

*   **Regular updates to `state.md` files:** Healthy runs will frequently update their `state.md` files to reflect progress. This indicates that the worker is actively processing tasks.
*   **Completion of sub-tasks:** As a worker progresses, sub-tasks within the mission tree should be marked as complete. This can be observed by changes in file content or the creation of new files indicating completion.
*   **Absence of long-running, uncompleted tasks:** If a particular branch of the mission tree remains stagnant for an extended period without any updates or progress, it could indicate a stuck process.
*   **Consistent file modification times:** Healthy activity within a mission directory will be reflected in recent modification times for files. Stale modification times can be a red flag.

Potential red flags that might indicate a stuck run include:

*   **Stagnant `state.md` files:** If a `state.md` file hasn't been updated for a significant duration, the worker associated with that branch may be stuck.
*   **Unfinished tasks without apparent reason:** If tasks are consistently failing or not progressing, and there are no clear error messages or reasons for the failure, it could indicate a deeper issue.
*   **Circular dependencies or deadlocks:** While harder to detect solely from file content, a pattern of tasks repeatedly attempting and failing to complete due to unmet dependencies could signal a deadlock.
*   **Lack of expected output files:** If a worker is supposed to generate certain output files upon completion of a task, and these files are consistently missing, it suggests the task is not completing successfully.

To effectively monitor the health of a run, one would typically look for a pattern of consistent, forward progress across the mission tree, with regular updates and task completions. Conversely, stagnation, repeated failures, or a lack of expected progress are indicators of a potentially stuck run.