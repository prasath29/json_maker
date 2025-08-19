from flask import Flask, request, send_file, jsonify
import io, json, hashlib, zipfile
from datetime import datetime, UTC

app = Flask(__name__)

@app.get("/")
def root():
    return jsonify({
        "status": "ok",
        "message": "POST /generate with JSON: username, password, project_name, project_id, store_password ('hash'|'plain')"
    })

@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    missing = [k for k in ["username","password","project_name","project_id"] if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    username = data["username"]
    password = data["password"]
    project_name = data["project_name"]
    project_id = data["project_id"]
    store_password = (data.get("store_password") or "hash").lower()
    if store_password not in {"hash","plain"}:
        return jsonify({"error": "store_password must be 'hash' or 'plain'"}), 400

    ts = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    credentials = {"username": username, "created_at": ts}
    if store_password == "plain":
        credentials["password"] = password
    else:
        credentials["password_hash"] = hashlib.sha256(password.encode("utf-8")).hexdigest()

    project = {
        "project_name": project_name,
        "project_id": project_id,
        "owner_username": username,
        "created_at": ts
    }

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("credentials.json", json.dumps(credentials, indent=2))
        zf.writestr("project.json", json.dumps(project, indent=2))
    buf.seek(0)
    print("Created buffer file:",buf)
    return send_file(
        buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{project_id or 'output'}-jsons.zip"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
