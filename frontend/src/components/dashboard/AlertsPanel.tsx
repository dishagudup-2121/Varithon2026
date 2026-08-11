import { useTranslation } from 'react-i18next';
import { AlertTriangle, Info, AlertCircle } from 'lucide-react';

interface Alert {
  id: string;
  zone: string;
  severity: 'critical' | 'high' | 'medium';
  title: string;
  description: string;
  time: string;
}

const mockAlerts: Alert[] = [
  {
    id: '1',
    zone: 'Zone 6',
    severity: 'critical',
    title: 'Critical Risk',
    description: 'Crowd density high & temperature rising',
    time: '10:22 AM'
  },
  {
    id: '2',
    zone: 'Zone 4',
    severity: 'high',
    title: 'High Risk',
    description: 'Congestion increasing rapidly',
    time: '10:18 AM'
  },
  {
    id: '3',
    zone: 'Zone 7',
    severity: 'high',
    title: 'High Risk',
    description: 'Water availability low',
    time: '10:15 AM'
  }
];

export default function AlertsPanel() {
  const { t } = useTranslation();

  const getIcon = (severity: string) => {
    switch(severity) {
      case 'critical': return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'high': return <AlertTriangle className="w-5 h-5 text-orange-500" />;
      default: return <Info className="w-5 h-5 text-amber-500" />;
    }
  };

  return (
    <div className="panel flex flex-col h-[280px]">
      <div className="panel-header flex justify-between items-center">
        <span>{t('active_alerts')}</span>
        <button className="text-[10px] text-slate-400 hover:text-white uppercase">{t('view_all')}</button>
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {mockAlerts.map(alert => (
          <div key={alert.id} className="bg-slate-900/50 rounded-lg p-3 border border-slate-700/30 flex gap-3 items-start">
            <div className="shrink-0 mt-0.5">
              {getIcon(alert.severity)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex justify-between items-start mb-1">
                <h4 className="text-sm font-bold text-slate-200">
                  {alert.zone} — {t(alert.severity === 'critical' ? 'critical' : 'high')}
                </h4>
                <span className="text-[10px] text-slate-500 whitespace-nowrap ml-2">{alert.time}</span>
              </div>
              <p className="text-xs text-slate-400 line-clamp-2">{alert.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
