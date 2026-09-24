"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Search, FileText, X } from "lucide-react";
import { cn, formatTime } from "@/lib/utils";
import type { TranscriptSegment } from "@/types";

interface TranscriptPanelProps {
  transcript: TranscriptSegment[];
  onJump: (seconds: number) => void;
  activeSeconds?: number | null;
}

/**
 * A2 · Searchable transcript panel (P0-3, DECISIONS D-03).
 * Client-side search over video transcript segments.
 * Clicking any segment seeks playback to that exact moment.
 */
export function TranscriptPanel({
  transcript,
  onJump,
  activeSeconds,
}: TranscriptPanelProps) {
  const [query, setQuery] = useState("");
  const segmentRefs = useRef(new Map<number, HTMLButtonElement>());

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return transcript;
    return transcript.filter(
      (seg) =>
        seg.text.toLowerCase().includes(q) ||
        formatTime(seg.startSeconds).includes(q),
    );
  }, [transcript, query]);

  useEffect(() => {
    if (activeSeconds == null) return;

    const activeSegment = filtered.find(
      (seg) =>
        activeSeconds >= seg.startSeconds && activeSeconds < seg.endSeconds,
    );
    if (activeSegment) {
      segmentRefs.current
        .get(activeSegment.startSeconds)
        ?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }, [activeSeconds, filtered]);

  if (!transcript || transcript.length === 0) {
    return (
      <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4 text-center text-xs text-slate-500">
        No transcript available for this video.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2.5" aria-label="Searchable transcript">
      {/* Search filter input */}
      <div className="relative">
        <Search
          className="pointer-events-none absolute left-3 top-1/2 size-3.5 -translate-y-1/2 text-slate-500"
          aria-hidden="true"
        />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search transcript..."
          aria-label="Filter transcript by keyword or timestamp"
          className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] py-2 pl-9 pr-8 text-xs text-slate-200 placeholder:text-slate-500 outline-none transition-colors focus:border-violet-400/50 focus:bg-white/[0.06] focus-visible:ring-2 focus-visible:ring-violet-400/70"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            aria-label="Clear search"
            className="absolute right-2.5 top-1/2 -translate-y-1/2 rounded p-0.5 text-slate-400 hover:text-slate-200"
          >
            <X className="size-3.5" aria-hidden="true" />
          </button>
        )}
      </div>

      {/* Segment row count indicator if searching */}
      {query && (
        <p className="px-1 text-[11px] text-slate-400">
          Showing {filtered.length} of {transcript.length} moments
        </p>
      )}

      {/* Segment list */}
      <div className="max-h-[340px] space-y-1.5 overflow-y-auto pr-1">
        {filtered.length === 0 ? (
          <div className="rounded-xl border border-white/[0.04] bg-white/[0.01] p-4 text-center text-xs text-slate-500">
            No lines match &ldquo;{query}&rdquo;
          </div>
        ) : (
          filtered.map((seg, idx) => {
            const isNearActive =
              activeSeconds != null &&
              activeSeconds >= seg.startSeconds &&
              activeSeconds < seg.endSeconds;

            return (
              <button
                key={`${seg.startSeconds}-${idx}`}
                ref={(element) => {
                  if (element) {
                    segmentRefs.current.set(seg.startSeconds, element);
                  } else {
                    segmentRefs.current.delete(seg.startSeconds);
                  }
                }}
                onClick={() => onJump(seg.startSeconds)}
                aria-label={`Jump to ${formatTime(seg.startSeconds)}: ${seg.text}`}
                className={cn(
                  "group relative flex w-full items-start gap-2.5 rounded-xl border p-2.5 text-left outline-none transition-all duration-200 focus-visible:ring-2 focus-visible:ring-violet-400/70",
                  isNearActive
                    ? "border-violet-400/40 bg-violet-500/[0.08]"
                    : "border-white/[0.05] bg-white/[0.02] hover:border-white/[0.12] hover:bg-white/[0.04]",
                )}
              >
                <span
                  className={cn(
                    "mt-0.5 shrink-0 font-mono text-[11px] font-semibold tabular-nums",
                    isNearActive ? "text-violet-300" : "text-violet-400/80 group-hover:text-violet-300",
                  )}
                >
                  {formatTime(seg.startSeconds)}
                </span>
                <span className="min-w-0 flex-1 text-xs leading-relaxed text-slate-300 group-hover:text-slate-100">
                  {seg.text}
                </span>
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}
