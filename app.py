from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, os, uuid, shutil

from TTS.api import TTS

DB = "ecochat.db"
VOICE_DIR = "voices"
OUT_DIR = "temp_audio"

os.makedirs(VOICE_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STATIC AUDIO SERVING ----------------
app.mount("/temp_audio", StaticFiles(directory=OUT_DIR), name="temp_audio")

# ---------------- LOAD XTTS ----------------
print("Loading XTTS model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
print("XTTS loaded")

def db():
    return sqlite3.connect(DB)

# =====================================================
# Upload voice sample
# =====================================================
@app.post("/upload_voice")
async def upload_voice(user_id: str = Form(...), file: UploadFile = File(...)):
    path = f"{VOICE_DIR}/{user_id}.wav"

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    con = db()
    cur = con.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (id,name,voice_path) VALUES (?,?,?)",
        (user_id, user_id, path),
    )
    con.commit()
    con.close()

    return {"status": "ok"}

# =====================================================
# SEND MESSAGE (YOUR VOICE ONLY)
# =====================================================
@app.post("/send_message")
async def send_message(
    sender_id: str = Form(...),
    receiver_id: str = Form(...),
    text: str = Form(...)
):
    con = db()
    cur = con.cursor()

    cur.execute("SELECT voice_path FROM users WHERE id=?", (sender_id,))
    row = cur.fetchone()

    if not row:
        return {"error": "Sender voice not uploaded"}

    out_file = f"{uuid.uuid4()}.wav"
    out_path = os.path.join(OUT_DIR, out_file)

    tts.tts_to_file(
        text=text,
        speaker_wav=row[0],
        language="en",
        file_path=out_path
    )

    cur.execute(
        "INSERT INTO messages (sender_id,receiver_id,text,audio_path) VALUES (?,?,?,?)",
        (sender_id, receiver_id, text, f"temp_audio/{out_file}")
    )

    con.commit()
    con.close()

    return {"status": "sent"}

# =====================================================
# RECEIVE MESSAGE (CONTACT VOICE – MANUAL)
# =====================================================
@app.post("/receive_message")
async def receive_message(
    sender_id: str = Form(...),
    receiver_id: str = Form(...),
    text: str = Form(...)
):
    con = db()
    cur = con.cursor()

    cur.execute("SELECT voice_path FROM users WHERE id=?", (sender_id,))
    row = cur.fetchone()

    if not row:
        return {"error": "Contact voice not uploaded"}

    out_file = f"{uuid.uuid4()}.wav"
    out_path = os.path.join(OUT_DIR, out_file)

    tts.tts_to_file(
        text=text,
        speaker_wav=row[0],
        language="en",
        file_path=out_path
    )

    cur.execute(
        "INSERT INTO messages (sender_id,receiver_id,text,audio_path) VALUES (?,?,?,?)",
        (sender_id, receiver_id, text, f"temp_audio/{out_file}")
    )

    con.commit()
    con.close()

    return {"status": "received"}

# =====================================================
# FETCH CHAT HISTORY
# =====================================================
@app.get("/messages")
def get_messages(user1: str, user2: str):
    con = db()
    cur = con.cursor()

    cur.execute("""
        SELECT sender_id, text, audio_path
        FROM messages
        WHERE (sender_id=? AND receiver_id=?)
           OR (sender_id=? AND receiver_id=?)
        ORDER BY id
    """, (user1, user2, user2, user1))

    rows = cur.fetchall()
    con.close()
    return rows
