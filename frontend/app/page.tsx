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

export default function Dashboard() {
  const [state, setState] = useState<SpacecraftState | null>(null);

  useEffect(() => {
    const fetchState = () => {
      fetch("http://127.0.0.1:8000/spacecraft/state")
        .then((res) => res.json())
        .then((data) => setState(data))
        .catch((err) => console.error("Failed to fetch spacecraft state:", err));
    };

    fetchState();
    const interval = setInterval(fetchState, 2000);

    return () => clearInterval(interval);
  }, []);

  if (!state) {
    return <main className="p-8">Loading spacecraft data...</main>;
  }

  return (
    <main className="p-8 font-sans">
      <h1 className="text-2xl font-bold mb-4">VyomXR Mission Dashboard</h1>
      <p className="text-sm text-gray-500 mb-6">Last updated: {state.timestamp}</p>

      <div className="grid grid-cols-2 gap-4">
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
    </main>
  );
}
