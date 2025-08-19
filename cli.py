#!/usr/bin/env python3
import argparse, hashlib, json, os
from datetime import datetime, UTC

def write_json_files(username, password, project_name, project_id, store_password_mode="hash", out_dir="output"):
    ts = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    os.makedirs(out_dir, exist_ok=True)

    cred = {"username": username, "created_at": ts}
    if store_password_mode == "plain":
        cred["password"] = password
    else:
        cred["password_hash"] = hashlib.sha256(password.encode("utf-8")).hexdigest()

    proj = {
        "project_name": project_name,
        "project_id": project_id,
        "owner_username": username,
        "created_at": ts
    }

    cred_path = os.path.join(out_dir, "credentials.json")
    proj_path = os.path.join(out_dir, "project.json")
    with open(cred_path, "w", encoding="utf-8") as f:
        json.dump(cred, f, indent=2)
    with open(proj_path, "w", encoding="utf-8") as f:
        json.dump(proj, f, indent=2)

    return cred_path, proj_path

def main():
    p = argparse.ArgumentParser(description="Generate two JSON files from inputs.")
    p.add_argument("--username", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--project-name", required=True)
    p.add_argument("--project-id", required=True)
    p.add_argument("--out-dir", default="output")
    p.add_argument("--store-password", choices=["hash", "plain"], default="hash")
    args = p.parse_args()

    cred_path, proj_path = write_json_files(
        args.username, args.password, args.project_name, args.project_id,
        store_password_mode=args.store_password, out_dir=args.out_dir
    )
    print(f"Written:\n {cred_path}\n {proj_path}")

if __name__ == "__main__":
    main()



