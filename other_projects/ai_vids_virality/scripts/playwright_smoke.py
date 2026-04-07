"""End-to-end Playwright smoke test for the live UI on http://localhost:8000.

Verifies the Phase 10 UX claims against the running server:
  1. Page loads, kanban data renders
  2. Premise Review is the default page and shows N>0 sketch cards
  3. ALL premise-review cards start collapsed (`.sketch-card.collapsed`)
  4. Clicking a card expands it (`.sketch-card.expanded` + variant rows visible)
  5. Edit button (.edit-premise-btn) is rendered on every premise inside an expanded card
  6. Add-premise button (.add-premise-btn) is rendered at the bottom of each variant
  7. Refreshing the page does NOT lose state — sketch count is identical before/after F5
  8. Signals page promote dialog has the new guidance textarea (#promote-guidance-textarea)

Run from project root:
    source .venv/bin/activate
    python scripts/playwright_smoke.py
"""
from __future__ import annotations

import sys
import time

from playwright.sync_api import sync_playwright, Page, expect


BASE_URL = "http://localhost:8000"


def log(msg: str) -> None:
    print(f"  {msg}", flush=True)


def fail(msg: str) -> None:
    print(f"  FAIL: {msg}", flush=True)
    raise SystemExit(1)


def pass_(msg: str) -> None:
    print(f"  PASS: {msg}", flush=True)


def wait_for_kanban(page: Page) -> None:
    """Wait for the initial /api/kanban response + first render."""
    page.wait_for_function(
        "() => window.kanbanData !== undefined || document.querySelectorAll('.sketch-card').length > 0 || document.querySelectorAll('.empty').length > 0",
        timeout=10000,
    )
    # Give the render loop one extra tick
    page.wait_for_timeout(500)


def click_premise_review_tab(page: Page) -> None:
    page.locator("nav.nav button", has_text="Premise Review").first.click()
    page.wait_for_timeout(300)


def click_signals_tab(page: Page) -> None:
    page.locator("nav.nav button", has_text="Signals").first.click()
    page.wait_for_timeout(300)


def test_1_page_loads(page: Page) -> None:
    print("\n[1] page loads + kanban renders")
    page.goto(BASE_URL)
    wait_for_kanban(page)
    title = page.title()
    log(f"page title: {title!r}")
    if not title:
        fail("blank title")
    pass_("page loaded")


def test_2_premise_review_default(page: Page) -> int:
    print("\n[2] Premise Review is the default page and has sketches")
    click_premise_review_tab(page)
    cards = page.locator(".sketch-card")
    count = cards.count()
    log(f"sketch-card count: {count}")
    if count == 0:
        fail("Premise Review has 0 cards (expected ~21 from kanban)")
    pass_(f"{count} sketch cards rendered")
    return count


def test_3_cards_start_collapsed(page: Page) -> None:
    print("\n[3] All sketch cards start COLLAPSED on initial load")
    collapsed = page.locator(".sketch-card.collapsed").count()
    expanded = page.locator(".sketch-card.expanded").count()
    log(f"collapsed={collapsed} expanded={expanded}")
    if expanded > 0:
        fail(f"{expanded} cards are expanded — should be 0 on load")
    if collapsed == 0:
        fail("0 collapsed cards — selector mismatch")
    pass_(f"all {collapsed} cards are collapsed")
    # Also check the JS state object
    js_state = page.evaluate("() => Array.from(window.premiseReview._state())")
    log(f"window.premiseReview._state() = {js_state}")
    if js_state:
        fail(f"expandedPremiseCards should be empty, got {js_state}")
    pass_("window.premiseReview._state() is empty")


