"use client";

import { Compass, ArrowRight } from "lucide-react";

interface ExploreSuggestionsProps {
  suggestions?: string[];
  onSelect?: (question: string) => void;
}

/**
 * A9 — ExploreSuggestions Component (D-25, Week 2 Task 2.2).
 * Renders 2–3 clickable chips labeled "Explore from here →" derived
 * directly from the video's own concepts.
 */
export function ExploreSuggestions({
  suggestions,
  onSelect,
}: ExploreSuggestionsProps) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="mt-3 flex flex-col gap-2 border-t border-white/[0.04] pt-2.5" aria-label="Explore from here">
      <div className="flex items-center gap-1.5 text-[11px] font-medium text-violet-300/80">
        <Compass className="size-3 text-violet-400" aria-hidden="true" />
        <span>Explore from here</span>
      </div>
      <div className="flex flex-wrap gap-1.5">
        {suggestions.map((item, idx) => (
          <button
            key={`${item}-${idx}`}
            type="button"
            onClick={() => onSelect?.(item)}
            className="group inline-flex items-center gap-1.5 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs text-violet-200 transition-all duration-150 hover:border-violet-400/50 hover:bg-violet-500/20 hover:text-white focus-visible:ring-2 focus-visible:ring-violet-400/70"
          >
            <span>{item}</span>
            <ArrowRight
              className="size-2.5 text-violet-400 opacity-60 transition-transform group-hover:translate-x-0.5 group-hover:opacity-100"
              aria-hidden="true"
            />
          </button>
        ))}
      </div>
    </div>
  );
}
