import os
import shutil
from TTS.api import TTS
from database import add_user, get_user, add_message, init_db

VOICE_DIR = "voices"

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

init_db()


def register_user(user_id, name, voice_file_path):
    os.makedirs(VOICE_DIR, exist_ok=True)

    new_voice_path = os.path.join(VOICE_DIR, f"{user_id}.wav")
    shutil.copy(voice_file_path, new_voice_path)

    add_user(user_id, name, new_voice_path)

    print(f"User {name} registered successfully!")


def generate_voice(sender_id, text, output_file):
    user = get_user(sender_id)

    if not user:
        raise Exception("User not found!")

    speaker_wav = user[2]

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="en",
        file_path=output_file
    )

    add_message(sender_id, text, output_file)

    print("Voice message generated:", output_file)
