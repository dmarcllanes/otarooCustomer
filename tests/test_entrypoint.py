import ast
import unittest
from pathlib import Path

MAIN_PY = Path(__file__).resolve().parent.parent / "main.py"


class EntrypointTests(unittest.TestCase):
    def test_main_assigns_top_level_app_name_for_vercel(self):
        # Vercel detects the ASGI app by a plain top-level `app = ...` assignment;
        # tuple unpacking such as `app, rt = fast_app()` is not detected.
        tree = ast.parse(MAIN_PY.read_text(encoding="utf-8"))
        targets = [
            target.id
            for node in tree.body
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        ]
        self.assertIn("app", targets)


if __name__ == "__main__":
    unittest.main()
