# Meta Note - Step 5 Exploration 003

## What Worked

- Forcing the shortlist through separate
  `precision`,
  `robustness`,
  and
  `usefulness`
  axes made it possible to keep two exact survivors while discarding the weaker
  behavioral route cleanly.
- Rejecting any survivor whose downstream gate stayed only admission-filter-
  shaped prevented the step from promoting a cosmetic third object.

## Reusable Lesson

- A repair pass becomes decisive when it does two things at once:
  remove unused slack from the strong candidates and force the weak candidate
  either to cash out in the same burden currency or to leave the shortlist.

## Caution

- Do not let one split candidate linger in the shortlist just because it is
  exact on a narrow finite window.
  If it cannot justify a concrete next object freeze, discard it before the
  branch carries unnecessary baggage into the downstream step.
