"use client";

import { motion } from "motion/react";
import { Play, Archive, Trash2, ListVideo } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { SavedLessonMeta } from "@/types";

export function LessonCard({
  lesson,
  onArchive,
  onDelete,
}: {
  lesson: SavedLessonMeta;
  onArchive: (id: string) => void;
  onDelete: (id: string) => void;
}) {
  const date = new Date(lesson.createdAt);
  const formatted = date.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <motion.article
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className={`group flex flex-col gap-4 rounded-2xl border p-4 transition-colors ${
        lesson.archived
          ? "border-white/[0.05] bg-white/[0.01] opacity-60"
          : "border-white/[0.08] bg-[#0D1322] hover:border-violet-400/30"
      }`}
    >
      {/* Thumbnail */}
      <div className="relative aspect-video w-full overflow-hidden rounded-xl border border-white/[0.06] bg-gradient-to-br from-[#141B2F] to-[#0E1526]">
        <span className="absolute inset-0 m-auto flex size-10 items-center justify-center rounded-full bg-violet-600/90 text-white opacity-90 transition-transform group-hover:scale-110">
          <Play className="ml-0.5 size-4" aria-hidden="true" />
        </span>
        <span className="absolute bottom-2 left-2 flex items-center gap-1 rounded-md bg-black/70 px-2 py-0.5 text-[10px] font-medium text-slate-200 backdrop-blur">
          <ListVideo className="size-3" aria-hidden="true" />
          {lesson.chapterCount} chapters
        </span>
      </div>

      <div className="flex min-w-0 flex-1 flex-col">
        <h3 className="truncate text-sm font-medium text-white" title={lesson.title}>
          {lesson.title}
        </h3>
        <p className="mt-0.5 text-xs text-slate-500">
          {formatted} · {lesson.language}
        </p>
      </div>

      <div className="flex items-center gap-2">
        <a
          href={`/lesson/${lesson.id}`}
          className="inline-flex h-8 flex-1 items-center justify-center gap-1.5 rounded-full bg-violet-600 text-xs font-medium text-white outline-none transition-colors hover:bg-violet-500 focus-visible:ring-2 focus-visible:ring-violet-400/70"
          aria-label={`Continue learning: ${lesson.title}`}
        >
          <Play className="size-3" aria-hidden="true" />
          {lesson.archived ? "Open" : "Continue learning"}
        </a>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onArchive(lesson.id)}
          aria-label={lesson.archived ? "Unarchive lesson" : "Archive lesson"}
        >
          <Archive className="size-3.5" aria-hidden="true" />
        </Button>
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onDelete(lesson.id)}
          aria-label={`Delete ${lesson.title}`}
          className="hover:text-red-300"
        >
          <Trash2 className="size-3.5" aria-hidden="true" />
        </Button>
      </div>
    </motion.article>
  );
}
