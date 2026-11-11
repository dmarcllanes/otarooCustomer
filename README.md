# Otaroo public website

The public website is served by a FastHTML application. Its HTML, CSS, and JavaScript
live in [`site/`](./site/), with Nunito fonts in `assets/` and Otaroo the Turtle's
artwork in `assets/branding/newMascot/`. It does not replace or depend on the Otaroo
mobile app.

## Run locally

Install the pinned dependencies and start the FastHTML app from the repository root:

```sh
uv sync
uv run python main.py
```

Open [http://localhost:5001/](http://localhost:5001/). FastHTML serves the page at
`/`, the existing site files under `/site/`, and shared images and fonts under
`/assets/`.

For a production ASGI server, run:

```sh
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Configure links before launch

Edit [`site/config.js`](./site/config.js) and set these values to verified public
HTTPS store URLs:

- `appStoreUrl` — Otaroo's public iOS App Store page.
- `googlePlayUrl` — Otaroo's public Google Play page.

Until a store URL is configured, that download button stays hidden and the page
displays a setup note. The `/privacy` page provides Otaroo's detailed public Privacy
Policy (including `/privacy#account-deletion` for account deletion instructions) for
Apple App Store and Google Play Store submissions.

## Deployment

Deploy the repository with both `site/` and `assets/` available to the app, and
start the ASGI application with the production command above. The page uses
root-relative `/site/` and `/assets/` URLs, so deploy at a domain root and keep both
directories available to the app.

### Vercel

Vercel's Python runtime detects the ASGI app through the top-level `app` variable in
`main.py`. Its filesystem is read-only except `/tmp`, so on Vercel the app keeps
FastHTML's session key file in `/tmp`. The site does not use sessions, but you can set
a stable key with this optional environment variable:

- `SESSION_SECRET_KEY` (secret, optional): the FastHTML session signing key. If it is
  unset, a key is generated and stored in `.sesskey` locally or `/tmp/.sesskey` on
  Vercel.

The public domain is not configured in this repository. If you add an Open Graph
image preview, use its fully qualified production HTTPS URL in `site/index.html`.
