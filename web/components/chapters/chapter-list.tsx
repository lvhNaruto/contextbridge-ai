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
      {chapters.map((chapter, index) => {
        const active = chapter.id === activeChapterId;
        return (
          <li key={chapter.id}>
            <button
              type="button"
              onClick={() => onSelect(chapter)}
              aria-current={active ? "true" : undefined}
              aria-label={`Jump to ${chapter.title}, starts at ${formatTime(chapter.startSeconds)}`}
              className={cn(
                "group relative flex w-full items-start gap-3 rounded-xl border p-2.5 text-left outline-none transition-all duration-200 focus-visible:ring-2 focus-visible:ring-sky-400/70",
                active
                  ? "border-sky-500/40 bg-sky-500/[0.1] shadow-inner"
                  : "border-white/[0.05] bg-white/[0.02] hover:border-white/[0.14] hover:bg-white/[0.05]",
              )}
            >
              {/* Thumbnail placeholder matching YouTube */}
              <span
                aria-hidden="true"
                className={cn(
                  "relative flex aspect-video w-24 shrink-0 items-center justify-center overflow-hidden rounded-lg border transition-colors",
                  active
                    ? "border-sky-400/50 bg-gradient-to-br from-sky-500/30 to-blue-600/10"
                    : "border-white/[0.08] bg-gradient-to-br from-white/[0.06] to-white/[0.01] group-hover:border-white/[0.16]",
                )}
              >
                <Play
                  className={cn(
                    "size-4 transition-transform group-hover:scale-110",
                    active
                      ? "text-sky-300 opacity-100"
                      : "text-slate-400 opacity-70 group-hover:text-white group-hover:opacity-100",
                  )}
                />
                <span className="absolute top-1 left-1.5 font-mono text-[9px] font-bold text-white/50">
                  #{index + 1}
                </span>
                {active && (
                  <motion.span
                    layoutId="chapter-playing"
                    className="absolute bottom-1 right-1 flex items-center gap-1 rounded bg-sky-500 px-1 py-0.5 text-[8px] font-semibold text-white uppercase tracking-wider"
                  >
                    <span className="size-1 animate-pulse rounded-full bg-white" />
                    Now
                  </motion.span>
                )}
              </span>

              <span className="min-w-0 flex-1 flex flex-col justify-between self-stretch gap-1.5">
                <span
                  className={cn(
                    "text-xs font-semibold leading-snug line-clamp-2 transition-colors",
                    active ? "text-white" : "text-slate-200 group-hover:text-white",
                  )}
                >
                  {chapter.title}
                </span>

                <span className="flex items-center gap-2 flex-wrap">
                  <span
                    className={cn(
                      "inline-flex items-center rounded px-1.5 py-0.5 font-mono text-[11px] font-bold tabular-nums transition-colors",
                      active
                        ? "bg-sky-500/30 text-sky-200 border border-sky-400/40"
                        : "bg-sky-500/15 text-sky-400 border border-sky-500/25 group-hover:bg-sky-500/25",
                    )}
                  >
                    {formatTime(chapter.startSeconds)}
                  </span>

                  {chapter.confidence != null && (
                    <ConfidenceBadge confidence={chapter.confidence} />
                  )}
                </span>
              </span>

              {/* Active edge indicator */}
              {active && (
                <motion.span
                  layoutId="chapter-edge"
                  className="absolute inset-y-2 left-0 w-[3px] rounded-full bg-sky-400"
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
