import {
  AlertTriangle,
  Flame,
  Activity,
  CheckCircle,
} from "lucide-react";

import { useTranslation } from "react-i18next";

const icons = {
  critical: AlertTriangle,
  high: Flame,
  medium: Activity,
  resolved: CheckCircle,
};

export default function AlertSummaryCard({
  item,
}) {
  const { t } = useTranslation();

  const Icon = icons[item.id] || Activity;

  const styles = {
    critical: "bg-red-50 text-red-600",
    high: "bg-orange-50 text-[#D96F00]",
    medium: "bg-[#FFF4DF] text-[#C97900]",
    resolved: "bg-green-50 text-green-600",
  };

  return (
    <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5">

      <div className="flex items-start justify-between">

        <div>
          <p className="text-sm text-[#8B735D]">
            {t(item.labelKey)}
          </p>

          <p className="mt-2 text-2xl font-bold text-[#3D2918]">
            {item.value}
          </p>
        </div>

        <div
          className={`flex h-10 w-10 items-center justify-center rounded-xl ${styles[item.id]}`}
        >
          <Icon size={20} />
        </div>

      </div>

    </div>
  );
}
