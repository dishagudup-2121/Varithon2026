import { Link, useLocation } from "react-router-dom";
import { Globe } from "lucide-react";
import { useTranslation } from "react-i18next";
import logo from "../../assets/logo_varithon.png";

export default function PublicNavbar() {
  const { t, i18n } = useTranslation();
  const location = useLocation();
  const isSolutionActive = location.pathname === "/solution";

  const changeLanguage = (language: string) => {
    i18n.changeLanguage(language);
    localStorage.setItem("varisetuLanguage", language);
  };

  return (
    <header className="sticky top-0 z-50 border-b border-[#F1DEC8] bg-white/95 backdrop-blur">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3.5">
          <img
            src={logo}
            alt="VariSetu"
            width="75"
            height="75"
            className="h-[70px] w-[70px] sm:h-[76px] sm:w-[76px] object-contain shrink-0"
          />
          <div>
            <div className="text-2xl font-extrabold tracking-tight text-[#E86F00]">
              VariSetu
            </div>
            <p className="hidden text-xs text-[#806B59] sm:block">
              {t("hero.tagline")}
            </p>
          </div>
        </Link>

        {/* Navigation */}
        <nav className="hidden items-center gap-8 lg:flex">
          <Link
            to="/"
            className={`font-semibold ${!isSolutionActive ? "text-[#E86F00]" : "text-[#392719] hover:text-[#E86F00]"} transition`}
          >
            {t("nav.home")}
          </Link>
          <a
            href="/#features"
            className="font-medium text-[#392719] transition hover:text-[#E86F00]"
          >
            {t("nav.features")}
          </a>
          <Link
            to="/solution"
            className={`font-semibold ${isSolutionActive ? "text-[#E86F00]" : "text-[#392719] hover:text-[#E86F00]"} transition`}
          >
            {t("nav.solution")}
          </Link>
          <Link
            to="/dashboard"
            className="font-medium text-[#392719] transition hover:text-[#E86F00]"
          >
            {t("nav.dashboard")}
          </Link>
        </nav>

        {/* Right actions */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Language */}
          <div className="flex items-center rounded-xl border border-[#F28C00] bg-white px-3 py-2 text-sm">
            <Globe size={16} className="mr-2 text-[#E86F00]" />
            <button
              type="button"
              onClick={() => changeLanguage("en")}
              className={`cursor-pointer ${
                i18n.language === "en" ? "font-bold text-[#E86F00]" : "text-[#806B59]"
              }`}
            >
              English
            </button>
            <span className="mx-2 text-[#C9B29C]">|</span>
            <button
              type="button"
              onClick={() => changeLanguage("mr")}
              className={`cursor-pointer ${
                i18n.language === "mr" ? "font-bold text-[#E86F00]" : "text-[#806B59]"
              }`}
            >
              मराठी
            </button>
          </div>

          {/* Login */}
          <Link
            to="/login"
            className="hidden rounded-xl border-2 border-[#F28C00] px-5 py-2.5 font-bold text-[#D96F00] transition hover:bg-[#FFF3E2] sm:block"
          >
            {t("nav.login")}
          </Link>

          {/* Signup */}
          <Link
            to="/signup"
            className="rounded-xl bg-[#F28C00] px-5 py-2.5 font-bold text-white shadow-md transition hover:bg-[#E06F00] hover:shadow-lg"
          >
            {t("nav.signup")}
          </Link>
        </div>
      </div>
    </header>
  );
}
