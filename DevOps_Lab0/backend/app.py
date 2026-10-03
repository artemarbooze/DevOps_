import os

import psycopg
from flask import Flask, jsonify, request

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://notes:notes@localhost:5432/notes"
)

INSTANCE_ID = os.environ.get("INSTANCE_ID", "backend-1")
PORT = int(os.environ.get("PORT", "8000"))

app = Flask(__name__, static_folder="../frontend", static_url_path="")


def db():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT now()
            )
            """
        )


@app.after_request
def add_instance_header(response):
    response.headers["X-Instance-Id"] = INSTANCE_ID
    return response


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/notes")
def list_notes():
    with db() as conn:
        rows = conn.execute(
            "SELECT id, text, created_at FROM notes ORDER BY id DESC"
        ).fetchall()
    notes = [
        {"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows
    ]
    return jsonify(instance=INSTANCE_ID, notes=notes)


@app.post("/api/notes")
def add_note():
    text = (request.get_json(silent=True) or {}).get("text", "").strip()
    if not text:
        return jsonify(error="text is required"), 400
    with db() as conn:
        note_id = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id", (text,)
        ).fetchone()[0]
    return jsonify(instance=INSTANCE_ID, id=note_id, text=text), 201


@app.get("/api/health")
def health():
    return jsonify(status="ok", instance=INSTANCE_ID)


if __name__ == "__main__":
    init_db()
    print(f"Сервис запущен: http://localhost:{PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)
