"use client";

import * as React from "react";
import { Compass } from "lucide-react";
import { cn } from "@/lib/utils";
import type { WebSource } from "@/types";
import { WebSourceCard } from "@/components/evidence/web-source-card";

interface BoundaryCardProps {
  children?: React.ReactNode;
  sources?: WebSource[];
  className?: string;
}

/**
 * A10 — BoundaryCard Component (D-26, Week 2 Task 2.3).
 * Pillar P3 (Boundary Honesty): Frames external web research clearly
 * so students always know they have stepped beyond the video.
 * Video answers NEVER render this container.
 */
export function BoundaryCard({
  children,
  sources,
  className,
}: BoundaryCardProps) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-sky-400/30 bg-sky-950/20 p-4 transition-all duration-200 shadow-sm shadow-sky-950/40",
        className,
      )}
      aria-label="External web research boundary"
    >
      <div className="mb-3 flex items-center justify-between gap-2 border-b border-sky-400/15 pb-2.5">
        <div className="flex items-center gap-2 text-xs font-semibold text-sky-300">
          <Compass className="size-4 text-sky-400 shrink-0" aria-hidden="true" />
          <span>You&apos;ve stepped beyond this video</span>
        </div>
        <span className="text-[11px] font-medium text-sky-400/80">
          External research · Real sources
        </span>
      </div>

      {children && (
        <div className="text-[15px] leading-relaxed text-slate-200">
          {children}
        </div>
      )}

      {sources && sources.length > 0 && (
        <div
          className="mt-3.5 grid gap-2 sm:grid-cols-2"
          aria-label="External sources"
        >
          {sources.map((source) => (
            <WebSourceCard key={source.url} source={source} />
          ))}
        </div>
      )}
    </div>
  );
}
