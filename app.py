#made by SAROJ_CODEX
import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
ADMIN_PASSWORDS = {"ROCKY_ADMIN", "SAROJ"}
MAX_PHOTOS = 200
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_photos():
    files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower().lstrip(".") in ALLOWED_EXTENSIONS]
    return sorted(files, key=lambda p: p.name.lower())

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/")
def index():
    photos = [url_for("uploaded_file", filename=p.name) for p in get_photos()]
    return render_template("index.html", photos=photos)

@app.route("/admin/login", methods=["POST"])
def admin_login():
    password = request.form.get("password", "")
    if password in ADMIN_PASSWORDS:
        session["admin"] = True
        return redirect(url_for("admin"))
    flash("Incorrect admin password.", "error")
    return redirect(url_for("index"))

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("index"))
    photos = get_photos()
    return render_template("admin.html", photos=photos, max_photos=MAX_PHOTOS)

@app.route("/admin/upload", methods=["POST"])
def upload():
    if not session.get("admin"):
        return redirect(url_for("index"))
    files = request.files.getlist("photos")
    current = len(get_photos())
    remaining = MAX_PHOTOS - current

    if remaining <= 0:
        flash("Maximum 200 photos reached.", "error")
        return redirect(url_for("admin"))

    saved = 0
    for file in files[:remaining]:
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename):
            continue

        original = secure_filename(file.filename)
        stem = Path(original).stem[:50] or "photo"
        ext = Path(original).suffix.lower()
        # Unique filename prevents collisions.
        filename = f"{stem}_{os.urandom(5).hex()}{ext}"
        file.save(UPLOAD_DIR / filename)
        saved += 1

    if saved:
        flash(f"{saved} photo(s) uploaded successfully.", "success")
    else:
        flash("No valid photos were uploaded.", "error")
    return redirect(url_for("admin"))

@app.route("/admin/delete/<filename>", methods=["POST"])
def delete_photo(filename):
    if not session.get("admin"):
        return jsonify({"ok": False}), 403
    safe = secure_filename(filename)
    target = UPLOAD_DIR / safe
    if target.exists() and target.is_file():
        target.unlink()
        return redirect(url_for("admin"))
    return redirect(url_for("admin"))

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5300"))
    app.run(host=host, port=port, debug=False)
    
#made by SAROJ_CODEX
