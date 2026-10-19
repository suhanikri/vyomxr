"use client";

import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

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

type ActionOption = {
  id: string;
  label: string;
};

type Decision = {
  tick: number;
  action: string;
  subsystem: string | null;
  allowed: boolean;
  effect: string;
  message: string;
  fault_active: boolean;
  ticks_since_fault: number | null;
};

const EFFECT_STYLES: Record<string, { label: string; box: string }> = {
  resolved: {
    label: "Resolved",
    box: "bg-green-100 border-green-400 text-green-800",
  },
  partial: {
    label: "Partly helped",
    box: "bg-yellow-100 border-yellow-400 text-yellow-800",
  },
  worsened: {
    label: "Made it worse",
    box: "bg-red-100 border-red-400 text-red-800",
  },
  no_effect: {
    label: "No effect",
    box: "bg-gray-100 border-gray-400 text-gray-800",
  },
  rejected: {
    label: "Rejected",
    box: "bg-gray-100 border-gray-400 text-gray-800",
  },
};

const DEFAULT_EFFECT_STYLE = {
  label: "Result",
  box: "bg-gray-100 border-gray-400 text-gray-800",
};

export default function Dashboard() {
  const [state, setState] = useState<SpacecraftState | null>(null);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [asking, setAsking] = useState(false);

  const [actions, setActions] = useState<ActionOption[]>([]);
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [lastResult, setLastResult] = useState<Decision | null>(null);
  const [acting, setActing] = useState(false);
  const [actionError, setActionError] = useState("");

  useEffect(() => {
    const fetchState = () => {
      fetch(API + "/spacecraft/state")
        .then((res) => res.json())
        .then((data) => setState(data))
        .catch((err) => console.error("Failed to fetch spacecraft state:", err));

      fetch(API + "/spacecraft/anomalies")
        .then((res) => res.json())
        .then((data) => setAnomalies(data.anomalies))
        .catch((err) => console.error("Failed to fetch anomalies:", err));
    };

    fetchState();
    const interval = setInterval(fetchState, 2000);

    return () => clearInterval(interval);
  }, []);

  // Load the available actions and any earlier decisions once, on page load.
  useEffect(() => {
    fetch(API + "/spacecraft/actions")
      .then((res) => res.json())
      .then((data) => setActions(data.actions))
      .catch((err) => console.error("Failed to fetch actions:", err));

    fetch(API + "/spacecraft/decisions")
      .then((res) => res.json())
      .then((data) => setDecisions(data.decisions))
      .catch((err) => console.error("Failed to fetch decisions:", err));
  }, []);

  const refreshDecisions = () => {
    fetch(API + "/spacecraft/decisions")
      .then((res) => res.json())
      .then((data) => setDecisions(data.decisions))
      .catch((err) => console.error("Failed to fetch decisions:", err));
  };

  const handleAction = (actionId: string) => {
    setActing(true);
    setActionError("");

    fetch(API + "/spacecraft/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: actionId }),
    })
      .then((res) => res.json())
      .then((record: Decision) => {
        setLastResult(record);
        setActing(false);
        refreshDecisions();
      })
      .catch((err) => {
        console.error("Failed to send action:", err);
        setActionError("Could not send the action. Is the backend running?");
        setActing(false);
      });
  };

  const handleAsk = () => {
    if (!question.trim()) return;
    setAsking(true);

    fetch(API + "/mentor/ask", {
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

  const actionLabel = (id: string) => {
    const found = actions.find((a) => a.id === id);
    return found ? found.label : id;
  };

  if (!state) {
    return <main className="p-8">Loading spacecraft data...</main>;
  }

  const resultStyle = lastResult
    ? EFFECT_STYLES[lastResult.effect] || DEFAULT_EFFECT_STYLE
    : DEFAULT_EFFECT_STYLE;

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

      <section className="border rounded p-4 mb-6">
        <h2 className="font-semibold mb-1">Recovery Actions</h2>
        <p className="text-sm text-gray-500 mb-3">
          Investigate first, then choose. Every action is checked by the safety
          validator before it runs.
        </p>

        <div className="flex flex-wrap gap-2 mb-3">
          {actions.map((a) => (
            <button
              key={a.id}
              onClick={() => handleAction(a.id)}
              disabled={acting}
              className="bg-gray-800 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {a.label}
            </button>
          ))}
        </div>

        {actionError && (
          <div className="bg-red-100 border border-red-400 text-red-800 rounded p-3 mb-3">
            {actionError}
          </div>
        )}

        {lastResult && (
          <div className={"border rounded p-3 mb-3 " + resultStyle.box}>
            <strong>{resultStyle.label}:</strong> {lastResult.message}
          </div>
        )}

        {decisions.length > 0 && (
          <div>
            <h3 className="font-medium mb-1">Your recent decisions</h3>
            <ul className="text-sm space-y-1">
              {decisions
                .slice(-5)
                .reverse()
                .map((d, i) => (
                  <li key={i}>
                    Tick {d.tick}: {actionLabel(d.action)} -{" "}
                    {(EFFECT_STYLES[d.effect] || DEFAULT_EFFECT_STYLE).label}
                    {d.ticks_since_fault !== null &&
                      " (acted " + d.ticks_since_fault + " ticks after the fault began)"}
                  </li>
                ))}
            </ul>
          </div>
        )}
      </section>

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
