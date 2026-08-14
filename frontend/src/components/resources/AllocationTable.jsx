import {
  Ambulance,
  Users,
  Droplets,
  HeartPulse,
  ArrowRight,
  Clock,
} from "lucide-react";

import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

const icons = {
  ambulance: Ambulance,
  volunteers: Users,
  water: Droplets,
  medical: HeartPulse,
};

export default function AllocationTable({
  allocations,
  onAssign,
}) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const handleTestSimulation = (item) => {
    const resource = encodeURIComponent(
      item.resource || item.name || "Resource"
    );
    const target = encodeURIComponent(
      item.to || item.destination || "High Risk Zone"
    );
    navigate(
      `/dashboard/simulation?resource=${resource}&target=${target}`
    );
  };

  return (
    <div className="rounded-2xl border border-[#EDE2D0] bg-white">

      <div className="border-b border-[#EDE2D0] p-5">

        <h2 className="font-bold text-[#3D2918]">
          {t("resources.recommendedAllocation")}
        </h2>

        <p className="mt-1 text-sm text-[#8B735D]">
          {t("resources.allocationSubtitle")}
        </p>

      </div>

      {/* Desktop table */}
      <div className="hidden overflow-x-auto md:block">

        <table className="w-full">

          <thead>
            <tr className="border-b border-[#EDE2D0] bg-[#FFFDF8] text-left text-xs uppercase tracking-wide text-[#9B836B]">
              <th className="px-5 py-4">
                {t("resources.resource")}
              </th>

              <th className="px-5 py-4">
                {t("resources.from")}
              </th>

              <th className="px-5 py-4">
                {t("resources.destination")}
              </th>

              <th className="px-5 py-4">
                {t("resources.eta")}
              </th>

              <th className="px-5 py-4">
                {t("resources.action")}
              </th>
            </tr>
          </thead>

          <tbody>

            {allocations.map((item) => {

              const Icon = icons[item.type] || Users;

              return (
                <tr
                  key={item.id}
                  className="border-b border-[#F1E8DB] last:border-0"
                >

                  <td className="px-5 py-4">

                    <div className="flex items-center gap-3">

                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#F8E7CF] text-[#D96F00]">
                        <Icon size={18} />
                      </div>

                      <div>
                        <p className="text-sm font-semibold text-[#3D2918]">
                          {item.resource}
                        </p>

                        <p className="text-xs text-[#9B836B]">
                          {t(`resources.types.${item.type}`)}
                        </p>
                      </div>

                    </div>

                  </td>

                  <td className="px-5 py-4 text-sm text-[#6B421F]">
                    {item.from}
                  </td>

                  <td className="px-5 py-4">

                    <div className="flex items-center gap-2 text-sm">

                      <ArrowRight
                        size={15}
                        className="text-[#D96F00]"
                      />

                      <span className="font-semibold text-[#3D2918]">
                        {item.to}
                      </span>

                    </div>

                  </td>

                  <td className="px-5 py-4">

                    <div className="flex items-center gap-1 text-sm text-[#6B421F]">
                      <Clock size={14} />
                      {item.eta}
                    </div>

                  </td>

                  <td className="px-5 py-4">

                    <div className="flex flex-wrap gap-2">

                      <button
                        type="button"
                        onClick={() => onAssign(item)}
                        className="rounded-lg border border-[#D96F00] px-3 py-2 text-xs font-semibold text-[#D96F00] transition hover:bg-[#F28C00] hover:text-white cursor-pointer"
                      >
                        {t("resources.assign")}
                      </button>

                      <button
                        type="button"
                        onClick={() => handleTestSimulation(item)}
                        className="rounded-lg bg-[#FFF4DF] px-3 py-2 text-xs font-semibold text-[#D96F00] transition hover:bg-[#F8E7CF] cursor-pointer"
                      >
                        {t("resources.testSimulation")}
                      </button>

                    </div>

                  </td>

                </tr>
              );
            })}

          </tbody>

        </table>

      </div>

      {/* Mobile cards */}
      <div className="space-y-3 p-4 md:hidden">

        {allocations.map((item) => {

          const Icon = icons[item.type] || Users;

          return (
            <div
              key={item.id}
              className="rounded-xl border border-[#EDE2D0] p-4"
            >

              <div className="flex items-center gap-3">

                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#F8E7CF] text-[#D96F00]">
                  <Icon size={18} />
                </div>

                <div>
                  <p className="text-sm font-semibold text-[#3D2918]">
                    {item.resource}
                  </p>

                  <p className="text-xs text-[#9B836B]">
                    {t(`resources.types.${item.type}`)}
                  </p>
                </div>

              </div>

              <div className="mt-3 flex items-center justify-between text-xs">

                <span className="text-[#8B735D]">
                  {item.from}
                </span>

                <ArrowRight
                  size={14}
                  className="text-[#D96F00]"
                />

                <span className="font-semibold text-[#3D2918]">
                  {item.to}
                </span>

              </div>

              <div className="mt-3 flex items-center justify-between">

                <span className="text-xs text-[#8B735D]">
                  ETA: {item.eta}
                </span>

                <div className="flex gap-2">

                  <button
                    type="button"
                    onClick={() => onAssign(item)}
                    className="rounded-lg bg-[#F28C00] px-3 py-2 text-xs font-semibold text-white cursor-pointer"
                  >
                    {t("resources.assign")}
                  </button>

                  <button
                    type="button"
                    onClick={() => handleTestSimulation(item)}
                    className="rounded-lg border border-[#D96F00] px-3 py-2 text-xs font-semibold text-[#D96F00] cursor-pointer"
                  >
                    {t("resources.testSimulation")}
                  </button>

                </div>

              </div>

            </div>
          );
        })}

      </div>

    </div>
  );
}
