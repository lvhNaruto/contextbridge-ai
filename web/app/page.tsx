"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "motion/react";
import Link from "next/link";
import { Sparkles, ShieldCheck, Clock3, MessageCircleQuestion, Target, UploadCloud, Captions, Globe2, AudioLines, ScanSearch, ArrowRight } from "lucide-react";
import { toast } from "sonner";
import { TopNav } from "@/components/top-nav";
import { Hero } from "@/components/hero";
import { UploadDropzone } from "@/components/upload/upload-dropzone";
import { AnalysisProgress } from "@/components/upload/analysis-progress";
import { DEMO_LESSON } from "@/lib/mock-data";
import { saveLessonMeta, listSavedLessons } from "@/lib/store";
import type { Lesson } from "@/types";

export default function LearnPage() {
  const router = useRouter();
  const [analyzing, setAnalyzing] = useState<Lesson | null>(null);

  const handleAnalyzed = useCallback((lesson: Lesson) => {
    // Persist the lesson so "My lessons" can restore it.
    saveLessonMeta({
      id: lesson.id,
      title: lesson.title,
      createdAt: lesson.createdAt,
      chapterCount: lesson.chapters.length,
      language: lesson.language,
      source: lesson.id === DEMO_LESSON.id ? "demo" : "upload",
    });
    setAnalyzing(lesson);
  }, []);

  const handleAnalysisComplete = useCallback(() => {
    if (analyzing) router.push(`/lesson/${analyzing.id}`);
  }, [analyzing, router]);

  const handleDemo = useCallback(() => {
    const exists = listSavedLessons().some((m) => m.id === DEMO_LESSON.id);
    if (!exists) {
      saveLessonMeta({
        id: DEMO_LESSON.id,
        title: DEMO_LESSON.title,
        createdAt: DEMO_LESSON.createdAt,
        chapterCount: DEMO_LESSON.chapters.length,
        language: DEMO_LESSON.language,
        source: "demo",
      });
    }
    toast.success("Loading the demo lesson");
    router.push(`/lesson/${DEMO_LESSON.id}`);
  }, [router]);

  return (
    <div className="min-h-screen">
      <TopNav />

      <AnimatePresence mode="wait">
        {analyzing ? (
          <motion.main
            key="analyzing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex min-h-[calc(100vh-3.5rem)] items-center justify-center px-4 py-16"
          >
            <AnalysisProgress
              title={analyzing.title}
              onComplete={handleAnalysisComplete}
            />
          </motion.main>
        ) : (
          <motion.main
            key="landing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: -24 }}
            transition={{ duration: 0.45 }}
          >
            <Hero />

            <section id="how" className="mx-auto max-w-7xl scroll-mt-24 px-4 py-12 sm:px-6 sm:py-20">
              <div className="mb-10 text-center">
                <p className="arena-section-label mx-auto">The learning flow</p>
                <h2 className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-5xl">
                  From passive watch to <span className="arena-violet">active dialogue</span>
                </h2>
                <p className="mx-auto mt-3 max-w-xl text-sm leading-relaxed text-slate-400 sm:text-base">
                  Explore a lesson, ask what you want to know, then check the answer against its source.
                </p>
              </div>
              <div className="grid gap-4 md:grid-cols-3">
                {[
                  { icon: UploadCloud, number: "01", title: "Bring your video", body: "Upload a supported lesson and get a searchable transcript with a chapter map." },
                  { icon: MessageCircleQuestion, number: "02", title: "Ask in your own words", body: "Type or speak. Choose an explanation level and answer language as you learn." },
                  { icon: Target, number: "03", title: "Verify the moment", body: "Jump from cited evidence to the exact part of the video. Web research stays clearly labeled." },
                ].map(({ icon: Icon, number, title, body }) => (
                  <article key={number} className="arena-feature-card rounded-2xl p-6 sm:p-7">
                    <div className="mb-6 flex items-center justify-between">
                      <span className="flex size-11 items-center justify-center rounded-xl border border-violet-400/25 bg-violet-500/10 text-violet-200"><Icon className="size-5" aria-hidden="true" /></span>
                      <span className="font-mono text-4xl font-semibold text-white/[0.08]">{number}</span>
                    </div>
                    <h3 className="text-lg font-semibold text-white">{title}</h3>
                    <p className="mt-2 text-sm leading-relaxed text-slate-400">{body}</p>
                  </article>
                ))}
              </div>
            </section>

            {/* Upload + demo */}
            <section
              id="upload"
              className="mx-auto max-w-5xl scroll-mt-24 px-4 pb-12 sm:px-6 sm:pb-16"
              aria-label="Upload a video"
            >
              <div className="mb-8 text-center">
                <p className="arena-section-label mx-auto">Step one · Start learning</p>
                <h2 className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-5xl">Upload your video</h2>
                <p className="mt-3 text-sm text-slate-400 sm:text-base">Drop a lesson here or choose the demo to explore the workspace.</p>
              </div>
              <UploadDropzone onAnalyzed={handleAnalyzed} />

              <div className="mt-5 flex flex-col items-center gap-3">
                <p className="text-xs uppercase tracking-widest text-slate-600">
                  or
                </p>
                <button
                  onClick={handleDemo}
                  className="group flex w-full items-center gap-4 rounded-2xl border border-white/[0.08] bg-white/[0.02] p-4 text-left outline-none transition-all hover:border-violet-400/40 hover:bg-violet-500/[0.05] focus-visible:ring-2 focus-visible:ring-violet-400/70"
                >
                  <span className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-violet-500/15">
                    <Sparkles className="size-5 text-violet-300" aria-hidden="true" />
                  </span>
                  <span className="min-w-0">
                    <span className="block text-sm font-medium text-white">
                      Try the demo lesson
                    </span>
                    <span className="mt-0.5 block truncate text-xs text-slate-400">
                      Gemini in Docs lesson plan — Lesson video: Google for Education
                    </span>
                  </span>
                </button>
              </div>

              <p className="mt-6 text-center text-xs leading-relaxed text-slate-600">
                Great for lectures, programming tutorials, exam preparation,
                workplace training, and public-service videos. Your video is
                analyzed to build chapters and a searchable lesson map — nothing
                is shared.
              </p>
            </section>

            {/* Trust strip */}
            <section
              aria-label="Why ContextBridge"
              className="mx-auto grid max-w-5xl gap-3 px-4 pb-20 sm:grid-cols-2 sm:px-6"
            >
              {[
                {
                  icon: Clock3,
                  title: "Skip to the moment that matters",
                  body: "Every answer points to the exact timestamp in the video.",
                },
                {
                  icon: ShieldCheck,
                  title: "Evidence you can trust",
                  body: "Video answers and web research are always clearly separated.",
                },
              ].map((item) => (
                <div
                  key={item.title}
                  className="flex gap-3.5 rounded-2xl border border-white/[0.06] bg-white/[0.02] p-4"
                >
                  <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-violet-500/10">
                    <item.icon className="size-4 text-violet-300" aria-hidden="true" />
                  </span>
                  <div>
                    <p className="text-sm font-medium text-slate-100">{item.title}</p>
                    <p className="mt-0.5 text-xs leading-relaxed text-slate-500">
                      {item.body}
                    </p>
                  </div>
                </div>
              ))}
            </section>

            <section id="features" className="mx-auto max-w-7xl scroll-mt-24 px-4 pb-20 sm:px-6">
              <div className="mb-10 text-center">
                <p className="arena-section-label mx-auto">Built for real learning</p>
                <h2 className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-5xl">
                  Keep the whole lesson <span className="arena-violet">in context.</span>
                </h2>
              </div>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {[
                  { icon: Captions, title: "Transcript in sync", body: "Follow the words and jump between the transcript and video." },
                  { icon: AudioLines, title: "Speak naturally", body: "Ask by voice or text, with English and Hindi support." },
                  { icon: ScanSearch, title: "Check the evidence", body: "Video answers carry timestamps and supporting quotes." },
                  { icon: Globe2, title: "Clear boundaries", body: "When the lesson falls short, web research is labeled and sourced separately." },
                ].map(({ icon: Icon, title, body }) => (
                  <article key={title} className="arena-feature-card rounded-2xl p-5">
                    <span className="mb-5 flex size-10 items-center justify-center rounded-xl border border-violet-400/25 bg-violet-500/10 text-violet-200"><Icon className="size-4.5" aria-hidden="true" /></span>
                    <h3 className="text-sm font-semibold text-white">{title}</h3>
                    <p className="mt-2 text-xs leading-relaxed text-slate-400">{body}</p>
                  </article>
                ))}
              </div>
              <div className="mt-10 flex flex-col items-center justify-between gap-5 rounded-3xl border border-violet-400/20 bg-gradient-to-r from-violet-500/[0.12] via-white/[0.025] to-fuchsia-500/[0.08] p-6 text-center sm:flex-row sm:p-8 sm:text-left">
                <div>
                  <h3 className="text-xl font-semibold text-white sm:text-2xl">Ready to explore a lesson?</h3>
                  <p className="mt-1 text-sm text-slate-400">Start with the live demo or bring a video of your own.</p>
                </div>
                <Link href="/lesson/demo-binary" className="arena-button-primary inline-flex h-11 shrink-0 items-center gap-2 rounded-xl px-5 text-sm font-semibold">
                  Open the demo <ArrowRight className="size-4" aria-hidden="true" />
                </Link>
              </div>
            </section>
          </motion.main>
        )}
      </AnimatePresence>
    </div>
  );
}
