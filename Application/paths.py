"""Central, working-directory-independent path definitions.

Every asset/data path in the game is derived from this module instead of being
hardcoded as a relative string, so the game runs the same whether it is
launched from an IDE, a terminal, or a double-clicked shortcut, regardless of
the current working directory.
"""
from pathlib import Path

APPLICATION_DIR = Path(__file__).resolve().parent
ROOT_DIR = APPLICATION_DIR.parent
ASSETS_DIR = ROOT_DIR / "Assets"
SCORE_FILE = APPLICATION_DIR / "score_data.json"
