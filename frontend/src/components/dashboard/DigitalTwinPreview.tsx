import { useState } from "react";

import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import HelpButton from "../common/HelpButton";
import HowItWorks from "../common/HowItWorks";

import DigitalTwinMap from "../digital-twin/DigitalTwinMap";

export default function DigitalTwinPreview() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [helpOpen, setHelpOpen] = useState(false);

  return (
    <>
      <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5 flex flex-col">
        <div className="mb-4 flex items-start justify-between shrink-0">
          <div>
            <h2 className="font-bold text-[#3D2918]">
              {t("dashboard.digitalTwin.title")}
            </h2>

            <p className="text-sm text-[#8B735D]">
              {t("dashboard.digitalTwin.subtitle")}
            </p>
          </div>

          <HelpButton onClick={() => setHelpOpen(true)} />
        </div>

        <div className="relative flex-1 min-h-[300px] overflow-hidden rounded-xl bg-[#F8F1E5]">
          <DigitalTwinMap previewMode={true} />

          <div className="absolute bottom-3 left-3 z-[1000] rounded-lg bg-white/95 px-3 py-2 text-xs font-semibold text-[#6B421F] shadow-sm backdrop-blur">
            {t("dashboard.digitalTwin.preview")}
          </div>
        </div>

        <button
          onClick={() => navigate("/dashboard/digital-twin")}
          className="mt-4 w-full rounded-xl bg-[#F28C00] py-3 text-sm font-semibold text-white transition hover:bg-[#D96F00]"
        >
          {t("dashboard.digitalTwin.open")}
        </button>
      </div>

      <HowItWorks
        feature="digitalTwin"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />
    </>
  );
}
