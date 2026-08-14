import { useTranslation } from "react-i18next";

export default function SuggestionButton({
  suggestion,
  onClick,
}) {
  const { t } = useTranslation();

  return (
    <button
      type="button"
      onClick={onClick}
      className="rounded-xl border border-[#E8D3B5] bg-[#FFF8EC] px-4 py-3 text-left text-sm font-medium text-[#6B421F] transition hover:border-[#F28C00] hover:bg-[#F8E7CF] cursor-pointer"
    >
      {t(suggestion.textKey)}
    </button>
  );
}
