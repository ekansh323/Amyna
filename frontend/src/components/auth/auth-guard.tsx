"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Shield } from "lucide-react";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("aegis_token");
    if (!token) {
      router.push("/login");
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  // Show a loading screen while checking auth
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative flex h-12 w-12 items-center justify-center rounded-xl bg-primary/20 animate-pulse">
            <Shield className="h-6 w-6 text-primary" />
          </div>
          <p className="text-sm text-muted-foreground animate-pulse">Loading secure environment...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
