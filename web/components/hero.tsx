"use client";

import { useEffect, useRef } from "react";
import { motion, useReducedMotion } from "motion/react";
import { ArrowDown, ArrowRight, BookOpenCheck, ShieldCheck, Sparkles } from "lucide-react";
import Link from "next/link";
import { DEMO_LESSON } from "@/lib/mock-data";

/** The landing hero follows the Design Arena visual direction without showing
 * fabricated lesson content. Its actions lead into the real upload and demo flows. */
export function Hero() {
  const reduce = useReducedMotion();
  const previewRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = previewRef.current;
    if (!video) return;
    const start = () => {
      if (video.currentTime < 1) video.currentTime = 8;
      if (reduce) {
        video.pause();
        return;
      }
      void video.play().catch(() => {});
    };
    if (video.readyState >= 1) start();
    else video.addEventListener("loadedmetadata", start, { once: true });
    return () => video.removeEventListener("loadedmetadata", start);
  }, [reduce]);

  return (
    <section className="arena-hero relative mx-auto max-w-7xl px-4 pb-14 pt-24 text-center sm:px-6 sm:pt-32 lg:pt-36">
      <div className="relative z-10 mx-auto max-w-5xl">
        <p className="arena-eyebrow mx-auto mb-7 w-fit">
          <span className="arena-pulse" aria-hidden="true" />
          The compass for self-learners
        </p>
        <h1 className="arena-title mb-5 text-[clamp(3.6rem,11vw,8.5rem)]">
          <span className="arena-gradient">ContextBridge</span>
        </h1>
        <p className="arena-serif mx-auto max-w-4xl text-[clamp(1.8rem,4.2vw,3rem)] leading-[1.08] text-white/90">
          Turn any educational video into a <span className="arena-violet">conversation.</span>
        </p>
        <p className="mx-auto mt-5 max-w-2xl text-sm leading-relaxed text-slate-300 sm:text-base">
          Ask the video directly, by text or voice. Get answers grounded in what it says, with a timestamp you can jump to and verify.
        </p>
        <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row" data-hero-cta>
          <a href="#upload" className="arena-button-primary inline-flex h-12 items-center justify-center gap-2 rounded-xl px-6 text-sm font-semibold">
            <Sparkles className="size-4" aria-hidden="true" /> Upload a video
          </a>
          <Link href="/lesson/demo-binary" className="arena-button-ghost inline-flex h-12 items-center justify-center gap-2 rounded-xl px-6 text-sm font-medium">
            Try the demo lesson <ArrowRight className="size-4" aria-hidden="true" />
          </Link>
        </div>
        <p className="mt-4 text-xs text-slate-500">Video answers with proof · clearly labeled web research · English and Hindi</p>
      </div>

      <motion.div
        className="arena-preview mx-auto mt-14 max-w-5xl text-left sm:mt-16"
        initial={reduce ? false : { opacity: 0, y: 28 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className="arena-preview-bar">
          <span className="flex gap-1.5" aria-hidden="true"><i className="arena-dot" /><i className="arena-dot" /><i className="arena-dot" /></span>
          <div className="min-w-0 flex-1 px-3 text-center">
            <p className="truncate text-[11px] font-medium tracking-wide text-slate-100 sm:text-xs">
              Context Bridge · Gemini lesson plan template · Google for Education
            </p>
            <p className="arena-live-label mt-0.5 truncate text-[10px] tracking-wide text-slate-500">
              Your video · your questions · your pace
            </p>
          </div>
          <BookOpenCheck className="size-4 text-emerald-300" aria-hidden="true" />
        </div>
        <div className="grid divide-y divide-white/[0.07] md:grid-cols-[1.1fr_0.9fr] md:divide-x md:divide-y-0">
          <motion.div
            className="arena-preview-media flex min-h-52 flex-col justify-between p-5 sm:min-h-64 sm:p-7"
            initial={reduce ? false : { opacity: 0, x: -16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.55, delay: 0.15 }}
          >
            <video
              ref={previewRef}
              className="arena-preview-video"
              src={DEMO_LESSON.videoUrl}
              muted
              playsInline
              loop
              preload="auto"
              aria-hidden="true"
            />
            <div className="arena-preview-scrim" aria-hidden="true" />
            <span className="w-fit rounded-lg border border-violet-300/20 bg-violet-400/10 px-2.5 py-1 text-[11px] font-medium text-violet-200">Your lesson map</span>
            <div>
              <div className="mb-3 text-xs text-slate-200">Chapters and transcript stay connected to playback.</div>
              <div className="h-1.5 overflow-hidden rounded-full bg-white/10"><div className="arena-progress-fill h-full rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-400" /></div>
              <div className="mt-2 flex justify-between font-mono text-[10px] text-slate-500"><span>00:00</span><span>Jump to cited moments</span></div>
            </div>
          </motion.div>
          <motion.div
            className="flex min-h-52 flex-col gap-3 p-5 sm:min-h-64 sm:p-7"
            initial={reduce ? false : { opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.55, delay: 0.22 }}
          >
            <div className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.12em] text-slate-500"><Sparkles className="size-3.5 text-violet-300" aria-hidden="true" /> Grounded answers</div>
            <div className="arena-preview-card arena-float-a ml-auto max-w-[90%] rounded-xl p-3 text-xs leading-relaxed text-slate-200">Ask a question about the video in your own words.</div>
            <div className="arena-preview-card arena-float-b max-w-[95%] rounded-xl p-3 text-xs leading-relaxed text-slate-300"><p>Answers point back to the lesson, so you can check the moment for yourself.</p><span className="mt-2 inline-flex items-center gap-1.5 rounded-md border border-violet-300/20 bg-violet-400/10 px-2 py-1 text-[10px] font-medium text-violet-200"><ShieldCheck className="size-3" aria-hidden="true" /> Evidence from video</span></div>
            <div className="mt-auto flex items-center justify-between border-t border-white/[0.07] pt-3 text-[11px] text-slate-500"><span>Text or voice</span><ArrowDown className="size-3.5" aria-hidden="true" /></div>
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
