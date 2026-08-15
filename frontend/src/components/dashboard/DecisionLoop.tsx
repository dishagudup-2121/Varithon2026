import {
  Brain,
  Lightbulb,
  FlaskConical,
  UserCheck,
  Zap,
} from "lucide-react";
import { useTranslation } from "react-i18next";

const steps = [
  { key: "predict", icon: Brain },
  { key: "recommend", icon: Lightbulb },
  { key: "simulate", icon: FlaskConical },
  { key: "approve", icon: UserCheck },
  { key: "act", icon: Zap },
];

export default function DecisionLoop() {
  const { t } = useTranslation();

  return (
    <div className="rounded-2xl border border-[#EDE2D0] bg-white p-5">
      <div className="mb-5">
        <h2 className="font-bold text-[#3D2918]">
          {t("dashboard.decisionLoop")}
        </h2>

        <p className="text-sm text-[#8B735D]">
          {t("dashboard.decisionLoopSubtitle")}
        </p>
      </div>

      <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <div
              key={step.key}
              className="flex w-full items-center md:w-auto"
            >
              <div className="flex flex-1 flex-col items-center">
                <div
                  className={`flex h-11 w-11 items-center justify-center rounded-full ${
                    index === 0
                      ? "bg-[#F28C00] text-white"
                      : "bg-[#F8E7CF] text-[#D96F00]"
                  }`}
                >
                  <Icon size={19} />
                </div>

                <span className="mt-2 text-xs font-semibold uppercase tracking-wide text-[#6B421F]">
                  {t(`dashboard.loop.${step.key}`)}
                </span>
              </div>

              {index < steps.length - 1 && (
                <div className="hidden h-px w-8 bg-[#EDE2D0] md:block" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
