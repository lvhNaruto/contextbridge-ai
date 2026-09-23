"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "motion/react";
import { GraduationCap, LifeBuoy, Library, Sparkles } from "lucide-react";
import {
  ContextBridgeLogo,
  ContextBridgeWordmark,
} from "@/components/contextbridge-logo";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/", label: "Learn", icon: Sparkles },
  { href: "/library", label: "My lessons", icon: Library },
  { href: "/accessibility", label: "Accessibility", icon: GraduationCap },
  { href: "/help", label: "Help", icon: LifeBuoy },
];

export function TopNav({ className }: { className?: string }) {
  const pathname = usePathname();

  return (
    <header
      className={cn(
        "sticky top-0 z-40 border-b border-white/[0.06] bg-[#070B14]/80 backdrop-blur-xl",
        className,
      )}
    >
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link
          href="/"
          className="flex items-center gap-2.5 rounded-lg outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70"
          aria-label="ContextBridge home"
        >
          <ContextBridgeLogo size={26} />
          <ContextBridgeWordmark className="hidden sm:inline" />
        </Link>

        <nav aria-label="Main navigation" className="flex items-center gap-1">
          {NAV_ITEMS.map((item) => {
            const active =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "relative rounded-full px-3 py-1.5 text-sm transition-colors outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70 sm:px-3.5",
                  active
                    ? "text-white"
                    : "text-slate-400 hover:text-slate-200",
                )}
              >
                {active && (
                  <motion.span
                    layoutId="nav-pill"
                    className="absolute inset-0 rounded-full bg-white/[0.08] ring-1 ring-white/10"
                    transition={{ type: "spring", stiffness: 400, damping: 32 }}
                  />
                )}
                <span className="relative">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <Link
          href="/#upload"
          className="hidden sm:inline-flex h-8 items-center justify-center gap-2 whitespace-nowrap rounded-full border border-white/10 bg-white/[0.06] px-3.5 text-xs font-medium text-slate-100 transition-all outline-none hover:bg-white/[0.1] hover:border-white/20 focus-visible:ring-2 focus-visible:ring-violet-400/70"
        >
          Upload a video
        </Link>
      </div>
    </header>
  );
}
