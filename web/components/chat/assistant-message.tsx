"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "motion/react";
import {
  GraduationCap,
  Copy,
  Check,
  Volume2,
  VolumeX,
  Quote,
} from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  ConfidenceBadge,
  EvidenceBadge,
} from "@/components/evidence/evidence-badge";
import { TimestampButton } from "@/components/evidence/timestamp-button";
import { WebSourceCard } from "@/components/evidence/web-source-card";
import { BoundaryCard } from "@/components/evidence/boundary-card";
import { ExploreSuggestions } from "@/components/chat/explore-suggestions";
import type { ChatMessage } from "@/types";
import { cn, formatTime } from "@/lib/utils";

const STAGE_COPY: Record<string, string> = {
  "checking-video": "Checking whether the video answers your question…",
  "finding-moment": "Finding the relevant moment…",
  researching: "Researching additional context…",
  "preparing-answer": "Preparing your teacher's answer…",
  speaking: "Preparing your teacher's voice answer…",
};

function formatEvidenceCard(
  text: string,
  answer?: ChatMessage["answer"],
  lessonTitle?: string,
): string {
  const parts: string[] = [text];

  if (answer?.evidence?.quote) {
    parts.push(`Evidence: "${answer.evidence.quote}"`);
  }

  if (
    answer?.evidence?.startSeconds !== undefined &&
    answer.evidence.startSeconds !== null
  ) {
    parts.push(`Timestamp: ${formatTime(answer.evidence.startSeconds)}`);
  }

  if (lessonTitle) {
    parts.push(`Source: ${lessonTitle}`);
  }

  return parts.join("\n\n");
}

