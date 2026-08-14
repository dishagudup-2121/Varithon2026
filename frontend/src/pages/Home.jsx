import {
  ArrowRight,
  Globe,
  ShieldCheck,
  Users,
  MapPin,
  Handshake,
  Clock,
} from "lucide-react";

import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

import logo from "../assets/logo_varithon.png";
import wariProcessionImg from "../assets/wari-procession.png";

export default function Home() {
  const { i18n } = useTranslation();

  const changeLanguage = (language) => {
    i18n.changeLanguage(language);
    localStorage.setItem("varisetuLanguage", language);
  };

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#FFFDF8] text-[#24170E]">

      {/* ================= NAVBAR ================= */}

      <header className="sticky top-0 z-50 border-b border-[#F1DEC8] bg-white/95 backdrop-blur">

        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">

          {/* Logo */}

          <Link
            to="/"
            className="flex items-center gap-3.5"
          >
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
                Technology that walks with the Wari.
              </p>
            </div>
          </Link>

          {/* Navigation */}

          <nav className="hidden items-center gap-8 lg:flex">

            <a
              href="#home"
              className="font-semibold text-[#E86F00]"
            >
              Home
            </a>

            <a
              href="#features"
              className="font-medium text-[#392719] transition hover:text-[#E86F00]"
            >
              Features
            </a>

            <Link
              to="/dashboard"
              className="font-medium text-[#392719] transition hover:text-[#E86F00]"
            >
              Dashboard
            </Link>

          </nav>

          {/* Right actions */}

          <div className="flex items-center gap-2 sm:gap-3">

            {/* Language */}

            <div className="flex items-center rounded-xl border border-[#F28C00] bg-white px-3 py-2 text-sm">

              <Globe
                size={16}
                className="mr-2 text-[#E86F00]"
              />

              <button
                type="button"
                onClick={() => changeLanguage("en")}
                className={`cursor-pointer ${
                  i18n.language === "en"
                    ? "font-bold text-[#E86F00]"
                    : "text-[#806B59]"
                }`}
              >
                English
              </button>

              <span className="mx-2 text-[#C9B29C]">
                |
              </span>

              <button
                type="button"
                onClick={() => changeLanguage("mr")}
                className={`cursor-pointer ${
                  i18n.language === "mr"
                    ? "font-bold text-[#E86F00]"
                    : "text-[#806B59]"
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
              Login
            </Link>

            {/* Signup */}

            <Link
              to="/signup"
              className="rounded-xl bg-[#F28C00] px-5 py-2.5 font-bold text-white shadow-md transition hover:bg-[#E06F00] hover:shadow-lg"
            >
              Sign Up
            </Link>

          </div>

        </div>

      </header>

      {/* ================= HERO ================= */}

      <main id="home">

        <section className="relative overflow-hidden bg-gradient-to-b from-[#FFF9EF] via-[#FFFDF8] to-[#FFE8C2]">

          {/* Decorative background */}

          <div className="absolute -left-40 top-20 h-80 w-80 rounded-full bg-[#F28C00]/10 blur-3xl pointer-events-none" />

          <div className="absolute -right-40 top-10 h-80 w-80 rounded-full bg-[#FFB84D]/15 blur-3xl pointer-events-none" />

          <div className="relative mx-auto max-w-7xl px-4 pt-8 text-center sm:px-6 lg:px-8 lg:pt-12">

            {/* Marathi heading */}

            <h1 className="mx-auto max-w-5xl text-4xl font-extrabold leading-tight tracking-tight text-[#E86F00] sm:text-5xl lg:text-6xl">
              माऊली चला वारिला
            </h1>

            {/* Decorative divider */}

            <div className="mx-auto mt-3 sm:mt-4 flex items-center justify-center gap-2">

              <div className="h-px w-16 bg-[#F28C00]" />

              <div className="h-2 w-2 rounded-full bg-[#E86F00]" />

              <div className="h-1.5 w-1.5 rounded-full bg-[#F28C00]" />

              <div className="h-px w-16 bg-[#F28C00]" />

            </div>

            <p className="mt-3 text-base sm:text-lg font-semibold text-[#2F2117]">
              Technology that walks with the Wari.
            </p>

            <h2 className="mx-auto mt-2 max-w-4xl text-xl font-bold leading-tight text-[#172033] sm:text-2xl lg:text-3xl">
              Safer journeys. Smarter decisions.
              <br className="hidden sm:block" />
              Stronger connections.
            </h2>

            {/* CTA */}

            <div className="mt-6 flex flex-col items-center justify-center gap-3 sm:flex-row sm:gap-4">

              <Link
                to="/signup"
                className="group flex w-full items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-[#F28C00] to-[#FF5A00] px-7 py-3.5 text-base font-bold text-white shadow-lg transition hover:-translate-y-1 hover:shadow-xl sm:w-auto"
              >
                Get Started

                <ArrowRight
                  size={19}
                  className="transition group-hover:translate-x-1"
                />

              </Link>

              <Link
                to="/dashboard"
                className="group flex w-full items-center justify-center gap-3 rounded-xl border-2 border-[#F28C00] bg-white px-7 py-3.5 text-base font-bold text-[#E86F00] shadow-sm transition hover:-translate-y-1 hover:bg-[#FFF5E7] sm:w-auto"
              >
                Explore VariSetu

                <ArrowRight
                  size={19}
                  className="transition group-hover:translate-x-1"
                />

              </Link>

            </div>

            {/* Feature highlights */}

            <div
              id="features"
              className="mx-auto mt-8 grid max-w-3xl grid-cols-2 gap-4 sm:grid-cols-4 sm:gap-6"
            >

              <FeatureIcon
                icon={<ShieldCheck size={22} />}
                title="AI-Powered"
                subtitle="Safety"
              />

              <FeatureIcon
                icon={<Users size={22} />}
                title="Real-time"
                subtitle="Monitoring"
              />

              <FeatureIcon
                icon={<MapPin size={22} />}
                title="Smart Route"
                subtitle="Management"
              />

              <FeatureIcon
                icon={<Handshake size={22} />}
                title="Better"
                subtitle="Coordination"
              />

            </div>

          </div>

          {/* ================= WARI IMAGE (1200 x 350 Transparent PNG) ================= */}

          <div className="relative mx-auto mt-6 max-w-[1200px] px-4 flex justify-center items-end">

            <img
              src={wariProcessionImg}
              alt="Wari procession"
              width="1200"
              height="350"
              className="w-full max-w-[1200px] h-auto max-h-[350px] object-contain object-bottom drop-shadow-sm"
            />

          </div>

          {/* ================= STATS ================= */}

          <div className="relative z-10 mx-4 -mt-3 sm:-mt-6 rounded-2xl border border-[#F1DEC8] bg-white p-5 shadow-xl sm:mx-auto sm:max-w-5xl mb-12">

            <div className="grid grid-cols-2 divide-x divide-y divide-[#F1DEC8] sm:grid-cols-4 sm:divide-y-0">

              <Stat
                icon={<Users size={22} />}
                number="2.5L+"
                label="Warkaris Supported"
              />

              <Stat
                icon={<ShieldCheck size={22} />}
                number="98%"
                label="Safety Accuracy"
              />

              <Stat
                icon={<MapPin size={22} />}
                number="500+"
                label="Active Zones"
              />

              <Stat
                icon={<Clock size={22} />}
                number="24/7"
                label="Monitoring"
              />

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}


/* ================= FEATURE ================= */

function FeatureIcon({
  icon,
  title,
  subtitle,
}) {
  return (
    <div className="flex flex-col items-center">

      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#FFF0DF] text-[#E86F00] shadow-sm">
        {icon}
      </div>

      <p className="mt-2 text-xs sm:text-sm font-bold text-[#24170E]">
        {title}
      </p>

      <p className="text-xs sm:text-sm font-bold text-[#24170E]">
        {subtitle}
      </p>

    </div>
  );
}


/* ================= STAT ================= */

function Stat({
  icon,
  number,
  label,
}) {
  return (
    <div className="flex items-center justify-center gap-3 px-3 py-3">

      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#FFF0DF] text-[#E86F00]">
        {icon}
      </div>

      <div className="text-left">

        <p className="text-xl sm:text-2xl font-extrabold text-[#E86F00]">
          {number}
        </p>

        <p className="text-xs text-[#806B59]">
          {label}
        </p>

      </div>

    </div>
  );
}
