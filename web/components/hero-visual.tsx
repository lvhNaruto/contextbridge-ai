"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import {
  Play,
  ListVideo,
  MessageCircleQuestion,
  MapPin,
  Sparkles,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { formatTime } from "@/lib/utils";

const STEPS = [
  { id: "video", label: "Your lesson" },
  { id: "chapters", label: "AI chapters" },
  { id: "question", label: "You ask" },
  { id: "answer", label: "Grounded answer" },
  { id: "moment", label: "Exact moment" },
] as const;

const CHAPTER_CHIPS = [
  { t: 0, title: "Introduction" },
  { t: 173, title: "What is binary language?" },
  { t: 642, title: "Practical example" },
];

type StepId = (typeof STEPS)[number]["id"];

/**
 * The five-second product story: an auto-advancing loop showing
 * video → chapters → question → answer → exact moment.
 */
export function HeroVisual() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const timer = setInterval(() => setStep((s) => (s + 1) % STEPS.length), 2600);
    return () => clearInterval(timer);
  }, []);

  const current: StepId = STEPS[step].id;
  const fade = {
    initial: { opacity: 0, y: 10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -8 },
    transition: { duration: 0.35 },
  };

  return (
    <div
      role="img"
      aria-label="How ContextBridge works: your video becomes chapters, you ask a question, and the answer points to the exact moment in the video."
      className="relative mx-auto max-w-3xl"
    >
      <ol className="mb-5 flex items-center justify-center gap-1.5 sm:gap-2.5">
        {STEPS.map((s, i) => (
          <li key={s.id} className="flex items-center gap-1.5 sm:gap-2.5">
            <div className="flex flex-col items-center gap-1.5">
              <motion.div
                animate={{
                  scale: i === step ? 1 : 0.72,
                  backgroundColor:
                    i === step ? "rgba(139,92,246,1)" : "rgba(255,255,255,0.09)",
                  boxShadow:
                    i === step ? "0 0 18px rgba(139,92,246,0.45)" : "none",
                }}
                transition={{ type: "spring", stiffness: 320, damping: 22 }}
                className="flex size-7 items-center justify-center rounded-full"
              >
                {i === step && <Sparkles className="size-3.5 text-white" aria-hidden="true" />}
              </motion.div>
              <span
                className={`hidden text-[10px] font-medium sm:block ${
                  i === step ? "text-violet-300" : "text-slate-600"
                }`}
              >
                {s.label}
              </span>
            </div>
            {i < STEPS.length - 1 && (
              <div className="h-px w-3 bg-white/10 sm:w-6" aria-hidden="true" />
            )}
          </li>
        ))}
      </ol>

      <div className="rounded-2xl border border-white/[0.08] bg-[#0B1120]/90 p-4 shadow-2xl shadow-black/40 sm:p-5">
        <AnimatePresence mode="wait">
          {current === "video" && (
            <motion.div {...fade} key="video" className="flex aspect-[21/9] items-center justify-center rounded-xl border border-white/[0.07] bg-gradient-to-br from-[#141B2F] to-[#0E1526]">
              <div className="flex flex-col items-center gap-2 text-slate-500">
                <Play className="size-7" aria-hidden="true" />
                <span className="text-xs">An educational video, any length</span>
              </div>
            </motion.div>
          )}

          {current === "chapters" && (
            <motion.div {...fade} key="chapters" className="flex aspect-[21/9] flex-col justify-center gap-2 rounded-xl border border-white/[0.07] bg-[#10182B] p-4">
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <ListVideo className="size-4" aria-hidden="true" />
                In this video
              </div>
              {CHAPTER_CHIPS.map((c, i) => (
                <motion.div
                  key={c.title}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.15 + i * 0.18 }}
                  className="flex items-center gap-3 rounded-lg border border-white/[0.06] bg-white/[0.03] px-3 py-2"
                >
                  <span className="font-mono text-[11px] font-semibold text-violet-300">
                    {formatTime(c.t)}
                  </span>
                  <span className="truncate text-xs text-slate-300">{c.title}</span>
                </motion.div>
              ))}
            </motion.div>
          )}

          {current === "question" && (
            <motion.div {...fade} key="question" className="flex aspect-[21/9] items-center justify-center rounded-xl border border-white/[0.07] bg-[#10182B] px-6">
              <motion.div
                initial={{ boxShadow: "0 0 0 0 rgba(139,92,246,0)" }}
                animate={{ boxShadow: ["0 0 0 0 rgba(139,92,246,0.35)", "0 0 0 12px rgba(139,92,246,0)"] }}
                transition={{ repeat: Infinity, duration: 1.6 }}
                className="flex w-full max-w-md items-center gap-3 rounded-full bg-white py-2.5 pl-5 pr-2.5"
              >
                <MessageCircleQuestion className="size-4 shrink-0 text-slate-400" aria-hidden="true" />
                <motion.span
                  initial={{ width: 0 }}
                  animate={{ width: "auto" }}
                  transition={{ duration: 1.1, ease: "linear" }}
                  className="overflow-hidden whitespace-nowrap text-sm text-slate-800"
                >
                  What does binary language mean?
                </motion.span>
                <span className="ml-auto h-5 w-px animate-pulse bg-slate-400" aria-hidden="true" />
              </motion.div>
            </motion.div>
          )}

          {current === "answer" && (
            <motion.div {...fade} key="answer" className="flex aspect-[21/9] flex-col justify-center gap-3 rounded-xl border border-violet-400/20 bg-[#10182B] p-5">
              <p className="max-w-md text-sm leading-relaxed text-slate-200">
                Binary language is how computers represent information using only{" "}
                <strong className="text-white">0 and 1</strong>. The video introduces this at{" "}
                <span className="font-mono font-semibold text-violet-300">02:53</span>.
              </p>
              <div className="flex items-center gap-2">
                <Badge variant="video">From video</Badge>
                <Badge variant="confidence">High confidence</Badge>
              </div>
            </motion.div>
          )}

          {current === "moment" && (
            <motion.div {...fade} key="moment" className="flex aspect-[21/9] flex-col justify-center gap-4 rounded-xl border border-white/[0.07] bg-[#10182B] p-5">
              <div className="relative h-2 overflow-hidden rounded-full bg-white/[0.08]">
                <motion.div
                  initial={{ width: "0%" }}
                  animate={{ width: "20%" }}
                  transition={{ duration: 0.9, ease: "easeOut" }}
                  className="h-full rounded-full bg-violet-500"
                />
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.7, type: "spring", stiffness: 300 }}
                  className="absolute left-[20%] top-1/2 size-4 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-violet-500 shadow-[0_0_16px_rgba(139,92,246,0.8)]"
                />
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <motion.span
                  animate={{ scale: [1, 1.04, 1] }}
                  transition={{ repeat: Infinity, duration: 1.8 }}
                  className="inline-flex items-center gap-2 rounded-full bg-violet-600 px-4 py-1.5 text-xs font-medium text-white"
                >
                  <MapPin className="size-3.5" aria-hidden="true" />
                  Jump to 02:53
                </motion.span>
                <span className="text-xs text-slate-500">
                  The video seeks to the exact moment
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

