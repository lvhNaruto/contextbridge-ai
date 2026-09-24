"use client";

import { motion } from "motion/react";
import { AlertTriangle } from "lucide-react";
import { TimestampButton } from "@/components/evidence/timestamp-button";
import type { ContradictionPair } from "@/types";

interface ContradictionCardProps {
  contradictions?: ContradictionPair[];
  onJump: (seconds: number) => void;
}

/**
 * A1 · Contradiction findings card (P0-4 UI, DECISIONS D-02).
 * Surfaces conflicting statements found in the video analysis with clickable
 * timestamps for both moments. Shows both sides without picking a winner.
 */
export function ContradictionCard({
  contradictions,
  onJump,
}: ContradictionCardProps) {
  if (!contradictions || contradictions.length === 0) {
    return null;
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.04, type: "spring", stiffness: 240, damping: 26 }}
      aria-label="Contradiction findings"
      className="rounded-2xl border border-amber-500/20 bg-[#0D1322] p-4 sm:p-5 shadow-[0_4px_24px_-4px_rgba(245,158,11,0.08)]"
    >
      <div className="mb-3 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="flex size-7 items-center justify-center rounded-lg bg-amber-500/10 text-amber-400 ring-1 ring-amber-500/20">
            <AlertTriangle className="size-4" aria-hidden="true" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-amber-300">
              Contradiction Surfaced
            </h2>
            <p className="text-xs text-slate-400">
              Conflicting statements identified in this video — verify both moments below:
            </p>
          </div>
        </div>
        <span className="rounded-full border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 text-[11px] font-medium text-amber-300">
          {contradictions.length} {contradictions.length === 1 ? "pair" : "pairs"}
        </span>
      </div>

      <div className="space-y-4">
        {contradictions.map((pair) => (
          <div
            key={pair.id}
            className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-3.5"
          >
            <p className="text-xs font-medium text-slate-200">
              <span className="text-amber-400">Claim:</span> {pair.claim}
            </p>

            <div className="mt-3 grid gap-3 sm:grid-cols-2">
              {/* Statement A */}
              <div className="flex flex-col justify-between rounded-lg border border-white/[0.05] bg-[#0A0F1A] p-3">
                <div>
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                    Statement A
                  </span>
                  <blockquote className="mt-1.5 text-xs leading-relaxed text-slate-300 italic before:content-['“'] after:content-['”']">
                    {pair.statementA.quote || pair.statementA.text}
                  </blockquote>
                </div>
                <div className="mt-3 pt-2">
                  <TimestampButton
                    seconds={pair.statementA.startSeconds}
                    onJump={onJump}
                    size="sm"
                  />
                </div>
              </div>

              {/* Statement B */}
              <div className="flex flex-col justify-between rounded-lg border border-white/[0.05] bg-[#0A0F1A] p-3">
                <div>
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                    Statement B
                  </span>
                  <blockquote className="mt-1.5 text-xs leading-relaxed text-slate-300 italic before:content-['“'] after:content-['”']">
                    {pair.statementB.quote || pair.statementB.text}
                  </blockquote>
                </div>
                <div className="mt-3 pt-2">
                  <TimestampButton
                    seconds={pair.statementB.startSeconds}
                    onJump={onJump}
                    size="sm"
                  />
                </div>
              </div>
            </div>

            {pair.note && (
              <p className="mt-2.5 text-[11px] text-amber-200/70 italic">
                Note: {pair.note}
              </p>
            )}
          </div>
        ))}
      </div>
    </motion.section>
  );
}
