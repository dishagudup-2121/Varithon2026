import {
  Users,
  ShieldAlert,
  Clock,
  MapPin,
  TrendingDown,
  TrendingUp,
} from "lucide-react";

import { useTranslation } from "react-i18next";

import { SimulationResult } from "../../types";

export default function ComparisonCard({ result }: { result: SimulationResult }) {
  const { t } = useTranslation();

  const metrics = [
    {
      key: "crowd",
      label: t("simulation.metrics.crowd"),
      icon: Users,
      before: result.before.crowd.toLocaleString(),
      after: result.after.crowd.toLocaleString(),
      impact: result.impact.congestion,
      suffix: "%",
    },
    {
      key: "risk",
      label: t("simulation.metrics.risk"),
      icon: ShieldAlert,
      before: `${result.before.risk}%`,
      after: `${result.after.risk}%`,
      impact: result.impact.risk,
      suffix: "%",
    },
    {
      key: "eta",
      label: t("simulation.metrics.eta"),
      icon: Clock,
      before: `${result.before.eta} min`,
      after: `${result.after.eta} min`,
      impact: result.impact.eta,
      suffix: " min",
    },
    {
      key: "zones",
      label: t("simulation.metrics.affectedZones"),
      icon: MapPin,
      before: result.before.affectedZones,
      after: result.after.affectedZones,
      impact:
        Number(result.after.affectedZones) -
        Number(result.before.affectedZones),
      suffix: "",
    },
  ];

  return (
    <div className="rounded-2xl border border-[#EDE2D0] bg-white">

      <div className="border-b border-[#EDE2D0] p-5">
        <h2 className="font-bold text-[#3D2918]">
          {t("simulation.comparisonTitle")}
        </h2>

        <p className="mt-1 text-sm text-[#8B735D]">
          {t("simulation.comparisonSubtitle")}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 p-5 sm:grid-cols-2 xl:grid-cols-4">

        {metrics.map((metric) => {
          const Icon = metric.icon;

          const isImprovement =
            Number(metric.impact) < 0;

          return (
            <div
              key={metric.key}
              className="rounded-xl bg-[#FFFDF8] p-4"
            >
              <div className="flex items-center gap-2">
                <Icon
                  size={17}
                  className="text-[#D96F00]"
                />

                <span className="text-xs font-semibold text-[#8B735D]">
                  {metric.label}
                </span>
              </div>

              <div className="mt-4 flex items-end justify-between gap-3">

                <div>
                  <p className="text-[10px] uppercase text-[#9B836B]">
                    {t("simulation.before")}
                  </p>

                  <p className="text-lg font-bold text-[#3D2918]">
                    {metric.before}
                  </p>
                </div>

                <div className="text-[#9B836B]">
                  →
                </div>

                <div>
                  <p className="text-[10px] uppercase text-[#9B836B]">
                    {t("simulation.after")}
                  </p>

                  <p className="text-lg font-bold text-[#3D2918]">
                    {metric.after}
                  </p>
                </div>

              </div>

              <div
                className={`mt-3 flex items-center gap-1 text-xs font-semibold ${
                  isImprovement
                    ? "text-green-600"
                    : "text-[#D96F00]"
                }`}
              >
                {isImprovement ? (
                  <TrendingDown size={14} />
                ) : (
                  <TrendingUp size={14} />
                )}

                {Number(metric.impact) > 0
                  ? `+${metric.impact}`
                  : metric.impact}
                {metric.suffix}
              </div>
            </div>
          );
        })}

      </div>
    </div>
  );
}
