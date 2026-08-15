import { ArrowLeft, BookOpen, Layers, Zap, Bot } from "lucide-react";
import { useNavigate } from "react-router-dom";
import logoImg from "../assets/logo_varithon.png";

export default function Help() {
  const navigate = useNavigate();

  const sections = [
    {
      icon: <Layers size={24} className="text-[#D96F00]" />,
      title: "Digital Twin (Active)",
      description: "A real-time geospatial visualization of the event. Connects to the backend simulation engine via WebSocket to display live pilgrim movements, density, and crowd edges."
    },
    {
      icon: <Zap size={24} className="text-[#D96F00]" />,
      title: "What-If Simulation (Pending)",
      description: "Allows command center operators to test scenarios before execution. E.g., 'What if we close Route A?' Currently pending integration with the simulation forecasting API."
    },
    {
      icon: <BookOpen size={24} className="text-[#D96F00]" />,
      title: "Resource Optimization (Pending)",
      description: "AI-driven automated allocation of medical teams, ambulances, and volunteers to high-risk zones based on predictive analytics. Pending optimization engine."
    },
    {
      icon: <Bot size={24} className="text-[#D96F00]" />,
      title: "AI Assistant (Pending)",
      description: "Context-aware LLM integration for rapid operational querying. Will analyze live crowd telemetry and historical data to answer spatial questions in natural language."
    }
  ];

  return (
    <div className="min-h-screen bg-[#FFFDF8]">
      <header className="flex items-center justify-between border-b border-[#EDE2D0] bg-white px-4 py-3.5 md:px-8 md:py-4">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            className="rounded-lg p-2 text-[#6B421F] hover:bg-[#F8F1E5] cursor-pointer"
            aria-label="Back to dashboard"
          >
            <ArrowLeft size={20} />
          </button>

          <div className="flex items-center gap-2.5 sm:gap-3">
            <img
              src={logoImg}
              alt="VariSetu Logo"
              width="44"
              height="44"
              className="h-10 w-10 sm:h-11 sm:w-11 object-contain shrink-0"
            />
            <div>
              <h1 className="text-base sm:text-lg font-bold text-[#3D2918]">
                System Architecture
              </h1>
              <p className="text-xs text-[#8B735D] hidden xs:block">
                Understanding VariSetu Modules
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[1000px] p-4 md:p-8">
        <section className="mb-8 text-center">
          <h2 className="text-2xl font-bold text-[#3D2918] md:text-3xl">
            VariSetu Command Center Overview
          </h2>
          <p className="mt-4 mx-auto max-w-2xl text-sm leading-6 text-[#8B735D]">
            VariSetu is composed of four primary engines designed to provide situational awareness and decision intelligence for large-scale event management. Below is the current integration status.
          </p>
        </section>

        <section className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {sections.map((section, index) => (
            <div key={index} className="rounded-2xl border border-[#EDE2D0] bg-white p-6 transition hover:shadow-sm">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#F8E7CF]">
                {section.icon}
              </div>
              <h3 className="mt-4 font-bold text-[#3D2918] text-lg">
                {section.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-[#8B735D]">
                {section.description}
              </p>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
