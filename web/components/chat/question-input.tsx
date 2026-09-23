"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { ArrowUp, Mic, Square, AudioLines } from "lucide-react";
import { toast } from "sonner";
import { MOCK_VOICE_TRANSCRIPT } from "@/lib/demo-answers";
import { cn } from "@/lib/utils";

type VoiceState = "idle" | "listening" | "transcribing";

interface QuestionInputProps {
  disabled?: boolean;
  onAsk: (question: string, isVoice: boolean) => void;
}

/* Minimal typings for the Web Speech API (not in lib.dom for all targets). */
interface SpeechRecognitionLike {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  start(): void;
  stop(): void;
  onresult: ((event: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void) | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
}

export function QuestionInput({ disabled, onAsk }: QuestionInputProps) {
  const [value, setValue] = useState("");
  const [voiceState, setVoiceState] = useState<VoiceState>("idle");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const transcriptRef = useRef<string>("");
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);

  const submitTyped = () => {
    const q = value.trim();
    if (!q) return;
    setValue("");
    onAsk(q, false);
  };

  const finalizeVoice = useCallback(
    async (audioBlob: Blob | null) => {
      setVoiceState("transcribing");
      let transcript = transcriptRef.current.trim();
      // Simulate a short "understanding" beat; real mode posts the blob
      // to POST /analyses/:id/voice-question.
      await new Promise((r) => setTimeout(r, 800));
      if (!transcript) {
        transcript = MOCK_VOICE_TRANSCRIPT;
        toast.info("Voice demo: using a sample transcription", {
          description:
            "This browser can't transcribe speech natively — the demo answer will use a sample question.",
        });
      }
      if (!transcript) {
        toast.error("We didn't hear anything. Try again.");
        setVoiceState("idle");
        return;
      }
      onAsk(transcript, true);
      setVoiceState("idle");
      void audioBlob; // Real backend: send audio with the question.
    },
    [onAsk],
  );

  const startListening = useCallback(async () => {
    setVoiceState("listening");
    transcriptRef.current = "";
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        if (blob.size < 800) {
          // Too short — treat as an empty recording.
          setVoiceState("idle");
          toast.error("We didn't hear anything. Try again.");
          return;
        }
        void finalizeVoice(blob);
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
    } catch {
      setVoiceState("idle");
      toast.error("Microphone access is needed for voice questions.");
      return;
    }

    // Use native speech recognition when the browser supports it.
    const SR =
      (window as unknown as Record<string, unknown>).SpeechRecognition ??
      (window as unknown as Record<string, unknown>).webkitSpeechRecognition;
    if (SR) {
      const recognition = new (SR as new () => SpeechRecognitionLike)();
      recognition.lang = "en-US";
      recognition.continuous = true;
      recognition.interimResults = false;
      recognition.onresult = (event) => {
        const last = event.results[event.results.length - 1];
        if (last?.[0]) transcriptRef.current = last[0].transcript;
      };
      recognition.onerror = () => {};
      recognition.start();
      recognitionRef.current = recognition;
    }
  }, [finalizeVoice]);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    recognitionRef.current = null;
    mediaRecorderRef.current?.stop();
    mediaRecorderRef.current = null;
  }, []);

  // Cleanup on unmount.
  useEffect(() => {
    return () => {
      recognitionRef.current?.stop();
      if (mediaRecorderRef.current?.state === "recording") {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const listening = voiceState === "listening";
  const transcribing = voiceState === "transcribing";

  return (
    <div className="w-full">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          submitTyped();
        }}
        className="relative"
      >
        <div
          className={cn(
            "flex items-center gap-1 rounded-full border bg-white pl-5 pr-1.5 shadow-[0_8px_32px_-12px_rgba(0,0,0,0.6)] transition-all duration-300",
            listening
              ? "border-red-400/60 ring-2 ring-red-400/20"
              : "border-white/40 focus-within:border-violet-300 focus-within:ring-2 focus-within:ring-violet-300/40",
          )}
        >
          <AudioLines
            className={cn(
              "size-4 shrink-0 transition-colors",
              listening ? "text-red-500" : "text-slate-400",
            )}
            aria-hidden="true"
          />
          <label htmlFor="question-input" className="sr-only">
            Ask anything about this lesson
          </label>
          <input
            id="question-input"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            disabled={disabled || listening || transcribing}
            placeholder="Ask anything about this lesson…"
            autoComplete="off"
            className="h-12 min-w-0 flex-1 bg-transparent text-[15px] text-slate-900 placeholder:text-slate-400 outline-none disabled:opacity-60"
          />

          {/* Microphone — compact, no waveform takeover */}
          <button
            type="button"
            onClick={() => (listening ? stopListening() : startListening())}
            disabled={disabled || transcribing}
            aria-label={
              listening
                ? "Stop recording and submit your question"
                : "Record a voice question"
            }
            aria-pressed={listening}
            className={cn(
              "relative flex size-9 shrink-0 items-center justify-center rounded-full outline-none transition-colors focus-visible:ring-2 focus-visible:ring-violet-500",
              listening
                ? "bg-red-500 text-white"
                : "text-slate-500 hover:bg-slate-100 hover:text-violet-600",
            )}
          >
            {listening && (
              <>
                <motion.span
                  animate={{ scale: [1, 1.5], opacity: [0.5, 0] }}
                  transition={{ repeat: Infinity, duration: 1.2 }}
                  className="absolute inset-0 rounded-full bg-red-400"
                  aria-hidden="true"
                />
                <motion.span
                  animate={{ scale: [1, 1.35], opacity: [0.4, 0] }}
                  transition={{ repeat: Infinity, duration: 1.2, delay: 0.3 }}
                  className="absolute inset-0 rounded-full bg-red-400"
                  aria-hidden="true"
                />
              </>
            )}
            {listening ? (
              <Square className="relative size-3.5" aria-hidden="true" />
            ) : (
              <Mic className="relative size-4.5" aria-hidden="true" />
            )}
          </button>

          {/* Send — only shown for typed input to keep the pill uncluttered */}
          <button
            type="submit"
            disabled={disabled || !value.trim() || listening}
            aria-label="Send question"
            className="flex size-9 shrink-0 items-center justify-center rounded-full bg-violet-600 text-white outline-none transition-all hover:bg-violet-500 focus-visible:ring-2 focus-visible:ring-violet-500 disabled:opacity-30"
          >
            <ArrowUp className="size-4.5" aria-hidden="true" />
          </button>
        </div>
      </form>

      {/* Voice status line — subtle, sits under the pill */}
      <AnimatePresence>
        {(listening || transcribing) && (
          <motion.p
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            className="mt-2.5 pl-5 text-center text-xs text-slate-400"
            aria-live="polite"
          >
            {listening ? (
              <>
                <span className="mr-1.5 inline-block size-1.5 animate-pulse rounded-full bg-red-400 align-middle" />
                Listening… tap the mic again when you&apos;re done — it submits
                automatically.
              </>
            ) : (
              <>Understanding your question…</>
            )}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}