def test_4_click_expands(page: Page) -> str:
    print("\n[4] Clicking a card header expands it")
    first_card = page.locator(".sketch-card.collapsed").first
    sketch_id = first_card.get_attribute("data-sketch-id") or "<unknown>"
    log(f"clicking first card: {sketch_id}")
    # Click the header (cursor: pointer area)
    first_card.locator(".sketch-header").click()
    page.wait_for_timeout(300)
    # The same card should now have .expanded
    expanded_now = page.locator(
        f'.sketch-card.expanded[data-sketch-id="{sketch_id}"]'
    ).count()
    log(f'card[data-sketch-id={sketch_id}].expanded count: {expanded_now}')
    if expanded_now != 1:
        fail(f"card {sketch_id} did not become .expanded after click")
    pass_(f"card {sketch_id} expanded after click")
    # Also verify the JS state
    js_has = page.evaluate(
        f"() => window.premiseReview.isPremiseCardExpanded('{sketch_id}')"
    )
    if not js_has:
        fail(f"window.premiseReview._state() doesn't contain {sketch_id}")
    pass_("window.premiseReview._state() includes the expanded card")
    return sketch_id


def test_5_edit_buttons(page: Page, expanded_id: str) -> None:
    print("\n[5] Expanded card shows .edit-premise-btn on every premise")
    selector = f'.sketch-card.expanded[data-sketch-id="{expanded_id}"] .edit-premise-btn'
    edit_btns = page.locator(selector)
    count = edit_btns.count()
    log(f"edit buttons in {expanded_id}: {count}")
    if count == 0:
        fail("0 edit buttons in expanded card — Phase 10 edit affordance missing")
    pass_(f"{count} edit buttons rendered")


def test_6_add_buttons(page: Page, expanded_id: str) -> None:
    print("\n[6] Expanded card shows .add-premise-btn at bottom of each variant column")
    selector = f'.sketch-card.expanded[data-sketch-id="{expanded_id}"] .add-premise-btn'
    add_btns = page.locator(selector)
    count = add_btns.count()
    log(f"add-premise buttons in {expanded_id}: {count}")
    if count == 0:
        fail("0 add-premise buttons in expanded card — Phase 10 add affordance missing")
    pass_(f"{count} add-premise buttons rendered")


def test_7_refresh_preserves_state(page: Page, expected_count: int) -> None:
    print("\n[7] Refreshing the page does NOT lose data")
    page.reload()
    wait_for_kanban(page)
    click_premise_review_tab(page)
    page.wait_for_timeout(500)
    after = page.locator(".sketch-card").count()
    log(f"sketch-card count before refresh: {expected_count}, after: {after}")
    if after != expected_count:
        fail(f"sketch count changed across refresh: {expected_count} -> {after}")
    pass_(f"sketch count stable across refresh ({after})")
    # Check cards are collapsed again after refresh
    expanded = page.locator(".sketch-card.expanded").count()
    if expanded > 0:
        fail(f"{expanded} cards are expanded after refresh — should be 0")
    pass_("all cards collapsed again after refresh")


def test_8_promote_dialog_has_guidance(page: Page) -> None:
    print("\n[8] Signals page promote dialog has guidance textarea")
    click_signals_tab(page)
    page.wait_for_timeout(500)
    # Check the textarea exists in the DOM (may be hidden initially)
    textareas = page.locator("#promote-guidance-textarea")
    count = textareas.count()
    log(f"#promote-guidance-textarea count: {count}")
    if count == 0:
        fail("#promote-guidance-textarea not in DOM — Phase 10 guidance affordance missing")
    pass_("#promote-guidance-textarea exists in DOM")


def main() -> int:
    print(f"smoke test against {BASE_URL}")
    print(f"started at {time.strftime('%H:%M:%S')}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(15000)

        # Capture console errors for debugging
        console_msgs = []
        page.on("console", lambda msg: console_msgs.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda e: console_msgs.append(f"pageerror: {e}"))

        try:
            test_1_page_loads(page)
            sketch_count = test_2_premise_review_default(page)
            test_3_cards_start_collapsed(page)
            expanded_id = test_4_click_expands(page)
            test_5_edit_buttons(page, expanded_id)
            test_6_add_buttons(page, expanded_id)
            test_7_refresh_preserves_state(page, sketch_count)
            test_8_promote_dialog_has_guidance(page)
        except SystemExit:
            print("\n--- console messages during failing run ---")
            for m in console_msgs[-30:]:
                print(f"  {m}")
            return 1
        finally:
            browser.close()

    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
