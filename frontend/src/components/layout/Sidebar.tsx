import { useTranslation } from 'react-i18next';
import { 
  LayoutDashboard, 
  Map, 
  BellRing, 
  Ambulance, 
  ActivitySquare, 
  CheckSquare, 
  FileText, 
  Settings 
} from 'lucide-react';

const navItems = [
  { id: 'dashboard', icon: LayoutDashboard },
  { id: 'digital_twin', icon: Map },
  { id: 'alerts', icon: BellRing },
  { id: 'resources', icon: Ambulance },
  { id: 'what_if_simulation', icon: ActivitySquare },
  { id: 'approvals', icon: CheckSquare },
  { id: 'reports', icon: FileText },
  { id: 'settings', icon: Settings },
];

export default function Sidebar() {
  const { t } = useTranslation();

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-full shrink-0">
      <div className="p-6 flex items-center gap-3 border-b border-slate-800">
        <div className="w-8 h-8 rounded bg-orange-500 flex items-center justify-center">
          <Map className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-white leading-tight">VARI OS</h1>
        </div>
      </div>
      
      <nav className="flex-1 py-4 overflow-y-auto">
        <ul className="space-y-1 px-3">
          {navItems.map((item) => (
            <li key={item.id}>
              <a 
                href="#"
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                  item.id === 'dashboard' 
                    ? 'bg-slate-800 text-orange-400' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium text-sm">{t(item.id)}</span>
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
