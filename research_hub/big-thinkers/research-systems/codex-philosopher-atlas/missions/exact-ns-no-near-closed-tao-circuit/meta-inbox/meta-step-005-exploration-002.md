# Meta Note - Step 5 Exploration 002

## What Worked

- Splitting the itinerary into early and late pieces made two different failure
  types visible:
  the early filter is exact but weak,
  while the late filter is not well-defined on the frozen record.
- Using the low-leakage friendly family kept the analysis focused on event-time
  rigidity instead of drifting back into leakage bookkeeping.

## Reusable Lesson

- When a behavior-based candidate is ambiguous only at the late stage, split
  the early exact filter from the late transfer requirement before deciding
  usefulness.
  That often reveals that the real bottleneck is event language, not
  isolation.

## Caution

- If the late split only works by deleting the final threshold event or by
  shortening the required event language after outcomes are seen, that is a
  definition change, not an honest repair.
