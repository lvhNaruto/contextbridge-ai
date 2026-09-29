"use client";

import * as React from "react";
import { Compass } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  lessonCopy,
  lessonUiLanguage,
  localizeSourceDescription,
} from "@/lib/lesson-copy";
import type { WebSource } from "@/types";
import { WebSourceCard } from "@/components/evidence/web-source-card";

interface BoundaryCardProps {
  children?: React.ReactNode;
  sources?: WebSource[];
  className?: string;
  /** Answer language (`hi` localizes the validity labels). */
  language?: string;
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
  language,
}: BoundaryCardProps) {
  const copy = lessonCopy(lessonUiLanguage(language));
  const localizedSources = sources?.map((source) => ({
    ...source,
    description: localizeSourceDescription(
      source.description,
      lessonUiLanguage(language),
    ),
  }));

  return (
    <div
      className={cn(
        "min-w-0 rounded-2xl border border-sky-400/30 bg-sky-950/20 p-4 transition-all duration-200 shadow-sm shadow-sky-950/40",
        className,
      )}
      aria-label={copy.boundaryLabel}
    >
      <div className="mb-3 flex min-w-0 flex-col gap-1.5 border-b border-sky-400/15 pb-2.5">
        <div className="flex min-w-0 items-start gap-2 text-sm font-semibold leading-snug text-sky-100">
          <Compass className="mt-0.5 size-4 shrink-0 text-sky-300" aria-hidden="true" />
          <span className="min-w-0 break-words">{copy.steppedBeyond}</span>
        </div>
        <span className="break-words text-xs font-medium leading-snug text-sky-200">
          {copy.realSources}
        </span>
      </div>

      {children && (
        <div className="text-[15px] leading-relaxed text-slate-200">
          {children}
        </div>
      )}

      {localizedSources && localizedSources.length > 0 && (
        <div
          className="mt-3.5 grid gap-2"
          aria-label={copy.sourcesLabel}
        >
          {localizedSources.map((source) => (
            <WebSourceCard key={source.url} source={source} />
          ))}
        </div>
      )}
    </div>
  );
}
