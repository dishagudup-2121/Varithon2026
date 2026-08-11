import { ReactNode } from 'react';

interface KpiCardProps {
  title: string;
  value: string | number;
  subValue?: string | ReactNode;
  subValueColor?: 'green' | 'red' | 'amber' | 'slate';
  className?: string;
}

export default function KpiCard({ title, value, subValue, subValueColor = 'slate', className = '' }: KpiCardProps) {
  const colorMap = {
    green: 'text-green-400',
    red: 'text-red-400',
    amber: 'text-amber-400',
    slate: 'text-slate-400',
  };

  return (
    <div className={`panel p-4 flex flex-col justify-between ${className}`}>
      <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">{title}</h3>
      <div className="text-3xl font-bold text-white mb-1">{value}</div>
      {subValue && (
        <div className={`text-xs font-medium ${colorMap[subValueColor]}`}>
          {subValue}
        </div>
      )}
    </div>
  );
}
