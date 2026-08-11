import { useTranslation } from 'react-i18next';
import { ArrowRight } from 'lucide-react';

export default function SimulationPanel() {
  const { t } = useTranslation();

  return (
    <div className="panel col-span-12 xl:col-span-12 flex flex-col xl:flex-row divide-y xl:divide-y-0 xl:divide-x divide-slate-700/50">
      
      {/* Controls */}
      <div className="p-4 flex flex-col w-full xl:w-64 shrink-0">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">
          {t('what_if_simulation_title')}
        </h3>
        <label className="text-[10px] text-slate-500 uppercase mb-1">{t('scenario')}</label>
        <select className="bg-slate-900 border border-slate-700 rounded-lg p-2 text-sm text-white focus:outline-none focus:border-orange-500 mb-4 w-full">
          <option>Close Route A</option>
          <option>Deploy Tanker 2 to Z7</option>
        </select>
        <button className="bg-orange-600 hover:bg-orange-500 text-white font-bold py-2 px-4 rounded-lg transition-colors text-xs uppercase tracking-wider mt-auto">
          {t('run_simulation')}
        </button>
      </div>

      {/* Metrics Before/After */}
      <div className="p-4 flex-1 flex flex-col justify-center">
        <div className="flex flex-col md:flex-row items-center gap-6 xl:gap-12">
          
          {/* Before */}
          <div className="flex-1 w-full">
            <h4 className="text-[10px] font-bold text-slate-500 uppercase mb-4">{t('current_state')}</h4>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">{t('congestion')}</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-green-500 w-[62%]"></div>
                  </div>
                  <span className="text-xs font-mono">62%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">{t('avg_eta')}</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-amber-500 w-[40%]"></div>
                  </div>
                  <span className="text-xs font-mono">18 min</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">{t('risk_zones')}</span>
                <span className="text-xs font-mono text-amber-400 font-bold">2</span>
              </div>
            </div>
          </div>

          {/* Arrow */}
          <ArrowRight className="hidden md:block w-8 h-8 text-slate-600 shrink-0" />

          {/* After */}
          <div className="flex-1 w-full">
            <h4 className="text-[10px] font-bold text-slate-500 uppercase mb-4">{t('simulation_result')}</h4>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">{t('congestion')}</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 w-[80%]"></div>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-xs font-mono">80%</span>
                    <span className="text-[10px] font-mono text-red-400 font-bold">▲18%</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">{t('avg_eta')}</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 w-[70%]"></div>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-xs font-mono">27 min</span>
                    <span className="text-[10px] font-mono text-red-400 font-bold">▲9 min</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">{t('risk_zones')}</span>
                <div className="flex items-center gap-1">
                  <span className="text-xs font-mono text-red-400 font-bold">3</span>
                  <span className="text-[10px] font-mono text-red-400 font-bold">▲1</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Impact & Actions */}
      <div className="p-4 flex flex-col xl:flex-row gap-6 xl:w-[400px] shrink-0">
        <div className="flex-1">
          <h4 className="text-[10px] font-bold text-orange-400 uppercase mb-2">{t('impact')}</h4>
          <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
            <li>Increased crowd on alternate routes</li>
            <li>Delays expected in Zones 4, 5, 7</li>
            <li>Additional resources required</li>
          </ul>
        </div>
        
        <div className="flex flex-col gap-2 w-full xl:w-28 shrink-0">
          <button className="bg-green-600/20 hover:bg-green-600 text-green-400 hover:text-white border border-green-600/50 rounded p-2 text-xs font-bold uppercase transition-colors">
            {t('approve')}
          </button>
          <button className="bg-amber-600/20 hover:bg-amber-600 text-amber-400 hover:text-white border border-amber-600/50 rounded p-2 text-xs font-bold uppercase transition-colors">
            {t('modify')}
          </button>
          <button className="bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white border border-red-600/50 rounded p-2 text-xs font-bold uppercase transition-colors">
            {t('reject')}
          </button>
        </div>
      </div>
      
    </div>
  );
}
