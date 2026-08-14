import {
  X,
  Info,
  CheckCircle2,
} from "lucide-react";

import { useTranslation } from "react-i18next";

import { howItWorksData } from "../../data/howItWorksData";

export default function HowItWorks({
  feature,
  open,
  onClose,
}) {
  const { t } = useTranslation();

  if (!open) return null;

  const content = howItWorksData[feature];

  if (!content) return null;

  const steps = t(content.stepsKey, {
    returnObjects: true,
  });

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/30 p-4 backdrop-blur-sm">

      {/* Overlay */}

      <button
        type="button"
        aria-label={t("howItWorks.close", { defaultValue: "Close" })}
        onClick={onClose}
        className="absolute inset-0 cursor-default"
      />

      {/* Modal */}

      <div className="relative z-10 w-full max-w-lg overflow-hidden rounded-3xl border border-[#EDE2D0] bg-[#FFFDF8] shadow-2xl">

        {/* Header */}

        <div className="flex items-start justify-between border-b border-[#EDE2D0] bg-white p-5">

          <div className="flex gap-3">

            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#D96F00]">
              <Info size={21} />
            </div>

            <div>

              <h2 className="font-bold text-[#3D2918]">
                {t(content.titleKey)}
              </h2>

              <p className="mt-1 text-sm leading-5 text-[#8B735D]">
                {t(content.descriptionKey)}
              </p>

            </div>

          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-[#8B735D] hover:bg-[#F8F1E5] cursor-pointer"
          >
            <X size={19} />
          </button>

        </div>

        {/* Steps */}

        <div className="p-5">

          <div className="space-y-3">

            {Array.isArray(steps) &&
              steps.map((step, index) => (
                <div
                  key={index}
                  className="flex gap-3 rounded-xl bg-white p-3 border border-[#EDE2D0]"
                >

                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#F28C00] text-xs font-bold text-white">
                    {index + 1}
                  </div>

                  <p className="pt-1 text-sm leading-5 text-[#5F4732]">
                    {step}
                  </p>

                </div>
              ))}

          </div>

          {/* Note */}

          <div className="mt-4 flex gap-2 rounded-xl border border-[#E8D3B5] bg-[#FFF8EC] p-4">

            <CheckCircle2
              size={17}
              className="mt-0.5 shrink-0 text-[#D96F00]"
            />

            <p className="text-xs leading-5 text-[#6B421F]">
              {t(content.noteKey)}
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}
