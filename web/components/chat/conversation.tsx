"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence, motion } from "motion/react";
import { MessageCircleQuestion } from "lucide-react";
import { AssistantMessage } from "@/components/chat/assistant-message";
import type { ChatMessage } from "@/types";
import { cn } from "@/lib/utils";

function UserMessage({ message }: { message: ChatMessage }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 300, damping: 26 }}
      className="flex justify-end"
    >
      <div className="max-w-[85%] rounded-2xl rounded-tr-md bg-violet-600 px-4 py-2.5 text-[15px] leading-relaxed text-white shadow-[0_4px_16px_-6px_rgba(139,92,246,0.5)]">
        {message.text}
        {message.isVoice && (
          <span className="mt-1 block text-right text-[10px] text-violet-200/80">
            asked by voice
          </span>
        )}
      </div>
    </motion.div>
  );
}

export function Conversation({
  messages,
  highlightMessageId,
  onJump,
  answerLanguage,
  emptyHint,
  lessonTitle,
  onSelectSuggestion,
}: {
  messages: ChatMessage[];
  /** The message whose moment is currently highlighted on the timeline. */
  highlightMessageId?: string | null;
  onJump: (seconds: number) => void;
  answerLanguage: string;
  emptyHint?: string;
  lessonTitle?: string;
  onSelectSuggestion?: (question: string) => void;
}) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-10 text-center">
        <span className="flex size-12 items-center justify-center rounded-2xl border border-violet-400/20 bg-violet-500/10">
          <MessageCircleQuestion className="size-5 text-violet-300" aria-hidden="true" />
        </span>
        <div>
          <p className="text-sm font-medium text-slate-200">
            Ask your first question about this lesson.
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {emptyHint ?? "Type below, or tap the microphone to speak."}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className="flex flex-col gap-5"
      role="log"
      aria-label="Conversation with the video"
      aria-live="polite"
    >
      <AnimatePresence initial={false}>
        {messages.map((message) =>
          message.role === "user" ? (
            <UserMessage key={message.id} message={message} />
          ) : (
            <div key={message.id} className={cn(message.processing && "min-h-16")}>
              <AssistantMessage
                message={message}
                isHighlighted={highlightMessageId === message.id}
                onJump={onJump}
                answerLanguage={answerLanguage}
                lessonTitle={lessonTitle}
                onSelectSuggestion={onSelectSuggestion}
              />
            </div>
          ),
        )}
      </AnimatePresence>
      <div ref={bottomRef} aria-hidden="true" />
    </div>
  );
}
