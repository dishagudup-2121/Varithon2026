import { Bell, Menu, Globe } from "lucide-react";
import { useTranslation } from "react-i18next";

interface TopbarProps {
  setMobileOpen: (open: boolean) => void;
}

export default function Topbar({ setMobileOpen }: TopbarProps) {
  const { t, i18n } = useTranslation();

  const changeLanguage = (language: string) => {
    i18n.changeLanguage(language);
    localStorage.setItem("varisetuLanguage", language);

    const userStr = localStorage.getItem("varisetuUser");
    const user = userStr ? JSON.parse(userStr) : null;

    if (user) {
      user.language = language;
      localStorage.setItem("varisetuUser", JSON.stringify(user));
    }
  };

  const user = JSON.parse(localStorage.getItem("varisetuUser") || "{}");

  return (
    <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-[#EDE2D0] bg-[#FFFDF8]/95 px-3 backdrop-blur sm:px-5 md:px-8">
      <div className="flex items-center gap-2 sm:gap-4">
        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="rounded-lg p-2 text-[#6B421F] hover:bg-[#F8F1E5] lg:hidden cursor-pointer"
          aria-label="Open menu"
        >
          <Menu size={22} />
        </button>

        <div>
          <h1 className="text-base font-bold text-[#3D2918] sm:text-lg md:text-xl">
            {t("dashboard.title")}
          </h1>

          <p className="hidden text-xs text-[#8B735D] sm:block md:text-sm">
            {t("dashboard.subtitle")}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3 md:gap-4">
        <div className="flex items-center gap-1 rounded-lg border border-[#EDE2D0] bg-white p-1">
          <Globe size={14} className="ml-1 text-[#6B421F] hidden sm:block" />

          <button
            type="button"
            onClick={() => changeLanguage("en")}
            className={`rounded-md px-1.5 py-1 text-xs sm:px-2 cursor-pointer ${
              i18n.language === "en"
                ? "bg-[#F28C00] text-white font-medium"
                : "text-[#6B421F] hover:bg-[#F8F1E5]"
            }`}
          >
            <span className="hidden sm:inline">English</span>
            <span className="sm:hidden">EN</span>
          </button>

          <button
            type="button"
            onClick={() => changeLanguage("mr")}
            className={`rounded-md px-1.5 py-1 text-xs sm:px-2 cursor-pointer ${
              i18n.language === "mr"
                ? "bg-[#F28C00] text-white font-medium"
                : "text-[#6B421F] hover:bg-[#F8F1E5]"
            }`}
          >
            मराठी
          </button>
        </div>

        <button 
          type="button"
          className="relative rounded-lg p-2 text-[#6B421F] hover:bg-[#F8F1E5] cursor-pointer"
          aria-label="Notifications"
        >
          <Bell size={20} />
          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-[#D96F00]" />
        </button>

        <div className="flex items-center gap-2 border-l border-[#EDE2D0] pl-2 sm:pl-3">
          <div className="flex h-8 w-8 sm:h-9 sm:w-9 items-center justify-center rounded-full bg-[#F8E7CF] font-semibold text-[#D96F00] text-xs sm:text-sm">
            {(user.name || "U").charAt(0).toUpperCase()}
          </div>

          <div className="hidden md:block">
            <p className="text-sm font-semibold text-[#3D2918]">
              {user.name || "User"}
            </p>
            <p className="text-xs text-[#8B735D]">
              {t("dashboard.authorityUser")}
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}
