"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";
import Link from "next/link";
import { Library } from "lucide-react";
import { TopNav } from "@/components/top-nav";
import { LessonCard } from "@/components/library/lesson-card";
import {
  listSavedLessons,
  removeLesson,
  updateLessonMeta,
  saveLessonMeta,
} from "@/lib/store";
import { deleteVideoBlob } from "@/lib/blob-store";
import { DEMO_LESSON } from "@/lib/mock-data";
import type { SavedLessonMeta } from "@/types";

export default function LibraryPage() {
  const [lessons, setLessons] = useState<SavedLessonMeta[] | null>(null);
  const [showArchived, setShowArchived] = useState(false);

  useEffect(() => {
    // Always include the demo lesson so judges can find it instantly.
    const existing = listSavedLessons();
    if (!existing.some((m) => m.id === DEMO_LESSON.id)) {
      saveLessonMeta({
        id: DEMO_LESSON.id,
        title: DEMO_LESSON.title,
        createdAt: DEMO_LESSON.createdAt,
        chapterCount: DEMO_LESSON.chapters.length,
        language: DEMO_LESSON.language,
        source: "demo",
      });
    }
    // Hydrate from localStorage after mount (see note in accessibility page).
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLessons(listSavedLessons());
  }, []);

  const refresh = () => setLessons(listSavedLessons());

  const handleArchive = (id: string) => {
    const lesson = lessons?.find((l) => l.id === id);
    updateLessonMeta(id, { archived: !lesson?.archived });
    refresh();
  };

  const handleDelete = (id: string) => {
    removeLesson(id);
    void deleteVideoBlob(id);
    refresh();
  };

  const active = lessons?.filter((l) => !l.archived) ?? [];
  const archived = lessons?.filter((l) => l.archived) ?? [];

  return (
    <div className="min-h-screen">
      <TopNav />
      <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-2xl font-semibold tracking-tight text-white">
            My lessons
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Your personal learning library — conversations, chapters, and
            settings are restored exactly where you left off.
          </p>
        </motion.div>

        {lessons === null ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <div
                key={i}
                className="h-56 animate-pulse rounded-2xl border border-white/[0.06] bg-white/[0.02]"
              />
            ))}
          </div>
        ) : active.length === 0 && archived.length === 0 ? (
          <div className="flex flex-col items-center gap-4 py-20 text-center">
            <span className="flex size-14 items-center justify-center rounded-2xl border border-violet-400/20 bg-violet-500/10">
              <Library className="size-6 text-violet-300" aria-hidden="true" />
            </span>
            <div>
              <p className="font-medium text-white">Your next lesson starts here.</p>
              <p className="mt-1 text-sm text-slate-500">
                Upload a video or try the demo lesson to begin.
              </p>
            </div>
            <Link href="/" className="inline-flex h-10 items-center justify-center rounded-full bg-violet-600 px-5 text-sm font-medium text-white outline-none transition-colors hover:bg-violet-500 focus-visible:ring-2 focus-visible:ring-violet-400/70">
              Go to Learn
            </Link>
          </div>
        ) : (
          <>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {active.map((lesson) => (
                <LessonCard
                  key={lesson.id}
                  lesson={lesson}
                  onArchive={handleArchive}
                  onDelete={handleDelete}
                />
              ))}
            </div>

            {archived.length > 0 && (
              <div className="mt-10">
                <button
                  onClick={() => setShowArchived((s) => !s)}
                  aria-expanded={showArchived}
                  className="text-xs font-medium text-slate-500 outline-none hover:text-slate-300 focus-visible:ring-2 focus-visible:ring-violet-400/70"
                >
                  {showArchived ? "Hide" : "Show"} archived lessons ({archived.length})
                </button>
                {showArchived && (
                  <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {archived.map((lesson) => (
                      <LessonCard
                        key={lesson.id}
                        lesson={lesson}
                        onArchive={handleArchive}
                        onDelete={handleDelete}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
