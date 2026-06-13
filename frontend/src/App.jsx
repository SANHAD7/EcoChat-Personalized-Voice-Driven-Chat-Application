import { useEffect, useRef, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const CONTACTS = [
  { id: "nawaz", name: "Nawaz" },
  { id: "maaz", name: "Maaz" },
  { id: "nikki", name: "Nikki" },
  { id: "radhika", name: "Radhika Mam" },
  { id: "vijayalakshmi", name: "Vijayalakshmi Mam" },
  { id: "azeez", name: "Azeez" },
  { id: "apj", name: "APJ Abdul Kalam" },

  // NEW CONTACTS
  { id: "malik", name: "Malik" },
  { id: "rahul", name: "Rahul" },
  { id: "faiz", name: "Faiz" },
  { id: "fayaz", name: "Fayaz" },
  { id: "hussain", name: "Hussain" },
  { id: "asif", name: "Asif" },
  { id: "sarvana", name: "Sarvana" },
  { id: "shrish", name: "Shrish" },
  { id: "sugandhan", name: "Sugandhan" },
  { id: "priya", name: "Priya" },
  { id: "ayesha", name: "Ayesha" },
  { id: "salma", name: "Salma" },
];

const ME = "syed";

export default function App() {
  const [active, setActive] = useState(CONTACTS[0]);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [status, setStatus] = useState("");

  const myVoiceRef = useRef(null);
  const contactVoiceRefs = useRef({});
  const attachRef = useRef(null);

  // Load messages
  const loadMessages = async () => {
    const res = await fetch(
      `${API}/messages?user1=${ME}&user2=${active.id}`
    );
    const data = await res.json();
    setMessages(data);
  };

  useEffect(() => {
    loadMessages();
  }, [active]);

  // Upload voice
  const uploadVoice = async (userId, file) => {
    if (!file) return;

    const fd = new FormData();
    fd.append("user_id", userId);
    fd.append("file", file);

    await fetch(`${API}/upload_voice`, {
      method: "POST",
      body: fd,
    });

    alert(`Voice uploaded for ${userId}`);
  };

  // Send message
  const sendMessage = async () => {
    if (!text.trim()) return;

    setStatus("Generating your voice...");

    const fd = new FormData();
    fd.append("sender_id", ME);
    fd.append("receiver_id", active.id);
    fd.append("text", text);

    await fetch(`${API}/send_message`, {
      method: "POST",
      body: fd,
    });

    setText("");
    setStatus("");
    loadMessages();
  };

  // Receive message
  const receiveMessage = async () => {
    if (!text.trim()) return;

    setStatus(`${active.name} is speaking...`);

    const fd = new FormData();
    fd.append("sender_id", active.id);
    fd.append("receiver_id", ME);
    fd.append("text", text);

    await fetch(`${API}/send_message`, {
      method: "POST",
      body: fd,
    });

    setText("");
    setStatus("");
    loadMessages();
  };

  const timeNow = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  return (
    <div className="app">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>EchoChat</h2>

        <div className="profile">
          <span><b>You (Syed)</b></span>
          <button className="plus" onClick={() => myVoiceRef.current.click()}>
            +
          </button>
          <input
            type="file"
            hidden
            ref={myVoiceRef}
            onChange={(e) => uploadVoice(ME, e.target.files[0])}
          />
        </div>

        <hr />

        {CONTACTS.map((c) => (
          <div
            key={c.id}
            className={`contact ${active.id === c.id ? "active" : ""}`}
            onClick={() => setActive(c)}
          >
            <span>{c.name}</span>
            <button
              className="plus"
              onClick={(e) => {
                e.stopPropagation();
                contactVoiceRefs.current[c.id].click();
              }}
            >
              +
            </button>
            <input
              type="file"
              hidden
              ref={(el) => (contactVoiceRefs.current[c.id] = el)}
              onChange={(e) => uploadVoice(c.id, e.target.files[0])}
            />
          </div>
        ))}
      </div>

      {/* Chat */}
      <div className="chat">
        <div className="chat-header">
          Chat with {active.name}
        </div>

        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={m[0] === ME ? "me" : "them"}>
              <p>{m[1]}</p>
              <audio controls src={`${API}/${m[2]}`} />
              <div className="time">{timeNow()}</div>
            </div>
          ))}
        </div>

        <div className="input">
          <button
            className="attach"
            onClick={() => {
              alert("File / Photo sending will be added next ");
              attachRef.current.click();
            }}
          >
            +
          </button>

          <input ref={attachRef} type="file" hidden />

          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type a message"
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
          <button onClick={receiveMessage}>Receive</button>
        </div>

        {status && <div className="status">{status}</div>}
      </div>
    </div>
  );
}