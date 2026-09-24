"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import Link from "next/link";
import { HeroVisual } from "@/components/hero-visual";

/**
 * Landing hero. GSAP drives the cinematic entrance only —
 * everything else in the product uses Motion.
 */
export function Hero() {
  const root = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    if (reduceMotion || !root.current) return;

    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
      tl.fromTo(
        "[data-hero-badge]",
        { y: 16, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5 },
      )
        .fromTo(
          "[data-hero-line]",
          { y: 28, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.7, stagger: 0.12 },
          "-=0.2",
        )
        .fromTo(
          "[data-hero-cta] > *",
          { y: 14, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.45, stagger: 0.08 },
          "-=0.35",
        )
        .fromTo(
          "[data-hero-visual]",
          { y: 24, opacity: 0, scale: 0.98 },
          { y: 0, opacity: 1, scale: 1, duration: 0.8 },
          "-=0.4",
        );
    }, root);
    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={root}
      className="relative mx-auto max-w-6xl px-4 pb-10 pt-16 sm:px-6 sm:pt-20"
    >
      {/* Subtle ambient depth — one restrained radial, no particles */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 -top-24 mx-auto h-[420px] max-w-3xl rounded-full bg-violet-600/[0.13] blur-[120px]"
      />

      <div className="relative flex flex-col items-center text-center">
        <span
          data-hero-badge
          className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-500/10 px-3.5 py-1.5 text-xs font-medium text-violet-300"
        >
          <span className="size-1.5 rounded-full bg-violet-400" aria-hidden="true" />
          The Compass for Self-Learners
        </span>

        <h1 className="max-w-3xl text-balance text-4xl font-semibold tracking-tight text-white sm:text-5xl md:text-[3.4rem] md:leading-[1.1]">
          <span data-hero-line className="block">
            Not a tutor.
          </span>
          <span data-hero-line className="block">
            A{" "}
            <span className="bg-gradient-to-r from-violet-300 to-violet-400 bg-clip-text text-transparent">
              compass
            </span>{" "}
            for self-learners.
          </span>
        </h1>

        <p
          data-hero-line
          className="mt-5 max-w-2xl text-pretty text-base leading-relaxed text-slate-300 sm:text-lg"
        >
          Every answer anchored to the video you chose, in your language, with proof, and honest about where the video ends.
        </p>

        {/* 3 Pillars badges */}
        <div data-hero-line className="mt-5 flex flex-wrap items-center justify-center gap-2 text-xs">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 font-medium text-emerald-300">
            <span>⚓</span> Anchored to Video
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 font-medium text-violet-300">
            <span>🔍</span> Clickable Proof
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-sky-500/20 bg-sky-500/10 px-3 py-1 font-medium text-sky-300">
            <span>🛡️</span> Boundary Honesty
          </span>
        </div>

        <div data-hero-cta className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/lesson/demo-binary"
            className="inline-flex h-12 items-center justify-center gap-2 whitespace-nowrap rounded-full bg-violet-600 px-7 text-base font-medium text-white shadow-[0_8px_24px_-8px_rgba(139,92,246,0.6)] outline-none transition-all hover:bg-violet-500 focus-visible:ring-2 focus-visible:ring-violet-400/70 focus-visible:ring-offset-2 focus-visible:ring-offset-[#070B14]"
          >
            Explore Tokyo Night Demo →
          </Link>
          <a
            href="#upload"
            className="inline-flex h-12 items-center justify-center gap-2 whitespace-nowrap rounded-full border border-white/10 bg-white/[0.06] px-7 text-base font-medium text-slate-100 outline-none transition-all hover:bg-white/[0.1] hover:border-white/20 focus-visible:ring-2 focus-visible:ring-violet-400/70 focus-visible:ring-offset-2 focus-visible:ring-offset-[#070B14]"
          >
            Upload your video
          </a>
        </div>

        <p data-hero-line className="mt-4 text-xs text-slate-500">
          Ask questions, seek to the exact moment with proof, or step beyond with verified web research.
        </p>
      </div>

      <div data-hero-visual className="relative mt-14 sm:mt-16">
        <HeroVisual />
      </div>
    </section>
  );
}
