import { useTranslation } from 'react-i18next';
import { Ambulance, Users, Droplets } from 'lucide-react';

export default function RecommendationPanel() {
  const { t } = useTranslation();

  return (
    <div className="panel flex flex-col h-[320px]">
      <div className="panel-header">
        <span>{t('ai_recommendation')}</span>
      </div>
      <div className="p-4 flex flex-col flex-1">
        <div className="text-xs text-slate-400 mb-4">{t('based_on_prediction')}</div>
        
        <div className="space-y-3 flex-1">
          {/* Mock Assignment 1 */}
          <div className="flex items-center justify-between bg-slate-900/50 p-3 rounded-lg border border-slate-700/30">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-red-500/20 flex items-center justify-center">
                <Ambulance className="w-4 h-4 text-red-400" />
              </div>
              <div>
                <div className="text-sm font-bold text-slate-200">Ambulance 3</div>
                <div className="text-xs text-slate-400">→ Zone 6</div>
              </div>
            </div>
            <div className="text-xs font-mono font-bold text-slate-300">
              ETA 6 min
            </div>
          </div>

          {/* Mock Assignment 2 */}
          <div className="flex items-center justify-between bg-slate-900/50 p-3 rounded-lg border border-slate-700/30">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-purple-500/20 flex items-center justify-center">
                <Users className="w-4 h-4 text-purple-400" />
              </div>
              <div>
                <div className="text-sm font-bold text-slate-200">Volunteer Team B</div>
                <div className="text-xs text-slate-400">→ Zone 6</div>
              </div>
            </div>
            <div className="text-xs font-mono font-bold text-slate-300">
              ETA 8 min
            </div>
          </div>

          {/* Mock Assignment 3 */}
          <div className="flex items-center justify-between bg-slate-900/50 p-3 rounded-lg border border-slate-700/30">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-blue-500/20 flex items-center justify-center">
                <Droplets className="w-4 h-4 text-blue-400" />
              </div>
              <div>
                <div className="text-sm font-bold text-slate-200">Water Tanker 2</div>
                <div className="text-xs text-slate-400">→ Zone 6</div>
              </div>
            </div>
            <div className="text-xs font-mono font-bold text-slate-300">
              ETA 10 min
            </div>
          </div>
        </div>

        <button className="w-full mt-4 bg-orange-600 hover:bg-orange-500 text-white font-bold py-3 rounded-lg transition-colors shadow-lg shadow-orange-900/20 text-sm tracking-wider uppercase">
          {t('simulate_scenario')}
        </button>
      </div>
    </div>
  );
}
