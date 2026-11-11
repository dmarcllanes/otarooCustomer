import re
import struct
import unittest
import zlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT_DIR / "site" / "index.html"
PRIVACY_HTML = ROOT_DIR / "site" / "privacy.html"
STYLES_CSS = ROOT_DIR / "site" / "styles.css"


class SitePrivacyTests(unittest.TestCase):
    def test_index_privacy_section_links_to_dedicated_privacy_page(self):
        html = INDEX_HTML.read_text(encoding="utf-8")
        self.assertIn('id="privacy"', html)
        self.assertIn('href="/privacy"', html)
        self.assertIn("Read full Privacy Policy", html)

    def test_privacy_page_is_indexable_and_complete_for_store_submission(self):
        html = PRIVACY_HTML.read_text(encoding="utf-8")
        self.assertNotIn("noindex", html.lower())
        self.assertNotIn("[NEEDS CONFIRMATION]", html)
        self.assertIn("Dan Marc Llanes", html)
        self.assertIn("dandigital1688@gmail.com", html)
        self.assertIn("Supabase", html)
        self.assertIn("Sign in with Apple", html)
        self.assertIn("Google Sign-In", html)

        expected_sections = [
            "scope",
            "information-we-collect",
            "device-permissions",
            "how-we-use-data",
            "third-party-services",
            "store-data-safety",
            "account-deletion",
            "data-security",
            "your-rights",
            "children",
            "changes-and-contact",
        ]
        for section_id in expected_sections:
            self.assertIn(f'id="{section_id}"', html)
            self.assertIn(f'href="#{section_id}"', html)

    def test_referenced_local_assets_exist(self):
        for page in (INDEX_HTML, PRIVACY_HTML):
            html = page.read_text(encoding="utf-8")
            paths = re.findall(r'(?:src|href)="(/(?:assets|site)/[^"#?]+)"', html)
            self.assertTrue(paths, f"Expected asset paths in {page.name}")
            for rel_path in paths:
                disk_path = ROOT_DIR / rel_path.lstrip("/")
                self.assertTrue(
                    disk_path.is_file(),
                    f"Missing referenced asset {rel_path} in {page.name}",
                )

    def test_referenced_mascot_images_have_transparent_background(self):
        for page in (INDEX_HTML, PRIVACY_HTML):
            html = page.read_text(encoding="utf-8")
            mascot_paths = re.findall(
                r'src="(/(?:assets/branding/newMascot|assets/mascot)/[^"#?]+\.png)"',
                html,
            )
            self.assertTrue(mascot_paths)
            for rel_path in mascot_paths:
                data = (ROOT_DIR / rel_path.lstrip("/")).read_bytes()
                _, _, _, color_type = struct.unpack(">IIBB", data[16:26])
                self.assertEqual(
                    color_type,
                    6,
                    f"{rel_path} should be RGBA (color_type=6) with transparency",
                )
                pos = 8
                idat = bytearray()
                while pos < len(data):
                    length, ctype = struct.unpack(">I4s", data[pos : pos + 8])
                    if ctype == b"IDAT":
                        idat.extend(data[pos + 8 : pos + 8 + length])
                    pos += 12 + length
                raw = zlib.decompress(bytes(idat))
                top_left_alpha = raw[4]
                self.assertEqual(
                    top_left_alpha,
                    0,
                    f"{rel_path} top-left pixel should be transparent (alpha=0)",
                )


if __name__ == "__main__":
    unittest.main()
