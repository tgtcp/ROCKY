#made by SAROJ_CODEX
# ROCKY GALLERY — Professional Admin Gallery

## Features
- Professional responsive dark/glassmorphism photo gallery
- Admin-only photo upload through the small ⚙ settings button
- Admin password: `ROCKY_ADMIN`
- Maximum 200 photos
- Photos displayed one-by-one
- Auto slideshow every 5 seconds
- Previous/Next controls + keyboard arrow navigation
- Admin can delete photos
- Supports JPG, JPEG, PNG, GIF and WEBP
- Instagram logo/link in the footer\n- © 2026 SAROJ copyright at the very bottom
- Works locally or on a Flask-compatible host/VPS

## Run on Termux / Linux

```bash
pkg update -y
pkg install python -y
cd PRO_PHOTO_GALLERY
pip install -r requirements.txt
python app.py
```

Then open:
`http://127.0.0.1:5300`

For LAN access, the app listens on `0.0.0.0`.

## Change password safely
The default is `ROCKY_ADMIN`, but you can override it without editing code:

```bash
export ADMIN_PASSWORD="your-new-password"
export SECRET_KEY="a-long-random-secret"
python app.py
```

## Hosting
For a public deployment, use a Flask-compatible Python host/VPS and persistent storage for `uploads`, because uploaded photos are stored on disk.
#made by SAROJ_CODEX