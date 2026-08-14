import { useState } from "react";
import { AlertTriangle, Thermometer, Ambulance, ArrowRight } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import HelpButton from "../common/HelpButton";
import HowItWorks from "../common/HowItWorks";

const alertIcons = {
  high: AlertTriangle,
  medium: Thermometer,
  resource: Ambulance,
};

export default function AlertsPanel({ alerts }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [helpOpen, setHelpOpen] = useState(false);

  const handleAlertClick = (alert) => {
    if (alert.type === "resource") {
      navigate("/dashboard/resources");
    } else {
      navigate("/dashboard/alerts");
    }
  };

  return (
    <>
      <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5">
        <div className="mb-5 flex items-center justify-between">
          <div>
            <h2 className="font-bold text-[#3D2918]">
              {t("dashboard.activeAlerts")}
            </h2>

            <p className="text-sm text-[#8B735D]">
              {t("dashboard.alertsSubtitle")}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="rounded-full bg-[#F8E7CF] px-2.5 py-1 text-xs font-semibold text-[#D96F00]">
              {alerts.length}
            </span>
            <HelpButton onClick={() => setHelpOpen(true)} />
          </div>
        </div>

        <div className="space-y-3">
          {alerts.map((alert) => {
            const Icon = alertIcons[alert.type] || AlertTriangle;

            const iconStyle =
              alert.type === "high"
                ? "bg-red-50 text-red-600"
                : alert.type === "medium"
                ? "bg-orange-50 text-orange-600"
                : "bg-[#F8E7CF] text-[#D96F00]";

            return (
              <button
                key={alert.id}
                onClick={() => handleAlertClick(alert)}
                className="w-full text-left rounded-xl border border-[#EDE2D0] p-3 transition hover:border-[#D96F00] hover:bg-[#FFFDF8] cursor-pointer"
              >
                <div className="flex gap-3">
                  <div
                    className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${iconStyle}`}
                  >
                    <Icon size={17} />
                  </div>

                  <div className="min-w-0">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-sm font-semibold text-[#3D2918]">
                        {t(alert.titleKey)}
                      </p>

                      <span className="whitespace-nowrap text-[10px] text-[#9B836B]">
                        {alert.time}
                      </span>
                    </div>

                    <p className="mt-0.5 text-xs font-medium text-[#6B421F]">
                      {alert.location}
                    </p>

                    <p className="mt-1 text-xs leading-relaxed text-[#8B735D]">
                      {t(alert.descriptionKey)}
                    </p>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        <button
          onClick={() => navigate("/dashboard/alerts")}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-[#EDE2D0] py-2.5 text-sm font-semibold text-[#6B421F] transition hover:bg-[#F8F1E5]"
        >
          {t("dashboard.viewAllAlerts")}
          <ArrowRight size={16} />
        </button>
      </div>

      <HowItWorks
        feature="alerts"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />
    </>
  );
}
