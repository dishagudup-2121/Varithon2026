import {
  AlertTriangle,
  Thermometer,
  Users,
  Ambulance,
  CloudRain,
  HeartPulse,
  Clock,
  ArrowRight,
} from "lucide-react";

import { useTranslation } from "react-i18next";

const icons = {
  crowd: Users,
  heat: Thermometer,
  resource: Ambulance,
  weather: CloudRain,
  medical: HeartPulse,
};

export default function AlertCard({
  alert,
  onView,
}) {
  const { t } = useTranslation();

  const Icon = icons[alert.type] || AlertTriangle;

  const severityStyles = {
    critical: {
      badge: "bg-red-50 text-red-700",
      icon: "bg-red-50 text-red-600",
      border: "border-l-red-500",
    },

    high: {
      badge: "bg-orange-50 text-[#C45E00]",
      icon: "bg-orange-50 text-[#D96F00]",
      border: "border-l-[#D96F00]",
    },

    medium: {
      badge: "bg-[#FFF4DF] text-[#A96600]",
      icon: "bg-[#FFF4DF] text-[#C97900]",
      border: "border-l-[#F2A900]",
    },

    resolved: {
      badge: "bg-green-50 text-green-700",
      icon: "bg-green-50 text-green-600",
      border: "border-l-green-500",
    },
  };

  const style =
    severityStyles[alert.severity] ||
    severityStyles.medium;

  return (
    <div
      className={`rounded-2xl border border-[#EDE2D0] border-l-4 ${style.border} bg-white p-5`}
    >

      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">

        {/* Main information */}

        <div className="flex gap-4">

          <div
            className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${style.icon}`}
          >
            <Icon size={21} />
          </div>

          <div>

            <div className="flex flex-wrap items-center gap-2">

              <h3 className="font-bold text-[#3D2918]">
                {t(alert.titleKey)}
              </h3>

              <span
                className={`rounded-full px-2.5 py-1 text-[10px] font-bold uppercase ${style.badge}`}
              >
                {t(`alerts.severity.${alert.severity}`)}
              </span>

            </div>

            <p className="mt-1 text-sm font-medium text-[#6B421F]">
              {alert.zone}
            </p>

            <p className="mt-2 max-w-xl text-sm leading-6 text-[#8B735D]">
              {t(alert.descriptionKey)}
            </p>

          </div>

        </div>

        {/* Time */}

        <div className="flex shrink-0 items-center gap-1 text-xs text-[#9B836B]">
          <Clock size={14} />
          {alert.time}
        </div>

      </div>

      {/* Prediction information */}

      <div className="mt-5 grid grid-cols-1 gap-3 border-t border-[#F1E8DB] pt-4 sm:grid-cols-3">

        <div className="rounded-xl bg-[#FFFDF8] p-3">

          <p className="text-xs text-[#9B836B]">
            {t("alerts.riskScore")}
          </p>

          <p className="mt-1 text-lg font-bold text-[#3D2918]">
            {alert.riskScore}%
          </p>

        </div>

        <div className="rounded-xl bg-[#FFFDF8] p-3">

          <p className="text-xs text-[#9B836B]">
            {t("alerts.predictedIn")}
          </p>

          <p className="mt-1 text-lg font-bold text-[#3D2918]">
            {alert.predictedTime}
          </p>

        </div>

        <div className="rounded-xl bg-[#FFFDF8] p-3">

          <p className="text-xs text-[#9B836B]">
            {t("alerts.recommendedAction")}
          </p>

          <p className="mt-1 text-sm font-semibold text-[#3D2918]">
            {t(alert.recommendationKey)}
          </p>

        </div>

      </div>

      {/* Action */}

      <div className="mt-4 flex justify-end">

        <button
          onClick={() => onView(alert)}
          className="flex items-center gap-2 rounded-xl border border-[#EDE2D0] px-4 py-2.5 text-sm font-semibold text-[#6B421F] transition hover:bg-[#F8F1E5]"
        >
          {t("alerts.viewDetails")}

          <ArrowRight size={16} />

        </button>

      </div>

    </div>
  );
}
