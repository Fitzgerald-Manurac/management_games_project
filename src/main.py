"""Entry point.

I-run gamit ang:
    python src/main.py
"""

import os
import sys

# Para gumana ang imports kahit saan i-run
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game  # noqa: E402


def ensure_supported_runtime():
    if sys.version_info[:2] < (3, 11):
        raise RuntimeError(
            "This game requires Python 3.11 or newer. "
            "Use the project virtual environment: .\\.venv\\Scripts\\python.exe src\\main.py"
        )

    try:
        import pygame  # noqa: F401
    except Exception as exc:  # pragma: no cover - runtime env check
        raise RuntimeError(
            "Pygame is not installed in the current environment. "
            "Run: .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt"
        ) from exc


def main():
    ensure_supported_runtime()
    Game().run()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Game startup failed: {exc}")
        print("Fix: cd to the project folder and run:")
        print("    .\\.venv\\Scripts\\python.exe src\\main.py")
        sys.exit(1)
