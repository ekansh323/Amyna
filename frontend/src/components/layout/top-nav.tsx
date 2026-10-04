"use client";

import { Search, Moon, LogOut } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useRouter } from "next/navigation";

interface TopNavProps {
  sidebarWidth: number;
}

export function TopNav({ sidebarWidth }: TopNavProps) {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("aegis_token");
    router.push("/login");
  };

  return (
    <header
      className="fixed top-0 right-0 z-30 flex h-14 items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-md"
      style={{ left: sidebarWidth }}
    >
      {/* Search */}
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search projects, investigations..."
          className="h-9 bg-secondary/50 pl-9 text-sm border-none focus-visible:ring-1 focus-visible:ring-ring"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground">
          <Moon className="h-4 w-4" />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Avatar className="h-8 w-8 border border-border cursor-pointer transition-opacity hover:opacity-80">
              <AvatarFallback className="bg-primary/20 text-xs text-primary">
                E
              </AvatarFallback>
            </Avatar>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout} className="text-destructive cursor-pointer">
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
