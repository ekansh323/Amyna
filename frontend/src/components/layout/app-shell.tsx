"use client";

import { useSidebar } from "@/hooks/use-sidebar";
import { Sidebar } from "./sidebar";
import { TopNav } from "./top-nav";
import { AuthGuard } from "@/components/auth/auth-guard";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { collapsed, toggle } = useSidebar();
  const sidebarWidth = collapsed ? 64 : 220;

  return (
    <AuthGuard>
      <div className="min-h-screen bg-background">
        <Sidebar collapsed={collapsed} onToggle={toggle} />
        <TopNav sidebarWidth={sidebarWidth} />
        <main
          className="pt-14 transition-[margin-left] duration-200"
          style={{ marginLeft: sidebarWidth }}
        >
          <div className="mx-auto max-w-7xl px-6 py-8">{children}</div>
        </main>
      </div>
    </AuthGuard>
  );
}
