import { useState } from "react";
import { MapPin, Ambulance, Users } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import HelpButton from "../common/HelpButton";
import HowItWorks from "../common/HowItWorks";

export default function DigitalTwinPreview() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [helpOpen, setHelpOpen] = useState(false);

  return (
    <>
      <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5">
        <div className="mb-4 flex items-start justify-between">
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

        <div className="relative h-[320px] overflow-hidden rounded-xl bg-[#F8F1E5]">
          {/* Abstract route lines */}
          <div className="absolute left-[15%] top-[55%] h-[2px] w-[65%] rotate-[-12deg] bg-[#D6B892]" />

          <div className="absolute left-[28%] top-[30%] h-[2px] w-[45%] rotate-[25deg] bg-[#D6B892]" />

          <div className="absolute left-[45%] top-[40%] h-[2px] w-[35%] rotate-[-30deg] bg-[#D6B892]" />

          {/* Risk zone */}
          <div className="absolute left-[64%] top-[30%] flex flex-col items-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#D96F00]/20">
              <MapPin className="text-[#D96F00]" size={27} />
            </div>

            <span className="mt-1 rounded-md bg-white px-2 py-1 text-xs font-semibold text-[#6B421F] shadow-sm">
              Zone 6
            </span>
          </div>

          {/* People */}
          <div className="absolute left-[32%] top-[62%] flex h-10 w-10 items-center justify-center rounded-full bg-white shadow">
            <Users size={19} className="text-[#6B421F]" />
          </div>

          {/* Ambulance */}
          <div className="absolute left-[22%] top-[38%] flex h-10 w-10 items-center justify-center rounded-full bg-white shadow">
            <Ambulance size={19} className="text-[#D96F00]" />
          </div>

          <div className="absolute bottom-3 left-3 rounded-lg bg-white/90 px-3 py-2 text-xs text-[#6B421F] shadow-sm">
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
