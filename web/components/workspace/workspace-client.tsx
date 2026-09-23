"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "motion/react";
import { ListVideo, ChevronDown } from "lucide-react";
import { toast } from "sonner";
import { VideoPlayer, type VideoPlayerHandle } from "@/components/video/video-player";
import { ChapterList } from "@/components/chapters/chapter-list";
import { Conversation } from "@/components/chat/conversation";
import { QuestionInput } from "@/components/chat/question-input";
import { LessonSettingsBar } from "@/components/settings/lesson-settings";
import { Skeleton } from "@/components/ui/skeleton";
import { getAnalysis, askQuestion } from "@/lib/api";
import {
  loadConversation,
  saveConversation,
  loadSettings,
  saveSettings,
} from "@/lib/store";
import { uid } from "@/lib/utils";
import { DEMO_SUGGESTED_QUESTIONS } from "@/lib/mock-data";
import type {
  Chapter,
  ChatMessage,
  Lesson,
  LessonSettings,
  ProcessingStage,
} from "@/types";

/** Processing beats the assistant cycles through — visible but honest. */
const PROCESSING_BEATS: ProcessingStage[] = [
  "checking-video",
  "finding-moment",
  "preparing-answer",
];

export function WorkspaceClient({ lessonId }: { lessonId: string }) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [settings, setSettings] = useState<LessonSettings>({
    answerLanguage: "auto",
    explanationLevel: "beginner",
    researchMissingContext: true,
  });
  const [activeChapterId, setActiveChapterId] = useState<string | null>(null);
  const [highlightSeconds, setHighlightSeconds] = useState<number | null>(null);
  const [highlightedMessageId, setHighlightedMessageId] = useState<string | null>(null);
  const [chaptersOpen, setChaptersOpen] = useState(false);
  const [asking, setAsking] = useState(false);

  const playerRef = useRef<VideoPlayerHandle>(null);

  // Hydrate lesson + persisted conversation + settings.
  useEffect(() => {
    let cancelled = false;
    getAnalysis(lessonId)
      .then((l) => {
        if (!cancelled) setLesson(l);
      })
      .catch(() => {
        if (!cancelled)
          setLoadError("We couldn't load this lesson. It may have been removed.");
      });
    // Hydrate persisted conversation/settings after mount — these live in
    // localStorage, which is only readable on the client.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setMessages(loadConversation(lessonId));
    setSettings(loadSettings());
    return () => {
      cancelled = true;
    };
  }, [lessonId]);

  // Persist conversation and settings as they change.
  useEffect(() => {
    if (messages.length > 0) saveConversation(lessonId, messages);
  }, [messages, lessonId]);
  useEffect(() => {
    saveSettings(settings);
  }, [settings]);

  const handleJump = useCallback((seconds: number) => {
    playerRef.current?.seek(seconds);
    setHighlightSeconds(seconds);
  }, []);

  const handleChapterSelect = useCallback(
    (chapter: Chapter) => {
      handleJump(chapter.startSeconds);
      setChaptersOpen(false);
    },
    [handleJump],
  );

  const ask = useCallback(
    async (question: string, isVoice: boolean) => {
      if (!lesson || asking) return;
      setAsking(true);

      const userMessage: ChatMessage = {
        id: uid("msg"),
        role: "user",
        text: question,
        isVoice,
        createdAt: Date.now(),
      };
      const pendingId = uid("msg");
      const pendingMessage: ChatMessage = {
        id: pendingId,
        role: "assistant",
        text: "",
        createdAt: Date.now(),
        processing: "checking-video",
      };
      setMessages((prev) => [...prev, userMessage, pendingMessage]);

      // Cycle processing beats while the answer resolves.
      let beat = 0;
      const beatTimer = setInterval(() => {
        beat = (beat + 1) % PROCESSING_BEATS.length;
        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingId ? { ...m, processing: PROCESSING_BEATS[beat] } : m,
          ),
        );
      }, 900);

      try {
        const resolved = isVoice
          ? await askQuestion(lessonId, question, settings, true)
          : await askQuestion(lessonId, question, settings);
        setMessages((prev) =>
          prev.map((m) => (m.id === pendingId ? resolved : m)),
        );
        // If the answer is video-grounded, mark it as the highlighted moment.
        if (resolved.answer?.evidenceType === "video" && resolved.answer.evidence) {
          setHighlightSeconds(resolved.answer.evidence.startSeconds);
          setHighlightedMessageId(resolved.id);
        }
      } catch {
        toast.error("Something went wrong answering your question.");
        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingId
              ? {
                  ...m,
                  processing: undefined,
                  text: "Something went wrong while answering. Please try again.",
                  answer: { text: "", evidenceType: "unknown", confidence: 0 },
                }
              : m,
          ),
        );
      } finally {
        clearInterval(beatTimer);
        setAsking(false);
      }
    },
    [lesson, lessonId, settings, asking],
  );

  const chapters = lesson?.chapters ?? [];
  const suggested = useMemo(
    () => (messages.length === 0 ? DEMO_SUGGESTED_QUESTIONS.slice(0, 3) : []),
    [messages.length],
  );

  if (loadError) {
    return (
      <div className="mx-auto flex max-w-md flex-col items-center gap-3 py-24 text-center">
        <p className="text-lg font-medium text-white">{loadError}</p>
        <Link
          href="/"
          className="text-sm text-violet-300 underline-offset-4 hover:underline"
        >
          Back to Learn
        </Link>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="mx-auto grid max-w-6xl gap-6 px-4 py-8 sm:px-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div className="flex flex-col gap-6">
          <Skeleton className="aspect-video w-full rounded-2xl" />
          <Skeleton className="h-24 rounded-2xl" />
          <Skeleton className="h-12 rounded-full" />
        </div>
        <div className="hidden flex-col gap-3 lg:flex">
          <Skeleton className="h-6 w-32 rounded-lg" />
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-20 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        {/* Left column: video + conversation */}
        <div className="flex min-w-0 flex-col gap-5">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 240, damping: 26 }}
          >
            <VideoPlayer
              ref={playerRef}
              src={lesson.videoUrl}
              chapters={chapters}
              highlightSeconds={highlightSeconds}
              onActiveChapterChange={setActiveChapterId}
              ariaLabel={lesson.title}
            />
          </motion.div>

          {/* Mobile chapters drawer */}
          <div className="lg:hidden">
            <button
              onClick={() => setChaptersOpen((o) => !o)}
              aria-expanded={chaptersOpen}
              className="flex w-full items-center justify-between rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-sm font-medium text-slate-200 outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70"
            >
              <span className="flex items-center gap-2">
                <ListVideo className="size-4 text-violet-300" aria-hidden="true" />
                Chapters
              </span>
              <motion.span animate={{ rotate: chaptersOpen ? 180 : 0 }}>
                <ChevronDown className="size-4 text-slate-400" aria-hidden="true" />
              </motion.span>
            </button>
            <AnimatePresence initial={false}>
              {chaptersOpen && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="overflow-hidden"
                >
                  <div className="pt-3">
                    <ChapterList
                      chapters={chapters}
                      activeChapterId={activeChapterId}
                      onSelect={handleChapterSelect}
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Conversation */}
          <motion.section
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08, type: "spring", stiffness: 240, damping: 26 }}
            aria-label="Ask the video"
            className="rounded-2xl border border-white/[0.08] bg-[#0D1322] p-4 sm:p-5"
          >
            <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
              <h2 className="text-sm font-semibold text-slate-100">
                Ask your teacher
              </h2>
              <LessonSettingsBar settings={settings} onChange={setSettings} />
            </div>

            <div className="max-h-[420px] overflow-y-auto pr-1">
              <Conversation
                messages={messages}
                highlightMessageId={highlightedMessageId}
                onJump={handleJump}
                answerLanguage={settings.answerLanguage}
              />
            </div>

            {/* Suggested starters */}
            {suggested.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {suggested.map((q) => (
                  <button
                    key={q}
                    onClick={() => ask(q, false)}
                    className="rounded-full border border-white/[0.08] bg-white/[0.03] px-3 py-1.5 text-xs text-slate-300 outline-none transition-colors hover:border-violet-400/40 hover:text-violet-200 focus-visible:ring-2 focus-visible:ring-violet-400/70"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}

            <div className="mt-4">
              <QuestionInput disabled={asking} onAsk={ask} />
            </div>
          </motion.section>
        </div>

        {/* Right column: chapters (desktop) */}
        <motion.aside
          initial={{ opacity: 0, x: 16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.12, type: "spring", stiffness: 240, damping: 26 }}
          aria-label="In this video"
          className="hidden lg:block"
        >
          <div className="sticky top-20">
            <h2 className="mb-3 px-1 text-sm font-semibold text-slate-100">
              In this video
            </h2>
            <ChapterList
              chapters={chapters}
              activeChapterId={activeChapterId}
              onSelect={handleChapterSelect}
            />
          </div>
        </motion.aside>
      </div>
    </div>
  );
}

