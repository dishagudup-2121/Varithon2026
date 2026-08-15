import {
  CheckCircle,
  Info,
} from "lucide-react";

import { useTranslation } from "react-i18next";

import { SimulationResult } from "../../types";

export default function SimulationRecommendation({
  result,
  onApprove,
  onReject,
}: {
  result: SimulationResult;
  onApprove: () => void;
  onReject: () => void;
}) {
  const { t } = useTranslation();

  return (
    <div className="rounded-2xl border border-[#E8D3B5] bg-[#FFF8EC] p-5">

      <div className="flex gap-3">

        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#F28C00] text-white">
          <CheckCircle size={20} />
        </div>

        <div>
          <h2 className="font-bold text-[#3D2918]">
            {t("simulation.recommendationTitle")}
          </h2>

          <p className="mt-1 text-sm leading-6 text-[#6B421F]">
            {t(result.recommendationKey)}
          </p>
        </div>

      </div>

      <div className="mt-4 flex gap-2 rounded-xl bg-white/70 p-3">

        <Info
          size={16}
          className="mt-0.5 shrink-0 text-[#D96F00]"
        />

        <p className="text-xs leading-5 text-[#8B735D]">
          {t("simulation.humanApprovalNote")}
        </p>

      </div>

      <div className="mt-5 flex flex-col gap-2 sm:flex-row">

        <button
          onClick={onApprove}
          className="flex-1 rounded-xl bg-[#F28C00] py-3 text-sm font-semibold text-white transition hover:bg-[#D96F00]"
        >
          {t("simulation.approve")}
        </button>

        <button
          onClick={onReject}
          className="flex-1 rounded-xl border border-[#E2D5C4] bg-white py-3 text-sm font-semibold text-[#6B421F] transition hover:bg-[#F8F1E5]"
        >
          {t("simulation.reject")}
        </button>

      </div>

    </div>
  );
}
