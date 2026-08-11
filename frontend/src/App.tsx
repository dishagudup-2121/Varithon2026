import { useTranslation } from 'react-i18next';
import AppShell from './components/layout/AppShell';
import KpiCard from './components/dashboard/KpiCard';
import DigitalTwinMap from './components/digital-twin/DigitalTwinMap';
import AlertsPanel from './components/dashboard/AlertsPanel';
import RecommendationPanel from './components/dashboard/RecommendationPanel';
import SimulationPanel from './components/dashboard/SimulationPanel';

export default function App() {
  const { t } = useTranslation();

  return (
    <AppShell>
      <div className="flex flex-col h-full gap-4 min-w-[1024px] max-w-[1920px] mx-auto">
        
        {/* KPI Row */}
        <div className="grid grid-cols-6 gap-4 shrink-0">
          <KpiCard 
            title={t('total_pilgrims')} 
            value="12,840" 
            subValue={<>▲ 8.5% <span className="text-slate-500">{t('vs_last_hour')}</span></>} 
            subValueColor="green" 
          />
          <KpiCard 
            title={t('high_risk_zones')} 
            value="2" 
            subValue="▲ Critical" 
            subValueColor="red" 
          />
          <KpiCard 
            title={t('ambulances')} 
            value="8" 
            subValue="Available 3" 
            subValueColor="green" 
          />
          <KpiCard 
            title={t('volunteers')} 
            value="34" 
            subValue="Active" 
            subValueColor="green" 
          />
          <KpiCard 
            title={t('water_tankers')} 
            value="5" 
            subValue="Available 2" 
            subValueColor="green" 
          />
          <KpiCard 
            title={t('avg_temperature')} 
            value="34.6°C" 
            subValue="▲ High" 
            subValueColor="amber" 
          />
        </div>

        {/* Main Content Area */}
        <div className="flex flex-1 gap-4 min-h-0">
          
          {/* Left/Center: Digital Twin */}
          <div className="flex-1 flex flex-col h-full">
            <DigitalTwinMap />
          </div>

          {/* Right: Operations Panels */}
          <div className="w-[320px] xl:w-[380px] flex flex-col gap-4 shrink-0 overflow-y-auto pr-1">
            <AlertsPanel />
            <RecommendationPanel />
          </div>
          
        </div>

        {/* Bottom: Simulation Panel */}
        <div className="shrink-0">
          <SimulationPanel />
        </div>

      </div>
    </AppShell>
  );
}
