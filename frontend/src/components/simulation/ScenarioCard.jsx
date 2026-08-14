import {
  Route,
  Users,
  Ambulance,
  Check,
} from "lucide-react";

import { useTranslation } from "react-i18next";

const icons = {
  route: Route,
  volunteers: Users,
  ambulance: Ambulance,
};

export default function ScenarioCard({
  scenario,
  selected,
  onSelect,
}) {
  const { t } = useTranslation();

  const Icon = icons[scenario.icon] || Route;

  return (
    <button
      type="button"
      onClick={() => onSelect(scenario.id)}
      className={`relative w-full rounded-2xl border p-5 text-left transition cursor-pointer ${
        selected
          ? "border-[#F28C00] bg-[#FFF8EC] shadow-sm ring-1 ring-[#F28C00]"
          : "border-[#EDE2D0] bg-white hover:border-[#E8D3B5] hover:bg-[#FFFDF8]"
      }`}
    >
      {selected && (
        <div className="absolute right-4 top-4 flex h-6 w-6 items-center justify-center rounded-full bg-[#F28C00] text-white">
          <Check size={14} />
        </div>
      )}

      <div
        className={`flex h-11 w-11 items-center justify-center rounded-xl ${
          selected
            ? "bg-[#F28C00] text-white"
            : "bg-[#F8E7CF] text-[#D96F00]"
        }`}
      >
        <Icon size={21} />
      </div>

      <h3 className="mt-4 font-bold text-[#3D2918]">
        {t(scenario.titleKey)}
      </h3>

      <p className="mt-1 text-sm leading-5 text-[#8B735D]">
        {t(scenario.descriptionKey)}
      </p>
    </button>
  );
}
