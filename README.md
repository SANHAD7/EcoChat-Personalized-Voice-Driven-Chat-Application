🎙️ EcoChat – A Personalized Voice-Driven Chat Application

📌 Overview

EcoChat is an AI-powered personalized voice-driven chat application that converts text messages into speech using voice cloning technology. Unlike traditional messaging applications, EcoChat allows users to communicate using their own cloned voices, creating a more natural and engaging communication experience.

The application leverages the Coqui XTTS v2 deep learning model to generate realistic speech from text while preserving the unique characteristics of a user's voice.

---
 ✨ Key Features

✅ Multi-user chat interface

✅ Personalized voice cloning

✅ AI-powered Text-to-Speech generation

✅ Voice sample upload for each user

✅ Real-time audio playback

✅ Chat history management

✅ SQLite database integration

✅ Modern and responsive user interface

---
 🛠️ Technologies Used

 Frontend

* React.js
* Vite
* HTML5
* CSS3
* JavaScript

Backend

* FastAPI
* Python

 Database

* SQLite

 Artificial Intelligence

* Coqui TTS
* XTTS v2 Voice Cloning Model
* Deep Learning-based Speech Synthesis

 Additional Tools

* FFmpeg
* Git & GitHub

---

 🧠 How AI Works in EcoChat

1. User uploads a voice sample.
2. The voice sample is stored securely.
3. User enters a text message.
4. FastAPI sends the text to the Coqui XTTS model.
5. XTTS analyzes the uploaded voice characteristics.
6. AI generates speech in the same voice.
7. The generated audio is returned to the chat interface.
8. Messages and audio paths are stored in SQLite.

---

 📂 Project Modules

 🎤 Voice Registration Module

Stores voice samples uploaded by users.

💬 Messaging Module

Handles sending and receiving text messages.

 🤖 Voice Generation Module

Generates personalized speech using Coqui XTTS v2.

 🔊 Audio Management Module

Manages generated audio files and playback.

 🗄️ Database Management Module

Stores user profiles, voice paths, and chat history.

 🖥️ User Interface Module

Provides an interactive and user-friendly chat environment.

---

 🧪 Database Structure

 Users Table

* User ID
* User Name
* Voice Sample Path

 Messages Table

* Message ID
* Sender ID
* Receiver ID
* Text Message
* Audio File Path

---

 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/SANHAD7/EcoChat-Personalized-Voice-Driven-Chat-Application.git
```

### Backend Setup

```bash
pip install fastapi uvicorn TTS
uvicorn app:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---
--- For converting voice into clear .wav form use command:
    ffmpeg -i voice.wav -ac 1 -ar 22050 -sample_fmt s16 new_voice.wav

 📸 Project Screenshots

All screenshots, outputs, and architecture diagrams are available in the **figures/** folder.

---

 🔮 Future Enhancements

* Emotion-based voice synthesis
* Mobile application support
* Voice-to-Voice communication
* Cloud database integration
* User authentication system
* Multimedia file sharing

---

 🎯 Conclusion

EcoChat demonstrates the practical application of Artificial Intelligence and Deep Learning in modern communication systems. By integrating voice cloning technology with web-based messaging, the project delivers a personalized, interactive, and innovative communication experience while showcasing the real-world potential of AI-powered speech synthesis.

---

 👨‍💻 Author

Syed Sanhad
B.Tech – Computer Science and Engineering
B.S. Abdur Rahman Crescent Institute of Science and Technology

🔗 GitHub: https://github.com/SANHAD7
