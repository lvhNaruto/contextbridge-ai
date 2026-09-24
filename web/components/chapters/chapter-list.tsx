"use client";

import { motion } from "motion/react";
import { Play } from "lucide-react";
import { cn, formatTime } from "@/lib/utils";
import { ConfidenceBadge } from "@/components/evidence/evidence-badge";
import type { Chapter } from "@/types";

interface ChapterListProps {
  chapters: Chapter[];
  activeChapterId: string | null;
  onSelect: (chapter: Chapter) => void;
}

export function ChapterList({
  chapters,
  activeChapterId,
  onSelect,
}: ChapterListProps) {
  return (
    <ol className="flex flex-col gap-2" aria-label="Chapters in this video">
      {chapters.map((chapter) => {
        const active = chapter.id === activeChapterId;
        return (
          <li key={chapter.id}>
            <button
              onClick={() => onSelect(chapter)}
              aria-current={active ? "true" : undefined}
              aria-label={`Jump to ${chapter.title}, starts at ${formatTime(chapter.startSeconds)}`}
              className={cn(
                "group relative flex w-full items-start gap-3 rounded-xl border p-3 text-left outline-none transition-all duration-200 focus-visible:ring-2 focus-visible:ring-violet-400/70",
                active
                  ? "border-violet-400/40 bg-violet-500/[0.1]"
                  : "border-white/[0.06] bg-white/[0.02] hover:border-white/[0.14] hover:bg-white/[0.05]",
              )}
            >
              {/* Thumbnail placeholder */}
              <span
                aria-hidden="true"
                className={cn(
                  "relative flex aspect-video w-20 shrink-0 items-center justify-center overflow-hidden rounded-lg border transition-colors",
                  active
                    ? "border-violet-400/40 bg-gradient-to-br from-violet-500/25 to-violet-500/5"
                    : "border-white/[0.07] bg-gradient-to-br from-white/[0.06] to-transparent",
                )}
              >
                <Play
                  className={cn(
                    "size-4 transition-all",
                    active
                      ? "text-violet-300 opacity-100"
                      : "text-slate-500 opacity-60 group-hover:opacity-100",
                  )}
                />
                {active && (
                  <motion.span
                    layoutId="chapter-playing"
                    className="absolute bottom-1 right-1 flex items-center gap-1 rounded bg-violet-500 px-1 py-0.5 text-[9px] font-semibold text-white"
                  >
                    <span className="size-1 animate-pulse rounded-full bg-white" />
                    Now
                  </motion.span>
                )}
              </span>

              <span className="min-w-0 flex-1">
                <span className="flex items-center gap-2">
                  <span
                    className={cn(
                      "font-mono text-[11px] font-semibold tabular-nums",
                      active ? "text-violet-300" : "text-slate-500",
                    )}
                  >
                    {formatTime(chapter.startSeconds)}
                  </span>
                  <span
                    className={cn(
                      "truncate text-sm font-medium",
                      active ? "text-white" : "text-slate-200",
                    )}
                  >
                    {chapter.title}
                  </span>
                  {chapter.confidence != null && (
                    <span className="ml-auto shrink-0">
                      <ConfidenceBadge confidence={chapter.confidence} />
                    </span>
                  )}
                </span>
                <span className="mt-1 line-clamp-2 block text-xs leading-relaxed text-slate-500">
                  {chapter.description}
                </span>
              </span>

              {/* Active edge indicator */}
              {active && (
                <motion.span
                  layoutId="chapter-edge"
                  className="absolute inset-y-2 left-0 w-[3px] rounded-full bg-violet-400"
                  transition={{ type: "spring", stiffness: 380, damping: 30 }}
                />
              )}
            </button>
          </li>
        );
      })}
    </ol>
  );
}
