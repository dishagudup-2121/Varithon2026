import {
  Ambulance,
  Users,
  Droplets,
  Info,
  Play,
  CheckCircle,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

const icons = {
  ambulance: Ambulance,
  users: Users,
  water: Droplets,
};

export default function RecommendationCard({ recommendations }) {
  const { t } = useTranslation();
  const navigate = useNavigate();

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

      <div className="mt-4 rounded-xl bg-[#F8F1E5] p-4">
        <div className="flex gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#F28C00] text-white">
            <CheckCircle size={19} />
          </div>

          <p className="text-sm leading-relaxed text-[#6B421F]">
            {t("dashboard.recommendationText")}
          </p>
        </div>
      </div>

      <div className="mt-4 space-y-2">
        {recommendations.map((item) => {
          const Icon = icons[item.icon] || Users;

          return (
            <button
              key={item.resource}
              onClick={() => navigate("/dashboard/resources")}
              className="w-full flex items-center justify-between rounded-xl border border-[#EDE2D0] p-3 text-left transition hover:border-[#D96F00] hover:bg-[#FFFDF8] cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#F8E7CF] text-[#D96F00]">
                  <Icon size={18} />
                </div>

                <div>
                  <p className="text-sm font-semibold text-[#3D2918]">
                    {item.resource}
                  </p>

                  <p className="text-xs text-[#8B735D]">
                    {t(item.textKey)}
                  </p>
                </div>
              </div>

              <span className="text-xs font-semibold text-[#D96F00]">
                {item.zone}
              </span>
            </button>
          );
        })}
      </div>

      <div className="mt-5 flex flex-col gap-2 sm:flex-row">
        <button
          onClick={() => navigate("/dashboard/simulation")}
          className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-[#F28C00] py-3 text-sm font-semibold text-white transition hover:bg-[#D96F00]"
        >
          <Play size={16} />
          {t("dashboard.simulateResponse")}
        </button>

        <button
          onClick={() => navigate("/dashboard/assistant")}
          className="flex-1 rounded-xl border border-[#EDE2D0] py-3 text-sm font-semibold text-[#6B421F] transition hover:bg-[#F8F1E5]"
        >
          {t("dashboard.reviewRecommendation")}
        </button>
      </div>
    </div>
  );
}
