import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  ArrowRight, 
  MapPin, 
  Users, 
  Activity, 
  ShieldAlert, 
  Clock, 
  Cpu, 
  Database, 
  Server, 
  Eye, 
  CheckCircle2, 
  CircleDashed,
  AlertTriangle
} from "lucide-react";
import PublicNavbar from "../components/common/PublicNavbar";

export default function Solution() {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#FFFDF8] text-[#24170E] font-sans">
      <PublicNavbar />

      {/* SECTION 1 — HERO */}
      <section className="relative overflow-hidden bg-gradient-to-b from-[#FFF9EF] via-[#FFFDF8] to-white px-4 pt-16 pb-20 sm:px-6 lg:px-8">
        <div className="absolute -left-40 top-20 h-80 w-80 rounded-full bg-[#F28C00]/10 blur-3xl pointer-events-none" />
        <div className="absolute -right-40 top-10 h-80 w-80 rounded-full bg-[#FFB84D]/15 blur-3xl pointer-events-none" />
        
        <div className="relative mx-auto max-w-5xl text-center">
          <p className="mb-4 text-sm sm:text-base font-bold tracking-widest text-[#E86F00] uppercase">
            {t("solution.hero.tagline")}
          </p>
          <h1 className="text-4xl font-extrabold leading-tight tracking-tight text-[#172033] sm:text-5xl lg:text-6xl mb-6">
            {t("solution.hero.title")}
          </h1>
          <p className="mx-auto max-w-3xl text-lg sm:text-xl font-medium text-[#4A3B2C] mb-10 leading-relaxed">
            {t("solution.hero.subtitle")}
          </p>
          
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              to="/dashboard"
              className="group flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[#F28C00] to-[#FF5A00] px-8 py-4 text-base font-bold text-white shadow-lg transition hover:-translate-y-1 hover:shadow-xl sm:w-auto"
            >
              {t("solution.hero.ctaPrimary")}
              <ArrowRight size={19} className="transition group-hover:translate-x-1" />
            </Link>
            <a
              href="/#features"
              className="group flex w-full items-center justify-center gap-2 rounded-xl border-2 border-[#F28C00] bg-white px-8 py-4 text-base font-bold text-[#E86F00] shadow-sm transition hover:-translate-y-1 hover:bg-[#FFF5E7] sm:w-auto"
            >
              {t("solution.hero.ctaSecondary")}
            </a>
          </div>
        </div>
      </section>

      {/* SECTION 2 — THE PROBLEM */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-[#172033]">{t("solution.problem.title")}</h2>
          <div className="mx-auto mt-4 h-1 w-20 rounded bg-[#F28C00]" />
        </div>
        
        <div className="grid gap-8 lg:grid-cols-2">
          <div className="flex flex-col justify-center space-y-6 text-lg text-[#4A3B2C]">
            <p>{t("solution.problem.p1")}</p>
            <p>{t("solution.problem.p2")}</p>
            <p className="font-semibold text-[#172033]">{t("solution.problem.p3")}</p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <ProblemCard icon={<Users />} text={t("solution.problem.points.1")} />
            <ProblemCard icon={<Activity />} text={t("solution.problem.points.2")} />
            <ProblemCard icon={<MapPin />} text={t("solution.problem.points.3")} />
            <ProblemCard icon={<ShieldAlert />} text={t("solution.problem.points.4")} />
            <ProblemCard icon={<Clock />} text={t("solution.problem.points.5")} className="sm:col-span-2" />
          </div>
        </div>
      </section>

      {/* SECTION 3 — PROPOSED SOLUTION & SECTION 4 — HOW IT WORKS */}
      <section className="bg-[#FFF9EF] py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-12 text-center">
            <h2 className="text-3xl font-bold text-[#172033]">{t("solution.proposed.title")}</h2>
            <div className="mx-auto mt-4 h-1 w-20 rounded bg-[#F28C00]" />
            <p className="mt-6 mx-auto max-w-3xl text-lg text-[#4A3B2C]">
              {t("solution.proposed.description")}
            </p>
          </div>

          {/* Visual Flow */}
          <div className="mb-16 hidden md:flex items-center justify-center overflow-x-auto py-4">
            <div className="flex items-center space-x-2 text-sm font-bold text-[#D96F00] whitespace-nowrap">
              <span>LIVE / SIMULATED DATA</span>
              <ArrowRight size={16} className="text-[#F1DEC8]" />
              <span>DIGITAL TWIN</span>
              <ArrowRight size={16} className="text-[#F1DEC8]" />
              <span>SITUATIONAL AWARENESS</span>
              <ArrowRight size={16} className="text-[#F1DEC8]" />
              <span>WHAT-IF SIMULATION</span>
              <ArrowRight size={16} className="text-[#F1DEC8]" />
              <span>DECISION SUPPORT</span>
            </div>
          </div>

          <h3 className="text-2xl font-bold text-center text-[#172033] mb-8">{t("solution.howItWorks.title")}</h3>
          <div className="grid gap-6 md:grid-cols-3 lg:grid-cols-5">
            <StepCard number="01" title={t("solution.howItWorks.steps.01.title")} desc={t("solution.howItWorks.steps.01.desc")} />
            <StepCard number="02" title={t("solution.howItWorks.steps.02.title")} desc={t("solution.howItWorks.steps.02.desc")} />
            <StepCard number="03" title={t("solution.howItWorks.steps.03.title")} desc={t("solution.howItWorks.steps.03.desc")} />
            <StepCard number="04" title={t("solution.howItWorks.steps.04.title")} desc={t("solution.howItWorks.steps.04.desc")} />
            <StepCard number="05" title={t("solution.howItWorks.steps.05.title")} desc={t("solution.howItWorks.steps.05.desc")} />
          </div>
          
          <div className="mt-8 text-center text-sm font-medium text-[#806B59] bg-[#FFF5E7] p-4 rounded-xl border border-[#F1DEC8] inline-block">
            {t("solution.howItWorks.note")}
          </div>
        </div>
      </section>

      {/* SECTION 5 — SYSTEM ARCHITECTURE */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-[#172033]">{t("solution.architecture.title")}</h2>
          <div className="mx-auto mt-4 h-1 w-20 rounded bg-[#F28C00]" />
        </div>
        
        <div className="flex justify-center">
          <div className="flex flex-col items-center max-w-2xl w-full">
            <div className="w-full rounded-xl border-2 border-[#E86F00] bg-white p-6 shadow-sm text-center mb-6 relative z-10">
              <h4 className="font-bold text-[#172033] mb-1">{t("solution.architecture.frontend")}</h4>
              <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 h-6 w-0.5 bg-[#F1DEC8] z-0"></div>
              <ArrowRight size={16} className="absolute -bottom-7 left-1/2 -translate-x-1/2 text-[#F1DEC8] rotate-90 z-0" />
            </div>

            <div className="w-full rounded-xl border-2 border-[#806B59] bg-[#F9F7F4] p-6 text-center mb-6 relative mt-4 z-10">
              <h4 className="font-bold text-[#172033] mb-1">{t("solution.architecture.backend")}</h4>
              <div className="absolute -bottom-6 left-1/4 h-6 w-0.5 bg-[#F1DEC8] z-0"></div>
              <ArrowRight size={16} className="absolute -bottom-7 left-1/4 -translate-x-1/2 text-[#F1DEC8] rotate-90 z-0" />
              
              <div className="absolute -bottom-6 left-1/2 h-6 w-0.5 bg-[#F1DEC8] z-0"></div>
              <ArrowRight size={16} className="absolute -bottom-7 left-1/2 -translate-x-1/2 text-[#F1DEC8] rotate-90 z-0" />

              <div className="absolute -bottom-6 left-3/4 h-6 w-0.5 bg-[length:2px_6px] bg-[linear-gradient(to_bottom,#F1DEC8_50%,transparent_50%)] z-0"></div>
              <ArrowRight size={16} className="absolute -bottom-7 left-3/4 -translate-x-1/2 text-[#F1DEC8] rotate-90 z-0" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full mt-4 z-10">
              <div className="rounded-xl border border-[#F1DEC8] bg-white p-4 text-center shadow-sm">
                <Database size={24} className="mx-auto mb-2 text-[#E86F00]" />
                <h4 className="font-bold text-sm text-[#172033]">{t("solution.architecture.digitalTwin")}</h4>
              </div>
              <div className="rounded-xl border border-[#F1DEC8] bg-white p-4 text-center shadow-sm">
                <Cpu size={24} className="mx-auto mb-2 text-[#E86F00]" />
                <h4 className="font-bold text-sm text-[#172033]">{t("solution.architecture.simulation")}</h4>
              </div>
              <div className="rounded-xl border border-dashed border-[#C9B29C] bg-transparent p-4 text-center">
                <Server size={24} className="mx-auto mb-2 text-[#806B59]" />
                <h4 className="font-bold text-sm text-[#806B59]">{t("solution.architecture.future")}</h4>
              </div>
            </div>
            
            <div className="w-full mt-6 text-center text-sm font-semibold text-[#806B59]">
              ↓ {t("solution.architecture.data")} ↓
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 6 & 7 & 8 — DIGITAL TWIN, SIMULATION, DECISION INTELLIGENCE */}
      <section className="bg-white py-16 border-y border-[#F1DEC8]">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12 lg:grid-cols-3">
            <FeatureBlock 
              icon={<MapPin />}
              title={t("solution.digitalTwin.title")}
              desc={t("solution.digitalTwin.description")}
            />
            <FeatureBlock 
              icon={<Cpu />}
              title={t("solution.simulation.title")}
              desc={t("solution.simulation.description")}
              extra={t("solution.simulation.examples")}
            />
            <FeatureBlock 
              icon={<Activity />}
              title={t("solution.decisionIntelligence.title")}
              desc={t("solution.decisionIntelligence.description")}
              extra={t("solution.decisionIntelligence.aiNote")}
            />
          </div>
        </div>
      </section>

      {/* SECTION 9 — CURRENT PROTOTYPE STATUS */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-[#172033]">{t("solution.prototypeStatus.title")}</h2>
          <div className="mx-auto mt-4 h-1 w-20 rounded bg-[#F28C00]" />
        </div>
        
        <div className="grid gap-8 md:grid-cols-2">
          <div className="rounded-2xl border-2 border-[#E86F00] bg-white p-8 shadow-md">
            <h3 className="mb-6 flex items-center gap-2 text-lg font-bold text-[#D96F00]">
              <CheckCircle2 size={22} />
              {t("solution.prototypeStatus.current.title")}
            </h3>
            <ul className="space-y-3">
              {(t("solution.prototypeStatus.current.items", { returnObjects: true }) as string[]).map((item, i) => (
                <li key={i} className="flex items-start gap-3 text-[#4A3B2C]">
                  <div className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-[#E86F00]" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="rounded-2xl border border-dashed border-[#806B59] bg-[#F9F7F4] p-8">
            <h3 className="mb-6 flex items-center gap-2 text-lg font-bold text-[#806B59]">
              <CircleDashed size={22} />
              {t("solution.prototypeStatus.future.title")}
            </h3>
            <ul className="space-y-3">
              {(t("solution.prototypeStatus.future.items", { returnObjects: true }) as string[]).map((item, i) => (
                <li key={i} className="flex items-start gap-3 text-[#806B59]">
                  <div className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-[#C9B29C]" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* SECTION 10 & 11 — DATA INTEGRITY & TECHNOLOGY */}
      <section className="bg-[#FFF9EF] py-16 border-y border-[#F1DEC8]">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12 lg:grid-cols-2">
            
            <div>
              <h2 className="text-2xl font-bold text-[#172033] mb-6">{t("solution.trust.title")}</h2>
              <p className="text-[#4A3B2C] mb-6">{t("solution.trust.description")}</p>
              <div className="space-y-4">
                <TrustBadge type="live" text={t("solution.trust.live")} />
                <TrustBadge type="simulated" text={t("solution.trust.simulated")} />
                <TrustBadge type="unavailable" text={t("solution.trust.unavailable")} />
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-[#172033] mb-6">{t("solution.technology.title")}</h2>
              <div className="flex flex-wrap gap-3">
                {(t("solution.technology.items", { returnObjects: true }) as string[]).map((item, i) => (
                  <div key={i} className="rounded-xl border border-[#F1DEC8] bg-white px-4 py-2 text-sm font-semibold text-[#E86F00] shadow-sm">
                    {item}
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* SECTION 12 & 13 — IMPACT & ROADMAP */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2">
          <div>
            <h2 className="text-2xl font-bold text-[#172033] mb-6">{t("solution.impact.title")}</h2>
            <div className="space-y-6">
              {[1, 2, 3, 4, 5].map((num) => (
                <div key={num} className="border-l-2 border-[#F28C00] pl-4">
                  <h4 className="font-bold text-[#172033]">
                    {t(`solution.impact.points.${num}.title`)}
                  </h4>
                  <p className="text-sm text-[#4A3B2C] mt-1">
                    {t(`solution.impact.points.${num}.desc`)}
                  </p>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h2 className="text-2xl font-bold text-[#172033] mb-6">{t("solution.roadmap.title")}</h2>
            <div className="rounded-2xl border border-[#F1DEC8] bg-white p-6 shadow-sm">
              <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-[#F28C00] before:to-[#F1DEC8]">
                <RoadmapStep num="1" text={t("solution.roadmap.p1")} active />
                <RoadmapStep num="2" text={t("solution.roadmap.p2")} />
                <RoadmapStep num="3" text={t("solution.roadmap.p3")} />
                <RoadmapStep num="4" text={t("solution.roadmap.p4")} />
                <RoadmapStep num="5" text={t("solution.roadmap.p5")} />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 14 — FINAL CTA */}
      <section className="bg-gradient-to-b from-white to-[#FFF9EF] py-20 text-center border-t border-[#F1DEC8]">
        <div className="mx-auto max-w-3xl px-4">
          <h2 className="text-3xl font-extrabold text-[#172033] mb-4">{t("solution.finalCta.title")}</h2>
          <p className="text-lg text-[#4A3B2C] mb-8">{t("solution.finalCta.description")}</p>
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              to="/dashboard"
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#F28C00] px-8 py-4 text-base font-bold text-white shadow-lg transition hover:bg-[#E06F00] hover:shadow-xl sm:w-auto"
            >
              {t("solution.finalCta.primary")}
            </Link>
            <a
              href="/#features"
              className="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-[#F1DEC8] bg-white px-8 py-4 text-base font-bold text-[#392719] transition hover:bg-[#F9F7F4] sm:w-auto"
            >
              {t("solution.finalCta.secondary")}
            </a>
          </div>
        </div>
      </section>

    </div>
  );
}

// ---------------- Helper Components ----------------

function ProblemCard({ icon, text, className = "" }: { icon: React.ReactNode; text: string; className?: string }) {
  return (
    <div className={`flex items-center gap-4 rounded-xl border border-[#F1DEC8] bg-white p-5 shadow-sm transition hover:shadow-md ${className}`}>
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[#FFF0DF] text-[#E86F00]">
        {icon}
      </div>
      <p className="font-bold text-[#172033]">{text}</p>
    </div>
  );
}

function StepCard({ number, title, desc }: { number: string; title: string; desc: string }) {
  return (
    <div className="relative rounded-xl bg-white p-5 shadow-sm border border-[#F1DEC8] flex flex-col h-full">
      <div className="text-3xl font-black text-[#F28C00]/20 absolute top-4 right-4">{number}</div>
      <h4 className="font-bold text-[#E86F00] mb-3 mt-4">{title}</h4>
      <p className="text-sm text-[#4A3B2C] flex-1">{desc}</p>
    </div>
  );
}

function FeatureBlock({ icon, title, desc, extra }: { icon: React.ReactNode; title: string; desc: string; extra?: string }) {
  return (
    <div className="flex flex-col items-center text-center">
      <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-[#FFF0DF] text-[#E86F00] shadow-sm">
        {icon}
      </div>
      <h3 className="mb-3 text-xl font-bold text-[#172033]">{title}</h3>
      <p className="text-[#4A3B2C] leading-relaxed">{desc}</p>
      {extra && <p className="mt-4 text-sm font-medium text-[#806B59] bg-[#F9F7F4] px-4 py-2 rounded-lg">{extra}</p>}
    </div>
  );
}

function TrustBadge({ type, text }: { type: "live" | "simulated" | "unavailable"; text: string }) {
  const styles = {
    live: "border-[#10B981] bg-[#ECFDF5] text-[#047857]",
    simulated: "border-[#3B82F6] bg-[#EFF6FF] text-[#1D4ED8]",
    unavailable: "border-[#9CA3AF] bg-[#F3F4F6] text-[#4B5563]"
  };
  return (
    <div className={`rounded-xl border p-4 shadow-sm ${styles[type]}`}>
      <div className="flex items-start gap-3">
        {type === "unavailable" ? <AlertTriangle className="shrink-0 mt-0.5" size={20} /> : <Eye className="shrink-0 mt-0.5" size={20} />}
        <p className="font-medium text-sm leading-relaxed">{text}</p>
      </div>
    </div>
  );
}

function RoadmapStep({ num, text, active = false }: { num: string; text: string; active?: boolean }) {
  return (
    <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
      <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-[#F28C00] text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-bold">
        {num}
      </div>
      <div className={`w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border shadow-sm ${active ? 'bg-[#FFF9EF] border-[#F28C00]' : 'bg-white border-[#F1DEC8]'}`}>
        <p className={`font-semibold text-sm ${active ? 'text-[#D96F00]' : 'text-[#806B59]'}`}>{text}</p>
      </div>
    </div>
  );
}
