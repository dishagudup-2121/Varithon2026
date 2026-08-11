import { ReactNode } from 'react';

type StatusType = 'critical' | 'high' | 'medium' | 'low' | 'active' | 'available' | 'closed';

interface StatusBadgeProps {
  status: StatusType;
  children: ReactNode;
  className?: string;
}

export default function StatusBadge({ status, children, className = '' }: StatusBadgeProps) {
  const styles: Record<StatusType, string> = {
    critical: 'bg-red-500/20 text-red-400 border-red-500/30',
    high: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
    medium: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    low: 'bg-green-500/20 text-green-400 border-green-500/30',
    active: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    available: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    closed: 'bg-slate-500/20 text-slate-400 border-slate-500/30 line-through',
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${styles[status]} ${className}`}>
      {children}
    </span>
  );
}
