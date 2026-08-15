import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Solution from "./pages/Solution";
import Dashboard from "./pages/Dashboard";
import Resources from "./pages/Resources";
import Alerts from "./pages/Alerts";
import Simulation from "./pages/Simulation";
import AIAssistant from "./pages/AIAssistant";
import Help from "./pages/Help";
import ProtectedRoute from "./components/ProtectedRoute";

import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";
import { useState } from "react";
import DigitalTwinMap from "./components/digital-twin/DigitalTwinMap";



// A layout wrapper for dashboard pages to include sidebar and topbar
function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  
  return (
    <div className="flex h-screen overflow-hidden bg-[#F8F1E5]">
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      
      <div className="flex flex-1 flex-col overflow-hidden lg:ml-64">
        <Topbar setMobileOpen={setMobileOpen} />
        
        <main className="flex-1 overflow-y-auto overflow-x-hidden p-3 sm:p-5 md:p-8">
          {children}
        </main>
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
        <Route path="/solution" element={<Solution />} />

        {/* Dashboard Routes wrapped in ProtectedRoute and DashboardLayout */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardLayout><Dashboard /></DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/dashboard/alerts" element={
          <ProtectedRoute>
            <DashboardLayout><Alerts /></DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/dashboard/resources" element={
          <ProtectedRoute>
            <DashboardLayout><Resources /></DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/dashboard/digital-twin" element={
          <ProtectedRoute>
            <DashboardLayout>
              {/* REAL Digital Twin Engine integrated into new shell */}
              <div className="flex-1 flex flex-col h-full min-h-[600px] bg-slate-900 rounded-xl overflow-hidden shadow-md">
                <DigitalTwinMap />
              </div>
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/dashboard/simulation" element={
          <ProtectedRoute>
            <DashboardLayout><Simulation /></DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/dashboard/assistant" element={
          <ProtectedRoute>
            <DashboardLayout><AIAssistant /></DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/dashboard/help" element={
          <ProtectedRoute>
            <DashboardLayout><Help /></DashboardLayout>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}
