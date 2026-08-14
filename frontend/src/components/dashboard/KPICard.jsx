import {
  Users,
  AlertTriangle,
  HeartPulse,
  Ambulance,
} from "lucide-react";

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
}) {
  const Icon = icons[icon] || Users;

  return (
    <div
      onClick={onClick}
      className={`rounded-2xl border border-[#EDE2D0] bg-white p-5 transition hover:-translate-y-0.5 hover:shadow-md ${
        onClick ? "cursor-pointer hover:border-[#F28C00]" : ""
      }`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-[#8B735D]">{title}</p>

          <p className="mt-2 text-2xl font-bold text-[#3D2918]">
            {value}
          </p>

          <p className="mt-1 text-xs text-[#9B836B]">
            {subtitle}
          </p>
        </div>

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#D96F00]">
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
}
