import { useTranslation } from 'react-i18next';
import { Bell, UserCircle2 } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function Header() {
  const { t, i18n } = useTranslation();
  const [time, setTime] = useState('');

  useEffect(() => {
    const updateTime = () => setTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center gap-4">
        <span className="text-slate-400 text-sm">{t('app_subtitle')}</span>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 bg-slate-800 rounded-full px-3 py-1">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-xs font-medium text-slate-300 uppercase tracking-wider">{t('live')}</span>
          <span className="text-xs font-mono text-slate-400 ml-2">{time}</span>
        </div>

        <div className="flex bg-slate-800 rounded-lg p-1">
          <button 
            className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${i18n.language === 'en' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:text-white'}`}
            onClick={() => i18n.changeLanguage('en')}
          >
            English
          </button>
          <button 
            className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${i18n.language === 'mr' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:text-white'}`}
            onClick={() => i18n.changeLanguage('mr')}
          >
            मराठी
          </button>
        </div>

        <button className="relative text-slate-400 hover:text-white transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
            3
          </span>
        </button>

        <div className="flex items-center gap-3 pl-4 border-l border-slate-800">
          <UserCircle2 className="w-8 h-8 text-slate-400" />
          <div className="flex flex-col">
            <span className="text-sm font-medium text-slate-200 leading-none">Control Officer</span>
            <span className="text-xs text-slate-500 mt-1 leading-none">Admin</span>
          </div>
        </div>
      </div>
    </header>
  );
}
