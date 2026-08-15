import { useState } from "react";

import {
  ArrowLeft,
  Filter,
  RefreshCw,
  AlertTriangle,
} from "lucide-react";

import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { AlertSummaryItem, Alert } from "../types";

import AlertSummaryCard from "../components/alerts/AlertSummaryCard";
import AlertCard from "../components/alerts/AlertCard";
import AlertDetails from "../components/alerts/AlertDetails";

import HelpButton from "../components/common/HelpButton";
import HowItWorks from "../components/common/HowItWorks";
import logoImg from "../assets/logo_varithon.png";

const alertSummary: AlertSummaryItem[] = [
  { id: "1", severity: "critical", labelKey: "alerts.critical", value: "1", title: "", trend: "", status: "", count: 0 },
  { id: "2", severity: "high", labelKey: "alerts.high", value: "1", title: "", trend: "", status: "", count: 0 },
  { id: "3", severity: "medium", labelKey: "alerts.medium", value: "0", title: "", trend: "", status: "", count: 0 },
  { id: "4", severity: "resolved", labelKey: "alerts.resolved", value: "2", title: "", trend: "", status: "", count: 0 }
];

export default function Alerts() {

  const { t } = useTranslation();
  const navigate = useNavigate();

  const [severity, setSeverity] = useState("all");
  const [type, setType] = useState("all");

  const [selectedAlert, setSelectedAlert] =
    useState<Alert | null>(null);

  const [helpOpen, setHelpOpen] =
    useState(false);

  const mockAlerts: Alert[] = [
    {
      id: "A001",
      status: "active",
      zone: "Zone 6",
      riskScore: 85,
      predictedTime: "10m",
      recommendationKey: "alerts.data.crowdRecommendation",
      location: "Zone 6 Main Corridor",
      descriptionKey: "alerts.data.criticalCrowdDescription",
      severity: "critical",
      type: "crowd",
      message: "Critical Crowd Congestion",
      time: "10m ago",
      titleKey: "alerts.data.criticalCrowd",
      messageKey: "alerts.data.criticalCrowd",
      details: ""
    },
    {
      id: "A002",
      status: "active",
      zone: "Zone 2",
      riskScore: 65,
      predictedTime: "45m",
      recommendationKey: "alerts.data.resourceRecommendation",
      location: "Zone 2 North",
      descriptionKey: "alerts.data.resourceShortageDescription",
      severity: "medium",
      type: "resource",
      message: "Resource Availability Warning",
      time: "45m ago",
      titleKey: "alerts.data.resourceShortage",
      messageKey: "alerts.data.resourceShortage",
      details: ""
    }
  ];

  const filteredAlerts: Alert[] = mockAlerts.filter(alert => {
    if (severity !== "all" && alert.severity !== severity) return false;
    if (type !== "all" && alert.type !== type) return false;
    return true;
  });

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
                {t("alerts.title")}
              </h1>

              <p className="text-xs text-[#8B735D] hidden xs:block">
                {t("alerts.subtitle")}
              </p>
            </div>
          </div>

        </div>

        <HelpButton
          onClick={() => setHelpOpen(true)}
        />

      </header>

      <main className="mx-auto max-w-[1500px] p-4 md:p-8">

        {/* Introduction */}

        <section className="mb-7">

          <p className="text-sm font-medium text-[#E86F00]">
            {t("alerts.commandCenter")}
          </p>

          <div className="mt-1 flex flex-col justify-between gap-4 md:flex-row md:items-end">

            <div>

              <h2 className="text-2xl font-bold text-[#3D2918] md:text-3xl">
                {t("alerts.overviewTitle")}
              </h2>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-[#8B735D]">
                {t("alerts.overviewDescription")}
              </p>

            </div>

            <button
              type="button"
              className="flex items-center justify-center gap-2 rounded-xl border border-[#EDE2D0] bg-white px-4 py-2.5 text-sm font-semibold text-[#6B421F] hover:bg-[#F8F1E5] cursor-pointer"
            >
              <RefreshCw size={16} className="text-[#E86F00]" />
              {t("alerts.refresh")}
            </button>

          </div>

        </section>

        {/* Summary */}

        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

          {alertSummary.map((item: AlertSummaryItem) => (
            <AlertSummaryCard
              key={item.id}
              item={item}
            />
          ))}

        </section>

        {/* Filters */}

        <section className="mt-6 rounded-2xl border border-[#EDE2D0] bg-white p-4">

          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

            <div className="flex items-center gap-2">

              <Filter
                size={18}
                className="text-[#E86F00]"
              />

              <span className="text-sm font-bold text-[#3D2918]">
                {t("alerts.filters")}
              </span>

            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">

              {/* Severity */}

              <select
                value={severity}
                onChange={(e) =>
                  setSeverity(e.target.value)
                }
                className="rounded-xl border border-[#EDE2D0] bg-[#FFFDF8] px-4 py-2.5 text-sm text-[#6B421F] outline-none focus:border-[#F28C00] cursor-pointer"
              >
                <option value="all">
                  {t("alerts.allSeverity")}
                </option>

                <option value="critical">
                  {t("alerts.severity.critical")}
                </option>

                <option value="high">
                  {t("alerts.severity.high")}
                </option>

                <option value="medium">
                  {t("alerts.severity.medium")}
                </option>

                <option value="resolved">
                  {t("alerts.severity.resolved")}
                </option>
              </select>

              {/* Type */}

              <select
                value={type}
                onChange={(e) =>
                  setType(e.target.value)
                }
                className="rounded-xl border border-[#EDE2D0] bg-[#FFFDF8] px-4 py-2.5 text-sm text-[#6B421F] outline-none focus:border-[#F28C00] cursor-pointer"
              >
                <option value="all">
                  {t("alerts.allTypes")}
                </option>

                <option value="crowd">
                  {t("alerts.types.crowd")}
                </option>

                <option value="heat">
                  {t("alerts.types.heat")}
                </option>

                <option value="resource">
                  {t("alerts.types.resource")}
                </option>

                <option value="weather">
                  {t("alerts.types.weather")}
                </option>

                <option value="medical">
                  {t("alerts.types.medical")}
                </option>

              </select>

            </div>

          </div>

        </section>

        {/* Alerts */}

        <section className="mt-6 space-y-4">

          {filteredAlerts.length > 0 ? (

            filteredAlerts.map((alert: Alert) => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onView={setSelectedAlert}
              />
            ))

          ) : (

            <div className="flex h-[300px] flex-col items-center justify-center rounded-2xl border border-dashed border-[#DECFBE] bg-[#FAF5EE] text-center p-10">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-[#F28C00]/10 text-[#D96F00] mb-4">
                <AlertTriangle size={28} />
              </div>
              <p className="font-bold text-[#3D2918] text-lg mb-2">
                No Operational Alerts Available
              </p>
              <p className="text-sm text-[#8B735D] max-w-sm leading-relaxed">
                Integration with the backend API is pending. Alerts will appear here when the alerting engine is connected.
              </p>
            </div>

          )}

        </section>

      </main>

      {/* Details modal */}

      {selectedAlert !== null && (
        <AlertDetails
          alert={selectedAlert as import("../types").Alert}
          onClose={() => setSelectedAlert(null)}
        />
      )}

      {/* How it works */}

      <HowItWorks
        feature="alerts"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />

    </div>
  );
}
