"use client";

import { useCallback, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import {
  UploadCloud,
  FileVideo,
  X,
  AlertCircle,
  Loader2,
  RotateCcw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { formatBytes, isSupportedVideo, MAX_UPLOAD_BYTES } from "@/lib/utils";
import { createAnalysis } from "@/lib/api";
import type { Lesson } from "@/types";

type UploadState =
  | "idle"
  | "dragging"
  | "invalid"
  | "selected"
  | "uploading"
  | "error";

export function UploadDropzone({
  onAnalyzed,
}: {
  onAnalyzed: (lesson: Lesson) => void;
}) {
  const [state, setState] = useState<UploadState>("idle");
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string>("");
  const dragCounter = useRef(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const acceptFile = useCallback((f: File | undefined) => {
    if (!f) return;
    if (!isSupportedVideo(f)) {
      setState("invalid");
      setErrorMsg(
        "This video format isn't supported. Use MP4, MOV, MPEG, WEBM, or AVI.",
      );
      return;
    }
    if (f.size > MAX_UPLOAD_BYTES) {
      setState("invalid");
      setErrorMsg("File is too large. Videos are limited to 100 MB.");
      return;
    }
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setState("selected");
  }, []);

  const reset = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(null);
    setPreviewUrl(null);
    setErrorMsg("");
    setState("idle");
  };

  const startAnalysis = async () => {
    if (!file) return;
    setState("uploading");
    setErrorMsg("");
    try {
      const lesson = await createAnalysis(file);
      onAnalyzed(lesson);
    } catch {
      setState("error");
      setErrorMsg(
        "Something went wrong while uploading. Your file is safe — try again.",
      );
    }
  };

  return (
    <div
      onDragEnter={(e) => {
        e.preventDefault();
        dragCounter.current += 1;
        if (state === "idle" || state === "invalid") setState("dragging");
      }}
      onDragLeave={(e) => {
        e.preventDefault();
        dragCounter.current -= 1;
        if (dragCounter.current <= 0 && state === "dragging") setState("idle");
      }}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        dragCounter.current = 0;
        acceptFile(e.dataTransfer.files?.[0]);
      }}
      className="relative"
    >
      <input
        ref={inputRef}
        type="file"
        accept="video/mp4,video/quicktime,video/mpeg,video/webm,video/x-msvideo,.mp4,.mov,.mpeg,.webm,.avi"
        className="sr-only"
        aria-label="Choose a video file to upload"
        onChange={(e) => acceptFile(e.target.files?.[0])}
      />

      <AnimatePresence mode="wait">
        {(state === "idle" ||
          state === "dragging" ||
          state === "invalid") && (
          <motion.button
            key="dropzone"
            type="button"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8, scale: 0.98 }}
            transition={{ duration: 0.25 }}
            onClick={() => inputRef.current?.click()}
            aria-label="Drop your lesson here, or browse from your computer (up to 100 MB)"
            className={`group flex w-full flex-col items-center justify-center gap-4 rounded-3xl border-2 px-6 py-14 text-center outline-none transition-colors focus-visible:ring-2 focus-visible:ring-violet-400/70 focus-visible:ring-offset-2 focus-visible:ring-offset-[#070B14] sm:py-16 ${
              state === "dragging"
                ? "border-violet-400 bg-violet-500/[0.08]"
                : "border-dashed border-white/[0.14] bg-white/[0.02] hover:border-violet-400/50 hover:bg-violet-500/[0.04]"
            }`}
          >
            <motion.div
              animate={
                state === "dragging"
                  ? { scale: 1.08, y: -2 }
                  : { scale: 1, y: 0 }
              }
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className={`flex size-14 items-center justify-center rounded-2xl ${
                state === "dragging"
                  ? "bg-violet-500 text-white"
                  : "bg-white/[0.05] text-slate-400 group-hover:text-violet-300"
              }`}
            >
              <UploadCloud className="size-6" aria-hidden="true" />
            </motion.div>

            <div>
              <p className="text-lg font-medium text-white">
                Drop your lesson here
              </p>
              <p className="mt-1 text-sm text-slate-400">
                or browse from your computer
              </p>
            </div>

            <p className="font-mono text-[11px] uppercase tracking-widest text-slate-500">
              MP4 · MOV · MPEG · WEBM · AVI · UP TO 100 MB
            </p>

            {state === "invalid" && (
              <motion.p
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                role="alert"
                className="flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-4 py-1.5 text-xs text-red-300"
              >
                <AlertCircle className="size-3.5" aria-hidden="true" />
                {errorMsg}
              </motion.p>
            )}
          </motion.button>
        )}

        {(state === "selected" ||
          state === "uploading" ||
          state === "error") &&
          file && (
            <motion.div
              key="preview"
              initial={{ opacity: 0, y: 12, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ type: "spring", stiffness: 260, damping: 26 }}
              className="flex flex-col gap-5 rounded-3xl border border-white/[0.08] bg-[#0D1322] p-5 sm:flex-row sm:items-center"
            >
              <div className="relative aspect-video w-full shrink-0 overflow-hidden rounded-2xl border border-white/[0.07] bg-black sm:w-56">
                {previewUrl && (
                  <video
                    src={previewUrl}
                    muted
                    playsInline
                    preload="metadata"
                    className="h-full w-full object-cover"
                    aria-label={`Preview of ${file.name}`}
                  />
                )}
                <div className="absolute inset-0 flex items-center justify-center bg-black/25">
                  <FileVideo className="size-6 text-white/80" aria-hidden="true" />
                </div>
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate font-medium text-white" title={file.name}>
                  {file.name}
                </p>
                <p className="mt-0.5 text-sm text-slate-400">
                  {formatBytes(file.size)} · ready to analyze
                </p>

                <div className="mt-4 flex flex-wrap items-center gap-2.5">
                  {state === "selected" && (
                    <>
                      <Button onClick={startAnalysis}>
                        <UploadCloud className="size-4" aria-hidden="true" />
                        Analyze video
                      </Button>
                      <Button variant="ghost" onClick={reset}>
                        <X className="size-4" aria-hidden="true" />
                        Remove
                      </Button>
                    </>
                  )}
                  {state === "uploading" && (
                    <span
                      className="flex items-center gap-2 text-sm text-violet-300"
                      role="status"
                    >
                      <Loader2 className="size-4 animate-spin" aria-hidden="true" />
                      Uploading your lesson…
                    </span>
                  )}
                  {state === "error" && (
                    <>
                      <Button variant="secondary" onClick={startAnalysis}>
                        <RotateCcw className="size-4" aria-hidden="true" />
                        Retry upload
                      </Button>
                      <Button variant="ghost" onClick={reset}>
                        Cancel
                      </Button>
                      <p role="alert" className="w-full text-xs text-red-300">
                        {errorMsg}
                      </p>
                    </>
                  )}
                </div>
              </div>
            </motion.div>
          )}
      </AnimatePresence>
    </div>
  );
}

