import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Resources from "./pages/Resources";
import Alerts from "./pages/Alerts";
import Simulation from "./pages/Simulation";
import AIAssistant from "./pages/AIAssistant";
import ProtectedRoute from "./components/ProtectedRoute";

function Placeholder({ title }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#FFFDF8]">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-[#3D2918]">{title}</h1>
        <p className="mt-2 text-[#8B735D]">
          This section will be implemented next.
        </p>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route path="/signup" element={<Signup />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/alerts"
          element={
            <ProtectedRoute>
              <Alerts />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/resources"
          element={
            <ProtectedRoute>
              <Resources />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/digital-twin"
          element={<Placeholder title="Digital Twin" />}
        />

        <Route
          path="/dashboard/simulation"
          element={
            <ProtectedRoute>
              <Simulation />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/assistant"
          element={
            <ProtectedRoute>
              <AIAssistant />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/help"
          element={<Placeholder title="Help" />}
        />
      </Routes>
    </Router>
  );
}
