"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Check, Loader2, Sparkles } from "lucide-react";
import { ContextBridgeLogo } from "@/components/contextbridge-logo";

const STAGES = [
  { id: "upload", label: "Video uploaded" },
  { id: "audio", label: "Audio extracted" },
  { id: "understanding", label: "Understanding the lesson" },
  { id: "chapters", label: "Creating chapters" },
  { id: "indexing", label: "Indexing important moments" },
  { id: "ready", label: "Preparing your learning workspace" },
];

/** Rotating, human-sounding status lines shown under the stages. */
const STATUS_LINES = [
  "Understanding the lesson…",
  "Finding the important moments…",
  "Creating chapters…",
  "Building your lesson map…",
  "Almost ready…",
];

export function AnalysisProgress({
  title,
  onComplete,
  isReady = true,
}: {
  title: string;
  /** Called when the final stage completes — parent navigates to the workspace. */
  onComplete: () => void;
  /** If false, holds before completing the final stage until ready (A7, D-08). */
  isReady?: boolean;
}) {
  const [elapsed, setElapsed] = useState(0);
  const [statusLine, setStatusLine] = useState(0);

  // Timer for elapsed seconds.
  useEffect(() => {
    const timer = setInterval(() => {
      setElapsed((s) => s + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Stage highlighting is DERIVED during render from elapsed time (A7, D-08)
  // instead of a setState-in-effect — fixes react-hooks/set-state-in-effect
  // while keeping the exact cadence and the "hold at 4 until ready" gate (D-33).
  // Cadence:
  // 0: 0s  - Video uploaded
  // 1: 2s  - Audio extracted
  // 2: 5s  - Understanding the lesson
  // 3: 8s  - Creating chapters
  // 4: 12s - Indexing important moments
  // 5: 16s - Preparing your learning workspace (held at 4 until ready)
  const stageIndex = (() => {
    if (elapsed >= 16) return isReady ? 5 : 4;
    if (elapsed >= 12) return 4;
    if (elapsed >= 8) return 3;
    if (elapsed >= 5) return 2;
    if (elapsed >= 2) return 1;
    return 0;
  })();

  // Rotating status lines.
  useEffect(() => {
    const statusTimer = setInterval(
      () => setStatusLine((s) => (s + 1) % STATUS_LINES.length),
      2200,
    );
    return () => clearInterval(statusTimer);
  }, []);

  useEffect(() => {
    if (stageIndex >= STAGES.length - 1 && isReady) {
      const done = setTimeout(onComplete, 1200);
      return () => clearTimeout(done);
    }
  }, [stageIndex, isReady, onComplete]);

  const minutes = Math.floor(elapsed / 60);
  const seconds = String(elapsed % 60).padStart(2, "0");

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="mx-auto flex max-w-lg flex-col items-center gap-6 rounded-3xl border border-white/[0.08] bg-[#0D1322] px-6 py-10 text-center shadow-2xl shadow-black/40 sm:px-10"
      role="status"
      aria-label="Analyzing your video"
    >
      <motion.div
        animate={{ rotate: [0, 6, -6, 0] }}
        transition={{ repeat: Infinity, duration: 3.2, ease: "easeInOut" }}
      >
        <ContextBridgeLogo size={44} />
      </motion.div>

      <div>
        <h2 className="text-lg font-semibold text-white">
          Understanding your lesson
        </h2>
        <p className="mt-1 truncate text-sm text-slate-400" title={title}>
          {title}
        </p>
        <p
          className="mt-2 text-xs font-medium text-violet-300/80"
          aria-live="polite"
        >
          Analyzing… {minutes}:{seconds} — usually under two minutes
        </p>
      </div>

      <ol className="w-full space-y-2.5 text-left" aria-label="Analysis stages">
        {STAGES.map((stage, i) => {
          const done = i < stageIndex;
          const active = i === stageIndex;
          return (
            <li
              key={stage.id}
              className={`flex items-center gap-3 rounded-xl border px-3.5 py-2.5 text-sm transition-colors duration-300 ${
                done
                  ? "border-emerald-400/15 bg-emerald-500/[0.06]"
                  : active
                    ? "border-violet-400/25 bg-violet-500/[0.08]"
                    : "border-white/[0.05] bg-white/[0.02] opacity-45"
              }`}
            >
              <span className="flex size-5 shrink-0 items-center justify-center">
                {done ? (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 400, damping: 18 }}
                  >
                    <Check className="size-4 text-emerald-400" aria-hidden="true" />
                  </motion.span>
                ) : active ? (
                  <Loader2
                    className="size-4 animate-spin text-violet-300"
                    aria-hidden="true"
                  />
                ) : (
                  <span className="size-1.5 rounded-full bg-slate-600" aria-hidden="true" />
                )}
              </span>
              <span
                className={
                  done
                    ? "text-slate-300"
                    : active
                      ? "text-white"
                      : "text-slate-500"
                }
              >
                {stage.label}
              </span>
              {active && (
                <Sparkles
                  className="ml-auto size-3.5 text-violet-300/70"
                  aria-hidden="true"
                />
              )}
              <span className="sr-only">
                {done ? "completed" : active ? "in progress" : "pending"}
              </span>
            </li>
          );
        })}
      </ol>

      <div className="h-5 overflow-hidden" aria-hidden="true">
        <AnimatePresence mode="wait">
          <motion.p
            key={statusLine}
            initial={{ y: 14, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -14, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="text-xs text-slate-500"
          >
            {STATUS_LINES[statusLine]}
          </motion.p>
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
