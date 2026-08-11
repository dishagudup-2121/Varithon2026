import { useEffect, useState } from "react";
import axios from "axios";

type Health = { status: string; version: string };

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);

  useEffect(() => {
    axios.get<Health>("http://localhost:8000/api/health")
      .then((response) => setHealth(response.data))
      .catch(() => setHealth(null));
  }, []);

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">VARI OS</h1>
      <p className="mt-2">Predict → Recommend → Simulate → Approve → Act</p>
      <p className="mt-6">
        Backend: {health ? `${health.status} (${health.version})` : "not connected"}
      </p>
    </main>
  );
}
