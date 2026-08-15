import { useState } from "react";
import { AlertTriangle, ArrowRight } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import HelpButton from "../common/HelpButton";
import HowItWorks from "../common/HowItWorks";



export default function AlertsPanel() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [helpOpen, setHelpOpen] = useState(false);

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
              2
            </span>
            <HelpButton onClick={() => setHelpOpen(true)} />
          </div>
        </div>

        <div className="flex h-[280px] flex-col gap-3 overflow-y-auto pr-1">
          {/* Active Alert 1 */}
          <div className="rounded-xl border border-red-100 bg-red-50/50 p-4">
            <div className="flex items-start gap-3">
              <div className="rounded-lg bg-red-100 p-2 text-red-600">
                <AlertTriangle size={20} />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-red-600 uppercase tracking-wider">{t("alerts.severity.critical")}</span>
                  <span className="text-[10px] font-medium text-slate-500">10m ago</span>
                </div>
                <h4 className="mt-1 font-bold text-slate-800 text-sm">{t("alerts.data.criticalCrowd")}</h4>
                <p className="mt-1 text-xs text-slate-600 line-clamp-2">
                  {t("alerts.data.criticalCrowdDescription")}
                </p>
                <div className="mt-3 flex gap-2">
                  <button onClick={() => navigate("/dashboard/alerts")} className="rounded-lg bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-sm border border-slate-200 hover:bg-slate-50">{t("alerts.viewDetails")}</button>
                </div>
              </div>
            </div>
          </div>
          {/* Active Alert 2 */}
          <div className="rounded-xl border border-amber-100 bg-amber-50/50 p-4">
            <div className="flex items-start gap-3">
              <div className="rounded-lg bg-amber-100 p-2 text-amber-600">
                <AlertTriangle size={20} />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-amber-600 uppercase tracking-wider">{t("alerts.severity.medium")}</span>
                  <span className="text-[10px] font-medium text-slate-500">45m ago</span>
                </div>
                <h4 className="mt-1 font-bold text-slate-800 text-sm">{t("alerts.data.resourceShortage")}</h4>
                <p className="mt-1 text-xs text-slate-600 line-clamp-2">
                  {t("alerts.data.resourceShortageDescription")}
                </p>
              </div>
            </div>
          </div>
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
