import { useState } from "react";
import {
  ArrowLeft,
  Info,
  CheckCircle,
} from "lucide-react";

import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ResourceAllocation, ResourceSummary } from "../types";

import ResourceSummaryCard from "../components/resources/ResourceSummaryCard";
import AllocationTable from "../components/resources/AllocationTable";

import HowItWorks from "../components/common/HowItWorks";
import HelpButton from "../components/common/HelpButton";
import logoImg from "../assets/logo_varithon.png";

const resourceSummary: ResourceSummary[] = [
  { id: "1", type: "ambulance", titleKey: "resources.ambulances", total: "45", available: "12" },
  { id: "2", type: "volunteers", titleKey: "resources.volunteers", total: "320", available: "150" },
  { id: "3", type: "water", titleKey: "resources.waterTankers", total: "20", available: "8" },
  { id: "4", type: "medical", titleKey: "resources.medicalTeams", total: "15", available: "5" }
];

const mockAllocations: ResourceAllocation[] = [
  {
    id: "R001",
    type: "ambulance",
    resource: "Ambulance A-12",
    name: "Ambulance A-12",
    from: "Zone 2",
    destination: "Zone 6",
    to: "Zone 6",
    eta: "5 mins"
  },
  {
    id: "R002",
    type: "volunteers",
    resource: "Volunteer Team V-08",
    name: "Volunteer Team V-08",
    from: "Zone 4",
    destination: "Zone 6",
    to: "Zone 6",
    eta: "12 mins"
  },
  {
    id: "R003",
    type: "water",
    resource: "Water Tanker WT-03",
    name: "Water Tanker WT-03",
    from: "Depot North",
    destination: "Zone 4",
    to: "Zone 4",
    eta: "25 mins"
  }
];

export default function Resources() {

  const { t } = useTranslation();
  const navigate = useNavigate();

  const [helpOpen, setHelpOpen] = useState(false);
  const [assigned, setAssigned] = useState<string[]>([]);

  const handleAssign = (resource: ResourceAllocation) => {

    setAssigned((previous) => [
      ...previous,
      resource.id,
    ]);

  };

  return (
    <div className="min-h-screen bg-[#FFFDF8]">

      {/* Header */}

      <header className="flex items-center justify-between border-b border-[#EDE2D0] bg-white px-4 py-3.5 md:px-8 md:py-4">

        <div className="flex items-center gap-3">

          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            className="rounded-lg p-2 text-[#6B421F] hover:bg-[#F8F1E5] cursor-pointer"
            aria-label="Back to dashboard"
          >
            <ArrowLeft size={20} />
          </button>

          <div className="flex items-center gap-2.5 sm:gap-3">
            <img
              src={logoImg}
              alt="VariSetu Logo"
              width="44"
              height="44"
              className="h-10 w-10 sm:h-11 sm:w-11 object-contain shrink-0"
            />

            <div>
              <h1 className="text-base sm:text-lg font-bold text-[#3D2918]">
                {t("resources.title")}
              </h1>

              <p className="text-xs text-[#8B735D] hidden xs:block">
                {t("resources.subtitle")}
              </p>
            </div>
          </div>

        </div>

        <HelpButton
          onClick={() => setHelpOpen(true)}
        />

      </header>

      <main className="mx-auto max-w-[1500px] p-4 md:p-8">

        {/* Intro */}

        <section className="mb-7">

          <p className="text-sm font-medium text-[#E86F00]">
            {t("resources.commandCenter")}
          </p>

          <h2 className="mt-1 text-2xl font-bold text-[#3D2918] md:text-3xl">
            {t("resources.overviewTitle")}
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-[#8B735D]">
            {t("resources.overviewDescription")}
          </p>

        </section>

        {/* Summary */}

        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

          {resourceSummary.map((resource: ResourceSummary) => (
            <ResourceSummaryCard
              key={resource.id}
              resource={resource}
            />
          ))}

        </section>

        {/* Recommendation */}

        <section className="mt-6">

          <div className="mb-4 flex items-center justify-between">

            <div>
              <h2 className="font-bold text-[#3D2918]">
                {t("resources.aiSectionTitle")}
              </h2>

              <p className="mt-1 text-sm text-[#8B735D]">
                {t("resources.aiSectionSubtitle")}
              </p>
            </div>

            {assigned.length > 0 && (
              <div className="flex items-center gap-2 rounded-full bg-[#EDF7E8] px-3 py-2 text-xs font-semibold text-green-700">
                <CheckCircle size={14} />
                {assigned.length} {t("resources.assigned")}
              </div>
            )}

          </div>

          <AllocationTable
            allocations={mockAllocations}
            onAssign={handleAssign}
          />

        </section>

        {/* Disclaimer */}

        <div className="mt-5 flex gap-3 rounded-xl border border-[#E8D3B5] bg-[#FFF8EC] p-4">

          <Info
            size={18}
            className="mt-0.5 shrink-0 text-[#E86F00]"
          />

          <p className="text-xs leading-5 text-[#8B735D]">
            {t("resources.prototypeNote")}
          </p>

        </div>

      </main>

      <HowItWorks
        feature="resources"
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />

    </div>
  );
}
