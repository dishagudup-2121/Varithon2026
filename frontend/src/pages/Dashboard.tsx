import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { ArrowRight } from "lucide-react";

import KPICard from "../components/dashboard/KpiCard";
import DigitalTwinPreview from "../components/dashboard/DigitalTwinPreview";
import AlertsPanel from "../components/dashboard/AlertsPanel";
import RecommendationCard from "../components/dashboard/RecommendationCard";
import DecisionLoop from "../components/dashboard/DecisionLoop";
import HelpButton from "../components/common/HelpButton";
import HowItWorks from "../components/common/HowItWorks";
import { useSimulationStream } from "../hooks/useSimulationStream";

export default function Dashboard() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [helpOpen, setHelpOpen] = useState(false);
  const { simulationState } = useSimulationStream();

  const user = JSON.parse(
    localStorage.getItem("varisetuUser") || "{}"
  );

  const getKpiClickHandler = (statId: string) => {
    switch (statId) {
      case "ambulance":
      case "volunteers":
      case "medical":
        return () => navigate("/dashboard/resources");
      case "risk":
        return () => navigate("/dashboard/alerts");
      case "pilgrims":
        return () => navigate("/dashboard/digital-twin");
      default:
        return undefined;
    }
  };

  const totalPilgrims = simulationState?.crowd?.summary?.total_pilgrims ?? 'unavailable';
  
  const dashboardStats = [
    {
      id: "pilgrims",
      titleKey: "dashboard.stats.pilgrims",
      value: totalPilgrims,
      subtitleKey: "dashboard.stats.pilgrimsSubtitle",
      icon: "users"
    },
    {
      id: "risk",
      titleKey: "dashboard.stats.riskZones",
      value: "2",
      subtitleKey: "dashboard.stats.riskZonesSubtitle",
      icon: "alert"
    },
    {
      id: "medical",
      titleKey: "dashboard.stats.medical",
      value: "14",
      subtitleKey: "dashboard.stats.medicalSubtitle",
      icon: "heart"
    },
    {
      id: "ambulance",
      titleKey: "dashboard.stats.ambulances",
      value: "45",
      subtitleKey: "dashboard.stats.ambulancesSubtitle",
      icon: "ambulance"
    },
    {
      id: "volunteers",
      titleKey: "dashboard.stats.volunteers",
      value: "320",
      subtitleKey: "dashboard.stats.volunteersSubtitle",
      icon: "users"
    }
  ];

  return (
    <>
      <main className="mx-auto max-w-[1600px] p-0">
        {/* Welcome */}
        <section className="mb-7">
            <div className="flex flex-col justify-between gap-3 md:flex-row md:items-end">
              <div>
                <p className="mb-1 text-sm font-medium text-[#D96F00]">
                  {t("dashboard.goodToSeeYou")}
                </p>

                <h2 className="text-2xl font-bold tracking-tight text-[#3D2918] md:text-3xl">
                  {t("dashboard.welcome")},{" "}
                  {user.name || "User"}
                </h2>

                <p className="mt-2 max-w-2xl text-sm text-[#8B735D]">
                  {t("dashboard.overview")}
                </p>
              </div>

              <div className="flex items-center gap-3 self-start">
                <div className="flex items-center gap-2 rounded-full border border-[#E2D5C4] bg-white px-3 py-2 text-xs font-medium text-[#6B421F]">
                  <span className="h-2 w-2 rounded-full bg-green-500" />
                  {t("dashboard.systemOperational")}
                </div>

                <div className="rounded-xl border border-[#E2D5C4] bg-white p-1">
                  <HelpButton onClick={() => setHelpOpen(true)} />
                </div>
              </div>
            </div>
          </section>

          {/* KPI */}
          <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {dashboardStats.map((stat: import("../types").DashboardStat) => (
              <KPICard
                key={stat.id}
                title={t(stat.titleKey)}
                value={stat.value}
                subtitle={t(stat.subtitleKey)}
                icon={stat.icon}
                onClick={getKpiClickHandler(stat.id) || undefined}
              />
            ))}
          </section>

          {/* Digital Twin + Alerts */}
          <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-[1.6fr_1fr]">
            <DigitalTwinPreview />
            <AlertsPanel />
          </section>

          {/* What-If Analysis Action Card */}
          <section className="mt-6">
            <button
              onClick={() => navigate("/dashboard/simulation")}
              className="group w-full rounded-2xl border border-[#EDE2D0] bg-white p-5 text-left transition hover:border-[#F28C00] hover:bg-[#FFF8EC] cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold text-[#D96F00]">
                    {t("dashboardActions.whatIfTitle")}
                  </p>

                  <h3 className="mt-1 text-lg font-bold text-[#3D2918]">
                    {t("dashboardActions.whatIfHeading")}
                  </h3>

                  <p className="mt-2 text-sm text-[#8B735D]">
                    {t("dashboardActions.whatIfDescription")}
                  </p>
                </div>

                <div className="rounded-xl bg-[#F8E7CF] p-3 text-[#D96F00] transition group-hover:bg-[#F28C00] group-hover:text-white">
                  <ArrowRight size={20} />
                </div>
              </div>
            </button>
          </section>

          {/* Recommendation */}
          <section className="mt-6">
            <RecommendationCard />
          </section>

          {/* Decision Loop */}
          <section className="mt-6">
            <DecisionLoop />
          </section>
      </main>

      <HowItWorks
        feature="dashboard"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />
    </>
  );
}
