"""CLI entry point for Open Brush AI."""

from __future__ import annotations

import argparse
import sys

from .client import OpenBrushClient
from .config import COMMAND_DELAY, DEFAULT_MODEL, ExecutionMode
from .styles import list_styles


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="open-brush-ai",
        description="AI-powered painting controller for Open Brush VR",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="What to paint (e.g. 'a sunset over mountains')",
    )
    parser.add_argument(
        "--style", "-s",
        help=f"Painting style. Built-in: {', '.join(list_styles())}. "
        "Or use any freeform style description.",
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["live", "mock", "record"],
        default="mock",
        help="Execution mode (default: mock)",
    )
    parser.add_argument(
        "--playback", "-p",
        help="Replay a saved recording JSON file",
    )
    parser.add_argument(
        "--demo", "-d",
        choices=["hello", "landscape", "abstract"],
        help="Run a built-in demo (no API key needed)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=COMMAND_DELAY,
        help=f"Seconds between commands in live mode (default: {COMMAND_DELAY})",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Enter interactive REPL mode",
    )
    parser.add_argument(
        "--url",
        default=None,
        help="Open Brush API URL (default: http://localhost:40074/api/v1)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--list-styles",
        action="store_true",
        help="List available painting styles",
    )
    return parser.parse_args()


def make_client(args: argparse.Namespace) -> OpenBrushClient:
    """Create an OpenBrushClient from CLI args."""
    kwargs: dict = {
        "mode": ExecutionMode(args.mode),
        "delay": args.delay,
    }
    if args.url:
        kwargs["base_url"] = args.url
    return OpenBrushClient(**kwargs)


def run_demo(args: argparse.Namespace) -> None:
    """Run a built-in demo."""
    client = make_client(args)

    if args.demo == "hello":
        from demos.hello_world import run
    elif args.demo == "landscape":
        from demos.landscape import run
    elif args.demo == "abstract":
        from demos.abstract import run
    else:
        print(f"Unknown demo: {args.demo}")
        sys.exit(1)

    run(client)


def run_playback(args: argparse.Namespace) -> None:
    """Replay a saved recording."""
    client = make_client(args)
    recording = OpenBrushClient.load_recording(args.playback)
    print(f"  📼 Replaying: {recording.prompt}")
    if recording.style:
        print(f"     Style: {recording.style}")
    client.execute_plan(recording.plan)


def run_paint(args: argparse.Namespace) -> None:
    """Generate and execute a painting from a prompt."""
    from .painter import AIPainter

    client = make_client(args)
    painter = AIPainter(client=client, model=args.model)
    plan = painter.paint(args.prompt, style=args.style)

    if args.mode == "record":
        client.save_recording(args.prompt, plan, style=args.style)


def run_repl(args: argparse.Namespace) -> None:
    """Interactive REPL for painting."""
    from .painter import AIPainter

    client = make_client(args)
    painter = AIPainter(client=client, model=args.model)

    print("\n" + "=" * 60)
    print("  Open Brush AI — Interactive Mode")
    print("  Type a scene description to paint it.")
    print("  Commands: /style <name>, /demo <name>, /save, /quit")
    print("=" * 60 + "\n")

    current_style = args.style

    while True:
        try:
            prompt = input("  🎨 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            break

        if not prompt:
            continue

        if prompt.lower() in ("/quit", "/exit", "/q"):
            print("  Bye!")
            break

        if prompt.lower().startswith("/style"):
            parts = prompt.split(maxsplit=1)
            if len(parts) > 1:
                current_style = parts[1]
                print(f"  Style set to: {current_style}")
            else:
                print(f"  Current style: {current_style or 'none'}")
                print(f"  Available: {', '.join(list_styles())}")
            continue

        if prompt.lower().startswith("/demo"):
            parts = prompt.split(maxsplit=1)
            if len(parts) > 1:
                args.demo = parts[1]
                run_demo(args)
            else:
                print("  Available demos: hello, landscape, abstract")
            continue

        if prompt.lower() == "/save":
            if client._command_log:
                # Save last plan if we have one
                print("  Use --mode record to save paintings automatically.")
            else:
                print("  Nothing to save yet.")
            continue

        if prompt.lower() == "/styles":
            from .styles import STYLES
            for key, s in STYLES.items():
                print(f"  {key:15s} — {s.description[:60]}...")
            continue

        try:
            painter.paint(prompt, style=current_style)
        except Exception as e:
            print(f"  ✗ Error: {e}")


def show_styles() -> None:
    """Print available styles with descriptions."""
    from .styles import STYLES
    print("\nAvailable painting styles:\n")
    for key, s in STYLES.items():
        print(f"  {key:15s} — {s.name}")
        print(f"  {'':15s}   {s.description[:70]}...")
        print(f"  {'':15s}   Brushes: {', '.join(s.preferred_brushes)}")
        print()


def main() -> None:
    args = parse_args()

    if args.list_styles:
        show_styles()
        return

    if args.demo:
        run_demo(args)
    elif args.playback:
        run_playback(args)
    elif args.interactive:
        run_repl(args)
    elif args.prompt:
        run_paint(args)
    else:
        parse_args()  # Will show help since no args
        print("\nExamples:")
        print('  python -m open_brush_ai "paint a sunset over mountains"')
        print('  python -m open_brush_ai "a dragon" --style fire')
        print('  python -m open_brush_ai --demo landscape')
        print('  python -m open_brush_ai --interactive')
        print('  python -m open_brush_ai --list-styles')


if __name__ == "__main__":
    main()
