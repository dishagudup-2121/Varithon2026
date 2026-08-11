import { ReactNode } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="flex h-screen w-full bg-slate-900 overflow-hidden">
      <Sidebar />
      <div className="flex flex-col flex-1 h-full min-w-0">
        <Header />
        <main className="flex-1 overflow-auto bg-slate-900 p-4">
          {children}
        </main>
      </div>
    </div>
  );
}
