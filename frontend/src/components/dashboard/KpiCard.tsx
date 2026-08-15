import {
  Users,
  AlertTriangle,
  HeartPulse,
  Ambulance,
} from "lucide-react";
import { useTranslation } from "react-i18next";

const icons = {
  users: Users,
  alert: AlertTriangle,
  heart: HeartPulse,
  ambulance: Ambulance,
};

export default function KPICard({
  title,
  value,
  subtitle,
  icon,
  onClick,
}: {
  title: string;
  value: string | number | "unavailable";
  subtitle: string;
  icon: keyof typeof icons | string;
  onClick?: () => void;
}) {
  const { t } = useTranslation();
  const Icon = icons[icon as keyof typeof icons] || Users;
  const isUnavailable = value === "unavailable";

  return (
    <div
      onClick={onClick}
      className={`rounded-2xl border border-[#EDE2D0] bg-white px-5 py-5 transition hover:-translate-y-0.5 hover:shadow-md ${
        onClick ? "cursor-pointer hover:border-[#F28C00]" : ""
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-[#8B735D] leading-tight">
            {title}
          </p>

          {isUnavailable ? (
            <p className="mt-2.5 text-sm font-semibold text-[#B3A191] italic">
              {t("dashboard.stats.unavailable", { defaultValue: "Data Unavailable" })}
            </p>
          ) : (
            <p className="mt-2 text-2xl font-bold text-[#3D2918] tabular-nums">
              {typeof value === "number" ? value.toLocaleString() : value}
            </p>
          )}

          <p
            className={`mt-1.5 text-xs leading-tight ${
              isUnavailable ? "text-[#C4B7AC]" : "text-[#9B836B]"
            }`}
          >
            {subtitle}
          </p>
        </div>

        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#D96F00]">
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
}
