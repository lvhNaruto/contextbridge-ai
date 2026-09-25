"use client";

import { useState } from "react";
import { motion } from "motion/react";
import {
  X,
  Play,
  Share2,
  RotateCcw,
  Check,
  ListVideo,
  FileText,
} from "lucide-react";
import { cn, formatTime } from "@/lib/utils";
import { ConfidenceBadge } from "@/components/evidence/evidence-badge";
import { TranscriptPanel } from "@/components/transcript/transcript-panel";
import type { Chapter, TranscriptSegment } from "@/types";

interface InThisVideoPanelProps {
  chapters: Chapter[];
  activeChapterId: string | null;
  onSelectChapter: (chapter: Chapter) => void;
  transcript: TranscriptSegment[];
  onJump: (seconds: number) => void;
  activeSeconds?: number | null;
  onClose?: () => void;
  className?: string;
}

export function InThisVideoPanel({
  chapters,
  activeChapterId,
  onSelectChapter,
  transcript,
  onJump,
  activeSeconds,
  onClose,
  className,
}: InThisVideoPanelProps) {
  const [activeTab, setActiveTab] = useState<"chapters" | "transcript">(
    chapters.length > 0 ? "chapters" : "transcript",
  );
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleCopyLink = (e: React.MouseEvent, chapter: Chapter) => {
    e.stopPropagation();
    if (typeof window === "undefined") return;
    const url = new URL(window.location.href);
    url.searchParams.set("t", String(Math.floor(chapter.startSeconds)));
    navigator.clipboard.writeText(url.toString()).then(() => {
      setCopiedId(chapter.id);
      setTimeout(() => setCopiedId(null), 2000);
    });
  };

  return (
    <div
      className={cn(
        "flex flex-col rounded-2xl border border-white/[0.08] bg-[#121620]/95 backdrop-blur-md shadow-2xl overflow-hidden",
        "h-[620px] max-h-[calc(100vh-140px)] min-h-[460px]",
        className,
      )}
      aria-label="In this video"
    >
      {/* Top Header matching YouTube */}
      <div className="flex items-center justify-between border-b border-white/[0.06] px-4 py-3 shrink-0">
        <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
          In this video
        </h2>
        {onClose && (
          <button
            onClick={onClose}
            aria-label="Close 'In this video' panel"
            className="rounded-lg p-1.5 text-slate-400 hover:bg-white/[0.08] hover:text-white transition-colors"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        )}
      </div>

      {/* Pill Switcher Tabs matching YouTube */}
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-white/[0.04] bg-white/[0.01] shrink-0">
        <button
          type="button"
          onClick={() => setActiveTab("chapters")}
          className={cn(
            "relative rounded-lg px-3 py-1.5 text-xs font-semibold transition-all duration-150 flex items-center gap-1.5",
            activeTab === "chapters"
              ? "bg-white text-slate-900 shadow-sm"
              : "bg-white/[0.06] text-slate-300 hover:bg-white/[0.1] hover:text-white",
          )}
        >
          <ListVideo className="size-3.5" />
          <span>Chapters</span>
          {chapters.length > 0 && (
            <span
              className={cn(
                "rounded px-1.5 py-0.2 text-[10px] font-mono",
                activeTab === "chapters"
                  ? "bg-slate-200 text-slate-800"
                  : "bg-white/[0.08] text-slate-400",
              )}
            >
              {chapters.length}
            </span>
          )}
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("transcript")}
          className={cn(
            "relative rounded-lg px-3 py-1.5 text-xs font-semibold transition-all duration-150 flex items-center gap-1.5",
            activeTab === "transcript"
              ? "bg-white text-slate-900 shadow-sm"
              : "bg-white/[0.06] text-slate-300 hover:bg-white/[0.1] hover:text-white",
          )}
        >
          <FileText className="size-3.5" />
          <span>Transcript</span>
          {transcript.length > 0 && (
            <span
              className={cn(
                "rounded px-1.5 py-0.2 text-[10px] font-mono",
                activeTab === "transcript"
                  ? "bg-slate-200 text-slate-800"
                  : "bg-white/[0.08] text-slate-400",
              )}
            >
              {transcript.length}
            </span>
          )}
        </button>
      </div>

      {/* Scrollable Container */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-white/20 hover:[&::-webkit-scrollbar-thumb]:bg-white/30 [&::-webkit-scrollbar-track]:bg-transparent">
        {activeTab === "chapters" ? (
          chapters.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-48 rounded-xl border border-white/[0.04] bg-white/[0.01] p-6 text-center text-xs text-slate-400">
              <ListVideo className="size-8 text-slate-600 mb-2" />
              <p>No chapters identified for this video.</p>
            </div>
          ) : (
            <ol className="flex flex-col gap-2" aria-label="Chapters in this video">
              {chapters.map((chapter, index) => {
                const active = chapter.id === activeChapterId;
                const isCopied = copiedId === chapter.id;

                return (
                  <li key={chapter.id}>
                    <button
                      type="button"
                      onClick={() => onSelectChapter(chapter)}
                      aria-current={active ? "true" : undefined}
                      aria-label={`Jump to ${chapter.title}, starts at ${formatTime(chapter.startSeconds)}`}
                      className={cn(
                        "group relative flex w-full items-start gap-3 rounded-xl border p-2.5 text-left outline-none transition-all duration-200 focus-visible:ring-2 focus-visible:ring-sky-400/70",
                        active
                          ? "border-sky-500/40 bg-sky-500/[0.1] shadow-inner"
                          : "border-white/[0.05] bg-white/[0.02] hover:border-white/[0.14] hover:bg-white/[0.05]",
                      )}
                    >
                      {/* Thumbnail frame on left */}
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

                      {/* Middle text content */}
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
                          {/* Blue pill timestamp badge matching screenshot */}
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

                      {/* Hover action icons on right matching screenshot */}
                      <span className="shrink-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <span
                          role="button"
                          tabIndex={0}
                          onClick={(e) => handleCopyLink(e, chapter)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") {
                              handleCopyLink(e as unknown as React.MouseEvent, chapter);
                            }
                          }}
                          aria-label="Copy timestamp link"
                          title="Copy link at this timestamp"
                          className="rounded-md p-1.5 text-slate-400 hover:bg-white/[0.1] hover:text-white transition-colors"
                        >
                          {isCopied ? (
                            <Check className="size-3.5 text-emerald-400" />
                          ) : (
                            <Share2 className="size-3.5" />
                          )}
                        </span>
                        <span
                          role="button"
                          tabIndex={0}
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectChapter(chapter);
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") {
                              e.stopPropagation();
                              onSelectChapter(chapter);
                            }
                          }}
                          aria-label="Replay chapter"
                          title="Play chapter from start"
                          className="rounded-md p-1.5 text-slate-400 hover:bg-white/[0.1] hover:text-white transition-colors"
                        >
                          <RotateCcw className="size-3.5" />
                        </span>
                      </span>

                      {/* Active indicator bar */}
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
          )
        ) : (
          <div className="h-full flex flex-col">
            <TranscriptPanel
              transcript={transcript}
              onJump={onJump}
              activeSeconds={activeSeconds}
              maxHeightClass="max-h-[calc(100vh-280px)] min-h-[380px]"
            />
          </div>
        )}
      </div>
    </div>
  );
}
