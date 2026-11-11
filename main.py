from pathlib import Path

from fasthtml.common import fast_app, serve
from starlette.responses import FileResponse

ROOT_DIR = Path(__file__).parent
SITE_DIR = ROOT_DIR / "site"

app, rt = fast_app(static_path=str(ROOT_DIR))


@rt("/")
def home():
    return FileResponse(SITE_DIR / "index.html")


@rt("/privacy")
def privacy():
    return FileResponse(SITE_DIR / "privacy.html")


if __name__ == "__main__":
    serve()
