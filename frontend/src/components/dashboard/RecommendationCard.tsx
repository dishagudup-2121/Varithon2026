import {
  Info,
  Play,
  CheckCircle,
} from "lucide-react";
import { useTranslation } from "react-i18next";

export default function RecommendationCard() {
  const { t } = useTranslation();

  return (
    <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-bold text-[#3D2918]">
            {t("dashboard.aiRecommendation")}
          </h2>

          <p className="mt-1 text-sm text-[#8B735D]">
            {t("dashboard.recommendationSubtitle")}
          </p>
        </div>

        <button
          className="text-[#9B836B] hover:text-[#D96F00]"
          title={t("dashboard.howItWorks")}
        >
          <Info size={18} />
        </button>
      </div>

      <div className="mt-4 rounded-xl border border-[#F28C00]/30 bg-[#FFF8EC] p-4 h-[200px] flex flex-col justify-center">
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#F28C00]/10 text-[#D96F00]">
            <CheckCircle size={20} />
          </div>
          <div>
            <h3 className="font-bold text-[#3D2918] text-sm">
              {t("dashboard.recommendations.volunteers")}
            </h3>
            <p className="mt-2 text-sm text-[#8B735D] leading-relaxed">
              {t("dashboard.recommendationText")}
            </p>
          </div>
        </div>
      </div>

      <div className="mt-5 flex flex-col gap-2 sm:flex-row">
        <button
          className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-[#F28C00] py-3 text-sm font-semibold text-white hover:bg-[#D96F00] transition"
        >
          <Play size={16} />
          {t("dashboard.simulateResponse")}
        </button>

        <button
          className="flex-1 rounded-xl border border-[#EDE2D0] bg-white py-3 text-sm font-semibold text-[#6B421F] hover:bg-[#F8F1E5] transition"
        >
          {t("dashboard.reviewRecommendation")}
        </button>
      </div>
    </div>
  );
}
