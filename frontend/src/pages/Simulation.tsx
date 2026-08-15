import { useEffect, useState } from "react";

import {
  ArrowLeft,
  FlaskConical,
  Play,
  RotateCcw,
} from "lucide-react";

import { useNavigate, useSearchParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import ScenarioCard from "../components/simulation/ScenarioCard";
import HelpButton from "../components/common/HelpButton";
import HowItWorks from "../components/common/HowItWorks";
import logoImg from "../assets/logo_varithon.png";
import { SimulationScenario } from "../types";

const scenarios: SimulationScenario[] = [
  { id: "s1", titleKey: "simulation.scenarios.closeRoute.title", descriptionKey: "simulation.scenarios.closeRoute.desc", description: "Close Route", icon: "route" },
  { id: "s2", titleKey: "simulation.scenarios.deployVolunteers.title", descriptionKey: "simulation.scenarios.deployVolunteers.desc", description: "Deploy Volunteers", icon: "volunteers" },
  { id: "s3", titleKey: "simulation.scenarios.deployAmbulance.title", descriptionKey: "simulation.scenarios.deployAmbulance.desc", description: "Deploy Ambulance", icon: "ambulance" }
];

export default function Simulation() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const resource = searchParams.get("resource");
  const target = searchParams.get("target");

  const [selectedScenario, setSelectedScenario] =
    useState<SimulationScenario | null>(null);

  const [helpOpen, setHelpOpen] = useState(false);
  const [showPending, setShowPending] = useState(false);

  useEffect(() => {
    if (resource) {
      const el = document.getElementById(resource);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, [resource]);

  const runSimulation = () => {
    if (!selectedScenario) return;
    setShowPending(true);
  };

  const resetSimulation = () => {
    setSelectedScenario(null);
    setShowPending(false);
  };

  return (
    <div className="min-h-screen bg-[#FFFDF8]">

      {/* Header */}

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
                {t("simulation.title")}
              </h1>

              <p className="text-xs text-[#8B735D] hidden xs:block">
                {t("simulation.subtitle")}
              </p>
            </div>
          </div>

        </div>

        <HelpButton
          onClick={() => setHelpOpen(true)}
        />

      </header>

      <main className="mx-auto max-w-[1500px] p-4 md:p-8">

        {/* Intro */}

        <section className="mb-7">

          <p className="text-sm font-medium text-[#E86F00]">
            {t("simulation.commandCenter")}
          </p>

          <h2 className="mt-1 text-2xl font-bold text-[#3D2918] md:text-3xl">
            {t("simulation.pageTitle")}
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-[#8B735D]">
            {t("simulation.pageDescription")}
          </p>

          {resource && (
            <div className="mt-5 rounded-2xl border border-[#E8D3B5] bg-[#FFF8EC] p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-[#9B836B]">
                {t("simulation.selectedResource")}
              </p>

              <div className="mt-2 flex flex-wrap items-center gap-2">
                <span className="font-bold text-[#3D2918]">
                  {resource}
                </span>

                <span className="text-[#9B836B]">
                  →
                </span>

                <span className="font-bold text-[#E86F00]">
                  {target || "High Risk Zone"}
                </span>
              </div>

              <p className="mt-2 text-xs text-[#8B735D]">
                {t("simulation.selectedResourceDescription")}
              </p>
            </div>
          )}

        </section>

        {/* Scenario selection */}

        <section>

          <div className="mb-4 flex items-center justify-between">

            <div className="flex items-center gap-2">

              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#F8E7CF] text-[#E86F00]">
                <FlaskConical size={18} />
              </div>

              <div>
                <h2 className="font-bold text-[#3D2918]">
                  {t("simulation.chooseScenario")}
                </h2>

                <p className="text-xs text-[#8B735D]">
                  {t("simulation.chooseScenarioSubtitle")}
                </p>
              </div>

            </div>

            {showPending && (
              <button
                type="button"
                onClick={resetSimulation}
                className="flex items-center gap-2 rounded-xl border border-[#EDE2D0] bg-white px-3 py-2 text-xs font-semibold text-[#6B421F] hover:bg-[#F8F1E5] cursor-pointer"
              >
                <RotateCcw size={14} />
                {t("simulation.reset")}
              </button>
            )}

          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">

            {scenarios.map((scenario: SimulationScenario) => (
              <ScenarioCard
                key={scenario.id}
                scenario={scenario}
                selected={
                  selectedScenario?.id === scenario.id
                }
                onSelect={setSelectedScenario}
              />
            ))}

          </div>

          <div className="mt-5 flex justify-end">

            <button
              type="button"
              onClick={runSimulation}
              disabled={!selectedScenario}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-[#F28C00] to-[#FF5A00] px-6 py-3 text-sm font-semibold text-white transition hover:from-[#E86F00] hover:to-[#E05000] disabled:cursor-not-allowed disabled:opacity-40 cursor-pointer shadow-md"
            >
              <Play size={16} />
              {t("simulation.run")}
            </button>

          </div>

        </section>

        {/* Results */}

        {showPending && (
          <section className="mt-8">
            <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-[#DECFBE] bg-[#FAF5EE] text-center p-12">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-[#F28C00]/10 text-[#D96F00] mb-4">
                <FlaskConical size={28} />
              </div>
              <p className="font-bold text-[#3D2918] text-lg mb-2">
                Backend Integration Pending
              </p>
              <p className="text-sm text-[#8B735D] max-w-sm leading-relaxed">
                The What-If Simulation engine API is not yet connected. Simulation execution is currently disabled.
              </p>
            </div>
          </section>
        )}

      </main>

      <HowItWorks
        feature="simulation"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />

    </div>
  );
}
