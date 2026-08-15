import {
  X,
  AlertTriangle,
  CheckCircle,
  ShieldAlert,
} from "lucide-react";

import { useTranslation } from "react-i18next";

import { Alert } from '../../types';

export default function AlertDetails({
  alert,
  onClose,
}: {
  alert: Alert;
  onClose: () => void;
}) {
  const { t } = useTranslation();

  if (!alert) return null;

  const isResolved =
    alert.status === "resolved";

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm">

      <div className="w-full max-w-lg overflow-hidden rounded-2xl border border-[#EDE2D0] bg-[#FFFDF8] shadow-2xl">

        {/* Header */}

        <div className="flex items-center justify-between border-b border-[#EDE2D0] px-5 py-4">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#F8E7CF] text-[#D96F00]">
              {isResolved ? (
                <CheckCircle size={20} />
              ) : (
                <AlertTriangle size={20} />
              )}
            </div>

            <div>

              <h2 className="font-bold text-[#3D2918]">
                {t("alerts.detailsTitle")}
              </h2>

              <p className="text-xs text-[#9B836B]">
                {alert.zone}
              </p>

            </div>

          </div>

          <button
            onClick={onClose}
            className="rounded-lg p-2 text-[#6B421F] hover:bg-[#F8E7CF]"
          >
            <X size={20} />
          </button>

        </div>

        {/* Content */}

        <div className="space-y-5 p-5">

          <div>

            <p className="text-xs font-semibold uppercase tracking-wide text-[#9B836B]">
              {t("alerts.alert")}
            </p>

            <h3 className="mt-1 text-lg font-bold text-[#3D2918]">
              {t(alert.titleKey)}
            </h3>

            <p className="mt-2 text-sm leading-6 text-[#6B421F]">
              {t(alert.descriptionKey)}
            </p>

          </div>

          {/* Risk */}

          <div className="rounded-xl bg-[#F8F1E5] p-4">

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-2">
                <ShieldAlert
                  size={18}
                  className="text-[#D96F00]"
                />

                <span className="text-sm font-semibold text-[#3D2918]">
                  {t("alerts.riskScore")}
                </span>
              </div>

              <span className="text-xl font-bold text-[#D96F00]">
                {alert.riskScore}%
              </span>

            </div>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-white">

              <div
                className="h-full rounded-full bg-[#F28C00]"
                style={{
                  width: `${alert.riskScore}%`,
                }}
              />

            </div>

          </div>

          {/* Details */}

          <div className="grid grid-cols-2 gap-3">

            <div className="rounded-xl border border-[#EDE2D0] p-3">

              <p className="text-xs text-[#9B836B]">
                {t("alerts.predictedIn")}
              </p>

              <p className="mt-1 font-bold text-[#3D2918]">
                {alert.predictedTime}
              </p>

            </div>

            <div className="rounded-xl border border-[#EDE2D0] p-3">

              <p className="text-xs text-[#9B836B]">
                {t("alerts.status")}
              </p>

              <p className="mt-1 font-bold capitalize text-[#3D2918]">
                {t(`alerts.statusValues.${alert.status}`)}
              </p>

            </div>

          </div>

          {/* Recommendation */}

          <div className="rounded-xl border border-[#E8D3B5] bg-[#FFF8EC] p-4">

            <p className="text-xs font-semibold uppercase tracking-wide text-[#9B836B]">
              {t("alerts.recommendedAction")}
            </p>

            <p className="mt-2 text-sm font-semibold leading-6 text-[#6B421F]">
              {t(alert.recommendationKey)}
            </p>

          </div>

        </div>

        {/* Footer */}

        <div className="border-t border-[#EDE2D0] p-4">

          <button
            onClick={onClose}
            className="w-full rounded-xl bg-[#F28C00] py-3 text-sm font-semibold text-white hover:bg-[#D96F00]"
          >
            {t("alerts.close")}
          </button>

        </div>

      </div>

    </div>
  );
}