function useSpeak() {
  const [speaking, setSpeaking] = useState(false);

  const speak = (text: string, lang: string) => {
    if (typeof window === "undefined" || !window.speechSynthesis) return;

    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    window.speechSynthesis.cancel();

    // Clean symbols for speech clarity
    const cleanText = text
      .replace(/\[\d{2}:\d{2}\]/g, "")
      .replace(/[*_#`~]/g, "")
      .replace(/https?:\/\/\S+/g, "")
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang;

    // Language-matched voice selection (Task 3.1)
    const voices = window.speechSynthesis.getVoices();
    if (voices && voices.length > 0) {
      const prefix = lang.toLowerCase().split("-")[0];
      const match = voices.find((v) => v.lang.toLowerCase().startsWith(prefix));
      if (match) {
        utterance.voice = match;
      }
    }

    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);

    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  };

  return { speaking, speak };
}

export function AssistantMessage({
  message,
  isHighlighted,
  onJump,
  answerLanguage,
  lessonTitle,
  onSelectSuggestion,
  autoSpeak,
  isLatest,
}: {
  message: ChatMessage;
  /** True when this answer's moment is the current timeline highlight. */
  isHighlighted?: boolean;
  onJump: (seconds: number) => void;
  answerLanguage: string;
  lessonTitle?: string;
  onSelectSuggestion?: (question: string) => void;
  autoSpeak?: boolean;
  isLatest?: boolean;
}) {
  const [copied, setCopied] = useState(false);
  const { speaking, speak } = useSpeak();
  const spokenRef = useRef(false);

  useEffect(() => {
    if (autoSpeak && isLatest && !message.processing && message.text && !spokenRef.current) {
      spokenRef.current = true;
      speak(message.text, answerLanguage === "hi" ? "hi-IN" : "en-US");
    }
  }, [autoSpeak, isLatest, message.processing, message.text, answerLanguage]);

  const copy = async () => {
    try {
      const payload = formatEvidenceCard(message.text, message.answer, lessonTitle);
      await navigator.clipboard.writeText(payload);
      setCopied(true);
      toast.success("Evidence card copied");
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard unavailable */
    }
  };

  // Processing state — friendly stage copy with a breathing avatar.
  if (message.processing) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-start gap-3"
        aria-live="polite"
      >
        <span className="relative mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-full border border-violet-400/30 bg-violet-500/15">
          <GraduationCap className="size-4 text-violet-300" aria-hidden="true" />
          <motion.span
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ repeat: Infinity, duration: 1.4 }}
            className="absolute inset-0 rounded-full ring-1 ring-violet-400/40"
            aria-hidden="true"
          />
        </span>
        <div className="flex flex-col gap-1.5 pt-1.5">
          <motion.span
            animate={{ opacity: [0.55, 1, 0.55] }}
            transition={{ repeat: Infinity, duration: 1.6 }}
            className="text-sm text-slate-300"
          >
            {STAGE_COPY[message.processing] ?? "Thinking…"}
          </motion.span>
          <span className="flex gap-1" aria-hidden="true">
            {[0, 1, 2].map((i) => (
              <motion.span
                key={i}
                animate={{ y: [0, -3, 0] }}
                transition={{ repeat: Infinity, duration: 0.9, delay: i * 0.15 }}
                className="size-1.5 rounded-full bg-violet-400/70"
              />
            ))}
          </span>
        </div>
      </motion.div>
    );
  }

  const answer = message.answer;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 260, damping: 24 }}
      className="flex items-start gap-3"
    >
      <span
        aria-hidden="true"
        className={cn(
          "relative mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-full border transition-all duration-300",
          speaking
            ? "border-emerald-400/60 bg-emerald-500/20 shadow-[0_0_16px_rgba(16,185,129,0.4)]"
            : "border-violet-400/25 bg-violet-500/15",
        )}
      >
        <GraduationCap
          className={cn(
            "size-4 transition-colors",
            speaking ? "text-emerald-300" : "text-violet-300",
          )}
        />
        {speaking && (
          <motion.span
            animate={{ scale: [1, 1.25, 1], opacity: [0.7, 0.1, 0.7] }}
            transition={{ repeat: Infinity, duration: 1.2 }}
            className="absolute inset-0 rounded-full border-2 border-emerald-400/60"
            aria-hidden="true"
          />
        )}
      </span>

      <div
        className={cn(
          "min-w-0 flex-1 rounded-2xl rounded-tl-md border p-4 transition-shadow duration-500",
          isHighlighted
            ? "border-violet-400/40 bg-violet-500/[0.07] shadow-[0_0_24px_-6px_rgba(139,92,246,0.35)]"
            : "border-white/[0.07] bg-white/[0.03]",
        )}
      >
        {answer?.evidenceType === "web" ? (
          <BoundaryCard sources={answer.sources}>
            <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-slate-100">
              {message.text}
            </p>
          </BoundaryCard>
        ) : (
          <>
            <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-slate-100">
              {message.text}
            </p>

            {answer?.evidence?.quote && (
              <blockquote className="mt-3 flex gap-2.5 rounded-xl border-l-2 border-violet-400/50 bg-violet-500/[0.06] px-3.5 py-2.5">
                <Quote className="mt-0.5 size-3.5 shrink-0 text-violet-300/70" aria-hidden="true" />
                <p className="text-xs italic leading-relaxed text-slate-300">
                  “{answer.evidence.quote}”
                </p>
              </blockquote>
            )}
          </>
        )}

        {/* Evidence footer — video and web are never mixed */}
        {answer && (
          <div className="mt-3.5 flex flex-wrap items-center gap-2 border-t border-white/[0.06] pt-3.5">
            <EvidenceBadge
              type={answer.evidenceType}
              confidence={answer.confidence}
            />
            {answer.evidenceType !== "video" && answer.confidence > 0 && (
              <ConfidenceBadge confidence={answer.confidence} />
            )}

            {answer.evidenceType === "video" && answer.evidence && (
              <span className="ml-auto">
                <TimestampButton
                  seconds={answer.evidence.startSeconds}
                  onJump={onJump}
                  size="sm"
                />
              </span>
            )}
          </div>
        )}

        {/* Explore from here suggestions (A9, D-25) */}
        {message.suggestions && message.suggestions.length > 0 && (
          <ExploreSuggestions
            suggestions={message.suggestions}
            onSelect={onSelectSuggestion}
          />
        )}

        {/* Copy + listen */}
        <div className="mt-3 flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={copy}
            aria-label={copied ? "Evidence card copied" : "Copy evidence card"}
          >
            {copied ? (
              <Check className="size-3.5 text-emerald-400" aria-hidden="true" />
            ) : (
              <Copy className="size-3.5" aria-hidden="true" />
            )}
          </Button>
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={() =>
              speak(message.text, answerLanguage === "hi" ? "hi-IN" : "en-US")
            }
            aria-label={
              speaking ? "Stop reading answer aloud" : "Read answer aloud"
            }
            className={cn(speaking && "text-emerald-400 hover:text-emerald-300")}
          >
            {speaking ? (
              <VolumeX className="size-3.5 text-emerald-400" aria-hidden="true" />
            ) : (
              <Volume2 className="size-3.5" aria-hidden="true" />
            )}
          </Button>
          {speaking && (
            <span className="ml-1 flex items-center gap-1.5 text-[11px] font-medium text-emerald-400">
              <span className="flex h-3 items-end gap-0.5" aria-hidden="true">
                {[0, 1, 2].map((i) => (
                  <motion.span
                    key={i}
                    animate={{ height: ["4px", "12px", "4px"] }}
                    transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.18 }}
                    className="w-0.5 rounded-full bg-emerald-400"
                  />
                ))}
              </span>
              Speaking aloud…
            </span>
          )}
          {message.isVoice && !speaking && (
            <span className="ml-1 text-[11px] text-slate-500">
              Voice answer
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
}

