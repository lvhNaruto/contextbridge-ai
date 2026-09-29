"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { ArrowUp, Mic, Square, AudioLines, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { transcribeAudio } from "@/lib/api";
import { lessonCopy, lessonUiLanguage } from "@/lib/lesson-copy";
import { cn } from "@/lib/utils";

type VoiceState = "idle" | "listening" | "transcribing";

interface QuestionInputProps {
  disabled?: boolean;
  onAsk: (question: string, isVoice: boolean, audioBlob?: Blob) => void;
  language?: string;
}

/* Minimal typings for the Web Speech API (not in lib.dom for all targets). */
interface SpeechRecognitionLike {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  start(): void;
  stop(): void;
  onresult: ((event: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void) | null;
  onerror: ((event: { error?: string }) => void) | null;
  onend: (() => void) | null;
}

export function QuestionInput({ disabled, onAsk, language = "auto" }: QuestionInputProps) {
  const copy = lessonCopy(lessonUiLanguage(language));
  const [value, setValue] = useState("");
  const [voiceState, setVoiceState] = useState<VoiceState>("idle");
  const [liveTranscript, setLiveTranscript] = useState<string>("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const transcriptRef = useRef<string>("");
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const discardRecordingRef = useRef(false);

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

      // If browser Web Speech didn't capture text, transcribe via backend Gemini
      if (!transcript && audioBlob && audioBlob.size > 800) {
        try {
          transcript = await transcribeAudio(audioBlob, language);
        } catch {
          transcript = "";
        }
      }

      if (!transcript) {
        setVoiceState("idle");
        setLiveTranscript("");
        toast.info(copy.noSpeech);
        return;
      }

      onAsk(transcript, true, audioBlob ?? undefined);
      setVoiceState("idle");
      setLiveTranscript("");
    },
    [onAsk, language, copy.noSpeech],
  );

  const startListening = useCallback(async () => {
    // Barge-in: immediately cancel any active answer speech when the learner speaks
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setVoiceState("listening");
    transcriptRef.current = "";
    setLiveTranscript("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        if (discardRecordingRef.current) {
          discardRecordingRef.current = false;
          setVoiceState("idle");
          setLiveTranscript("");
          return;
        }
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        if (blob.size < 500 && !transcriptRef.current.trim()) {
          setVoiceState("idle");
          setLiveTranscript("");
          toast.info("Recording was too short. Please try speaking again.");
          return;
        }
        void finalizeVoice(blob);
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
    } catch {
      setVoiceState("idle");
      setLiveTranscript("");
      toast.error(copy.micNeeded);
      return;
    }

    // Use native speech recognition with real-time interim results when supported.
    const SR =
      (window as unknown as Record<string, unknown>).SpeechRecognition ??
      (window as unknown as Record<string, unknown>).webkitSpeechRecognition;
    if (SR) {
      try {
        const recognition = new (SR as new () => SpeechRecognitionLike)();
        recognition.lang =
          language === "hi"
            ? "hi-IN"
            : language === "en"
              ? "en-US"
              : (navigator.language || "en-US");
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.onresult = (event) => {
          let full = "";
          for (let i = 0; i < event.results.length; i++) {
            const piece = event.results[i]?.[0]?.transcript || "";
            full += piece;
          }
          if (full.trim()) {
            transcriptRef.current = full.trim();
            setLiveTranscript(full.trim());
          }
        };
        recognition.onerror = (event) => {
          const code = event.error ?? "";
          // no-speech / aborted / network still leave the recording for transcription.
          const fatal =
            code === "not-allowed" ||
            code === "service-not-allowed" ||
            code === "audio-capture";
          if (!fatal) return;
          discardRecordingRef.current = true;
          setVoiceState("idle");
          setLiveTranscript("");
          toast.error(copy.voiceFailed);
          try {
            recognition.stop();
          } catch {
            /* already stopped */
          }
          const recorder = mediaRecorderRef.current;
          if (recorder && recorder.state === "recording") recorder.stop();
        };
        recognition.start();
        recognitionRef.current = recognition;
      } catch {}
    }
  }, [finalizeVoice, language, copy.micNeeded, copy.voiceFailed]);

  const stopListening = useCallback(() => {
    try {
      recognitionRef.current?.stop();
    } catch {}
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
    }
  }, []);

  // Cleanup on unmount.
  useEffect(() => {
    return () => {
      try {
        recognitionRef.current?.stop();
      } catch {}
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
            {copy.askLabel}
          </label>
          <input
            id="question-input"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            disabled={disabled || listening || transcribing}
            placeholder={copy.placeholder}
            autoComplete="off"
            className="h-12 min-w-0 flex-1 bg-transparent text-[15px] text-slate-900 placeholder:text-slate-400 outline-none disabled:opacity-60"
          />

          {/* Microphone — compact, no waveform takeover */}
          <button
            type="button"
            onClick={() => (listening ? stopListening() : startListening())}
            disabled={disabled || transcribing}
            aria-label={listening ? copy.stopRecord : copy.record}
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
            aria-label={copy.send}
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
            className="mt-2.5 px-4 text-center text-xs text-slate-400"
            aria-live="polite"
          >
            {listening ? (
              liveTranscript ? (
                <span className="font-medium text-violet-300">
                  &ldquo;{liveTranscript}&rdquo;
                </span>
              ) : (
                <>
                  <span className="mr-1.5 inline-block size-1.5 animate-pulse rounded-full bg-red-400 align-middle" />
                  {copy.listening}
                </>
              )
            ) : (
              <span className="inline-flex items-center gap-1.5 text-violet-300">
                <Sparkles className="size-3 animate-spin" />
                {copy.transcribing}
              </span>
            )}
          </motion.p>
        )}
      </AnimatePresence>

    </div>
  );
}

