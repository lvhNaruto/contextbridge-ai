"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "motion/react";
import { Sparkles, ShieldCheck, Clock3 } from "lucide-react";
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

            {/* Upload + demo */}
            <section
              id="upload"
              className="mx-auto max-w-2xl scroll-mt-24 px-4 pb-8 sm:px-6"
              aria-label="Upload a video"
            >
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
                      Understanding binary &amp; computer language — 5 chapters,
                      ready to question
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
              className="mx-auto grid max-w-3xl gap-3 px-4 pb-16 sm:grid-cols-2 sm:px-6"
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
          </motion.main>
        )}
      </AnimatePresence>
    </div>
  );
}

