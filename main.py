import os
from pathlib import Path

from fasthtml.common import fast_app, serve
from starlette.responses import FileResponse

ROOT_DIR = Path(__file__).parent
SITE_DIR = ROOT_DIR / "site"

# Vercel's filesystem is read-only except /tmp, so FastHTML cannot create its
# default .sesskey file there. Prefer an explicit secret from the environment.
SESSION_KEY_FILE = "/tmp/.sesskey" if os.environ.get("VERCEL") else ".sesskey"

# Assign `app` directly (not via tuple unpacking) so Vercel's Python runtime can
# detect the top-level ASGI entrypoint.
app = fast_app(
    static_path=str(ROOT_DIR),
    secret_key=os.environ.get("SESSION_SECRET_KEY"),
    key_fname=SESSION_KEY_FILE,
)[0]
rt = app.route


@rt("/")
def home():
    return FileResponse(SITE_DIR / "index.html")


@rt("/privacy")
def privacy():
    return FileResponse(SITE_DIR / "privacy.html")


if __name__ == "__main__":
    serve()
