"use client";

import { useEffect, useState } from "react";

type SpacecraftState = {
  timestamp: string;
  battery_voltage: number;
  battery_current: number;
  battery_percentage: number;
  temperature: number;
  roll: number;
  pitch: number;
  yaw: number;
  angular_velocity: number;
  signal_strength: number;
  packet_loss: number;
  link_status: string;
};

type Anomaly = {
  subsystem: string;
  reading: number | string;
  reason: string;
  severity: string;
};

type ChatMessage = {
  question: string;
  answer: string;
};

export default function Dashboard() {
  const [state, setState] = useState<SpacecraftState | null>(null);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [asking, setAsking] = useState(false);

  useEffect(() => {
    const fetchState = () => {
      fetch("http://127.0.0.1:8000/spacecraft/state")
        .then((res) => res.json())
        .then((data) => setState(data))
        .catch((err) => console.error("Failed to fetch spacecraft state:", err));

      fetch("http://127.0.0.1:8000/spacecraft/anomalies")
        .then((res) => res.json())
        .then((data) => setAnomalies(data.anomalies))
        .catch((err) => console.error("Failed to fetch anomalies:", err));
    };

    fetchState();
    const interval = setInterval(fetchState, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleAsk = () => {
    if (!question.trim()) return;
    setAsking(true);

    fetch("http://127.0.0.1:8000/mentor/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
      .then((res) => res.json())
      .then((data) => {
        setChatHistory((prev) => [...prev, { question, answer: data.answer }]);
        setQuestion("");
        setAsking(false);
      })
      .catch((err) => {
        console.error("Failed to ask mentor:", err);
        setAsking(false);
      });
  };

  if (!state) {
    return <main className="p-8">Loading spacecraft data...</main>;
  }

  return (
    <main className="p-8 font-sans">
      <h1 className="text-2xl font-bold mb-4">VyomXR Mission Dashboard</h1>
      <p className="text-sm text-gray-500 mb-6">Last updated: {state.timestamp}</p>

      <div className="mb-6">
        {anomalies.length === 0 ? (
          <div className="bg-green-100 border border-green-400 text-green-800 rounded p-4">
            All systems nominal
          </div>
        ) : (
          <div className="space-y-2">
            {anomalies.map((a, i) => (
              <div
                key={i}
                className={
                  a.severity === "high"
                    ? "bg-red-100 border border-red-400 text-red-800 rounded p-4"
                    : "bg-yellow-100 border border-yellow-400 text-yellow-800 rounded p-4"
                }
              >
                <strong>[{a.subsystem.toUpperCase()}]</strong> {a.reason}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <section className="border rounded p-4">
          <h2 className="font-semibold mb-2">Power</h2>
          <p>Voltage: {state.battery_voltage} V</p>
          <p>Current: {state.battery_current} A</p>
          <p>Battery: {state.battery_percentage}%</p>
        </section>

        <section className="border rounded p-4">
          <h2 className="font-semibold mb-2">Thermal</h2>
          <p>Temperature: {state.temperature} degrees C</p>
        </section>

        <section className="border rounded p-4">
          <h2 className="font-semibold mb-2">Attitude</h2>
          <p>Roll: {state.roll}</p>
          <p>Pitch: {state.pitch}</p>
          <p>Yaw: {state.yaw}</p>
          <p>Angular velocity: {state.angular_velocity}</p>
        </section>

        <section className="border rounded p-4">
          <h2 className="font-semibold mb-2">Communication</h2>
          <p>Signal strength: {state.signal_strength}%</p>
          <p>Packet loss: {state.packet_loss}</p>
          <p>Link status: {state.link_status}</p>
        </section>
      </div>

      <section className="border rounded p-4">
        <h2 className="font-semibold mb-3">AI Mentor</h2>

        <div className="space-y-3 mb-4 max-h-64 overflow-y-auto">
          {chatHistory.map((msg, i) => (
            <div key={i}>
              <p className="font-medium">You: {msg.question}</p>
              <p className="text-gray-700">Mentor: {msg.answer}</p>
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Ask the AI Mentor a question..."
            className="border rounded px-3 py-2 flex-1"
          />
          <button
            onClick={handleAsk}
            disabled={asking}
            className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {asking ? "Asking..." : "Ask"}
          </button>
        </div>
      </section>
    </main>
  );
}
