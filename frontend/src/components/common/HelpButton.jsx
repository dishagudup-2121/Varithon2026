import { Info } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function HelpButton({ onClick }) {
  const { t } = useTranslation();

  return (
    <button
      onClick={onClick}
      title={t("help.open")}
      aria-label={t("help.open")}
      className="flex h-8 w-8 items-center justify-center rounded-lg text-[#9B836B] transition hover:bg-[#F8E7CF] hover:text-[#D96F00]"
    >
      <Info size={18} />
    </button>
  );
}
