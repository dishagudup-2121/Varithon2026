import {
  Ambulance,
  Users,
  Droplets,
  
  ShieldAlert,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { ResourceSummary } from "../../types";

const icons: Record<string, React.ElementType> = {
  ambulance: Ambulance,
  volunteers: Users,
  water: Droplets,
  medical: ShieldAlert,
};

export default function ResourceSummaryCard({
  resource,
}: {
  resource: ResourceSummary;
}) {
  const { t } = useTranslation();

  const Icon = icons[resource.type as keyof typeof icons] || Users;

  const isUnavailable = resource.available === 'unavailable' || resource.total === 'unavailable';
  
  const percentage = isUnavailable ? 0 : Math.round(
    (Number(resource.available) / Number(resource.total)) * 100
  );

  return (
    <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5">

      <div className="flex items-start justify-between">

        <div>
          <p className="text-sm text-[#8B735D]">
            {t(resource.titleKey)}
          </p>

          {isUnavailable ? (
            <div className="mt-2 flex items-baseline gap-1">
              <span className="text-sm font-semibold text-[#B3A191] italic">
                Data Unavailable
              </span>
            </div>
          ) : (
            <div className="mt-2 flex items-baseline gap-1">
              <span className="text-2xl font-bold text-[#3D2918]">
                {resource.available}
              </span>

              <span className="text-sm text-[#9B836B]">
                / {resource.total}
              </span>
            </div>
          )}
        </div>

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#D96F00]">
          <Icon size={20} />
        </div>

      </div>

      <div className="mt-4">

        <div className="mb-1 flex justify-between text-xs">
          <span className="text-[#8B735D]">
            {t("resources.available")}
          </span>

          <span className="font-semibold text-[#6B421F]">
            {isUnavailable ? '--' : `${percentage}%`}
          </span>
        </div>

        <div className="h-2 overflow-hidden rounded-full bg-[#F1E8DB]">
          {!isUnavailable && (
            <div
              className="h-full rounded-full bg-[#F28C00]"
              style={{ width: `${percentage}%` }}
            />
          )}
        </div>

      </div>

    </div>
  );
}
