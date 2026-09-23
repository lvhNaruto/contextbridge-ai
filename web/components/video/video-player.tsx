"use client";

import {
  forwardRef,
  useCallback,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";
import { motion } from "motion/react";
import {
  Play,
  Pause,
  Volume2,
  VolumeX,
  Maximize,
  Captions,
  Gauge,
} from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn, formatTime } from "@/lib/utils";
import type { Chapter } from "@/types";

export interface VideoPlayerHandle {
  seek: (seconds: number) => void;
}

interface VideoPlayerProps {
  src: string;
  chapters: Chapter[];
  /** Evidence marker — the moment an answer came from. */
  highlightSeconds?: number | null;
  onTimeUpdate?: (seconds: number) => void;
  onActiveChapterChange?: (chapterId: string | null) => void;
  ariaLabel?: string;
}

const PLAYBACK_RATES = [0.75, 1, 1.25, 1.5, 2] as const;

export const VideoPlayer = forwardRef<VideoPlayerHandle, VideoPlayerProps>(
  function VideoPlayer(
    {
      src,
      chapters,
      highlightSeconds,
      onTimeUpdate,
      onActiveChapterChange,
      ariaLabel,
    },
    ref,
  ) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

    const [playing, setPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [volume, setVolume] = useState(1);
    const [muted, setMuted] = useState(false);
    const [rate, setRate] = useState(1);
    const [captionsOn, setCaptionsOn] = useState(false);
    const [controlsVisible, setControlsVisible] = useState(true);

    const seek = useCallback((seconds: number) => {
      const video = videoRef.current;
      if (!video) return;
      video.currentTime = seconds;
      setCurrentTime(seconds);
    }, []);

    useImperativeHandle(ref, () => ({ seek }), [seek]);

    const togglePlay = useCallback(() => {
      const video = videoRef.current;
      if (!video) return;
      if (video.paused) void video.play();
      else video.pause();
    }, []);

    // Auto-hide controls while playing.
    const wakeControls = useCallback(() => {
      setControlsVisible(true);
      if (hideTimer.current) clearTimeout(hideTimer.current);
      hideTimer.current = setTimeout(
        () => setControlsVisible(false),
        2600,
      );
    }, []);

    useEffect(() => {
      if (playing) wakeControls();
      else setControlsVisible(true);
      return () => {
        if (hideTimer.current) clearTimeout(hideTimer.current);
      };
    }, [playing, wakeControls]);

    // Notify parent about the active chapter.
    useEffect(() => {
      if (!onActiveChapterChange) return;
      const active = chapters.find(
        (c) => currentTime >= c.startSeconds && currentTime < c.endSeconds,
      );
      onActiveChapterChange(active?.id ?? null);
    }, [currentTime, chapters, onActiveChapterChange]);

    // Keyboard controls.
    const onKeyDown = (e: React.KeyboardEvent) => {
      if (e.key === " " || e.key === "k") {
        e.preventDefault();
        togglePlay();
      } else if (e.key === "ArrowRight") {
        seek(Math.min((videoRef.current?.currentTime ?? 0) + 5, duration));
      } else if (e.key === "ArrowLeft") {
        seek(Math.max((videoRef.current?.currentTime ?? 0) - 5, 0));
      }
    };

    const toggleFullscreen = () => {
      const el = containerRef.current;
      if (!el) return;
      if (document.fullscreenElement) void document.exitFullscreen();
      else void el.requestFullscreen();
    };

    const progress = duration > 0 ? (currentTime / duration) * 100 : 0;
    const highlightPos =
      highlightSeconds != null && duration > 0
        ? (highlightSeconds / duration) * 100
        : null;

    return (
      <div
        ref={containerRef}
        onKeyDown={onKeyDown}
        onMouseMove={wakeControls}
        tabIndex={0}
        role="region"
        aria-label={ariaLabel ?? "Video player — space to play or pause, arrow keys to seek"}
        className={cn(
          "group relative aspect-video w-full overflow-hidden rounded-2xl border border-white/[0.08] bg-black outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70",
        )}
      >
        <video
          ref={videoRef}
          src={src}
          playsInline
          preload="metadata"
          className="h-full w-full"
          onClick={togglePlay}
          onPlay={() => setPlaying(true)}
          onPause={() => setPlaying(false)}
          onTimeUpdate={(e) => {
            const t = e.currentTarget.currentTime;
            setCurrentTime(t);
            onTimeUpdate?.(t);
          }}
          onLoadedMetadata={(e) => setDuration(e.currentTarget.duration)}
          aria-label={ariaLabel ?? "Lesson video"}
        />

        {/* Center play button */}
        {!playing && (
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            onClick={togglePlay}
            aria-label="Play video"
            className="absolute inset-0 m-auto flex size-16 items-center justify-center rounded-full bg-violet-600/90 text-white shadow-[0_8px_40px_rgba(139,92,246,0.5)] backdrop-blur transition-transform hover:scale-105"
          >
            <Play className="ml-1 size-7" aria-hidden="true" />
          </motion.button>
        )}

        {/* Controls */}
        <div
          className={cn(
            "absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/85 via-black/45 to-transparent px-3 pb-3 pt-10 transition-opacity duration-300 sm:px-4",
            controlsVisible || !playing ? "opacity-100" : "pointer-events-none opacity-0",
          )}
        >
          {/* Intelligent timeline with chapter boundaries */}
          <div
            role="slider"
            aria-label="Seek within video"
            aria-valuemin={0}
            aria-valuemax={Math.round(duration)}
            aria-valuenow={Math.round(currentTime)}
            aria-valuetext={formatTime(currentTime)}
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "ArrowRight") seek(currentTime + 5);
              if (e.key === "ArrowLeft") seek(currentTime - 5);
            }}
            onClick={(e) => {
              const rect = e.currentTarget.getBoundingClientRect();
              const ratio = (e.clientX - rect.left) / rect.width;
              seek(ratio * duration);
            }}
            className="group/timeline relative -mx-1 mb-3 cursor-pointer rounded-md px-1 py-2 outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70"
          >
            {/* Chapter boundary ticks */}
            {chapters.slice(1).map((c) => (
              <span
                key={c.id}
                aria-hidden="true"
                className="absolute top-1/2 z-10 h-3 w-px -translate-y-1/2 rounded bg-[#070B14]/90"
                style={{ left: `${duration ? (c.startSeconds / duration) * 100 : 0}%` }}
              />
            ))}
            {/* Track */}
            <div className="relative h-1.5 rounded-full bg-white/15 transition-all group-hover/timeline:h-2.5">
              <div
                className="absolute inset-y-0 left-0 rounded-full bg-violet-500"
                style={{ width: `${progress}%` }}
              />
              {/* Playhead */}
              <span
                aria-hidden="true"
                className="absolute top-1/2 size-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white shadow transition-transform group-hover/timeline:scale-110"
                style={{ left: `${progress}%` }}
              />
              {/* Evidence highlight — the moment an answer came from */}
              {highlightPos != null && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 380, damping: 16 }}
                  aria-hidden="true"
                  className="absolute top-1/2 z-20 size-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-violet-500 shadow-[0_0_14px_rgba(139,92,246,0.9)]"
                  style={{ left: `${highlightPos}%` }}
                />
              )}
            </div>
          </div>


          <div className="flex items-center gap-1 sm:gap-1.5">
            <button
              onClick={togglePlay}
              aria-label={playing ? "Pause" : "Play"}
              className="flex size-9 items-center justify-center rounded-full text-white outline-none transition-colors hover:bg-white/10 focus-visible:ring-2 focus-visible:ring-violet-400/70"
            >
              {playing ? (
                <Pause className="size-5" aria-hidden="true" />
              ) : (
                <Play className="size-5" aria-hidden="true" />
              )}
            </button>

            <button
              onClick={() => {
                const video = videoRef.current;
                if (!video) return;
                video.muted = !video.muted;
                setMuted(video.muted);
              }}
              aria-label={muted ? "Unmute" : "Mute"}
              className="flex size-9 items-center justify-center rounded-full text-white outline-none transition-colors hover:bg-white/10 focus-visible:ring-2 focus-visible:ring-violet-400/70"
            >
              {muted || volume === 0 ? (
                <VolumeX className="size-5" aria-hidden="true" />
              ) : (
                <Volume2 className="size-5" aria-hidden="true" />
              )}
            </button>

            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={muted ? 0 : volume}
              onChange={(e) => {
                const v = Number(e.target.value);
                setVolume(v);
                if (videoRef.current) {
                  videoRef.current.volume = v;
                  videoRef.current.muted = v === 0;
                  setMuted(v === 0);
                }
              }}
              aria-label="Volume"
              className="h-1 w-16 cursor-pointer appearance-none rounded-full bg-white/20 accent-violet-500 outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70"
            />

            <span className="ml-1 font-mono text-xs tabular-nums text-slate-300">
              {formatTime(currentTime)}{" "}
              <span className="text-slate-500">/ {formatTime(duration)}</span>
            </span>

            <div className="ml-auto flex items-center gap-1">
              <Tooltip>
                <TooltipTrigger asChild>
                  <button
                    onClick={() => setCaptionsOn((c) => !c)}
                    aria-pressed={captionsOn}
                    aria-label="Toggle captions"
                    className={cn(
                      "flex size-9 items-center justify-center rounded-full outline-none transition-colors hover:bg-white/10 focus-visible:ring-2 focus-visible:ring-violet-400/70",
                      captionsOn ? "text-violet-300" : "text-slate-400",
                    )}
                  >
                    <Captions className="size-5" aria-hidden="true" />
                  </button>
                </TooltipTrigger>
                <TooltipContent>Captions</TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <button
                    onClick={() => {
                      const idx = PLAYBACK_RATES.indexOf(rate as (typeof PLAYBACK_RATES)[number]);
                      const next = PLAYBACK_RATES[(idx + 1) % PLAYBACK_RATES.length];
                      setRate(next);
                      if (videoRef.current) videoRef.current.playbackRate = next;
                    }}
                    aria-label={`Playback speed, currently ${rate}x`}
                    className="flex h-9 items-center justify-center rounded-full px-2 font-mono text-xs text-slate-300 outline-none transition-colors hover:bg-white/10 focus-visible:ring-2 focus-visible:ring-violet-400/70"
                  >
                    <span className="flex items-center gap-1">
                      <Gauge className="size-4" aria-hidden="true" />
                      {rate}x
                    </span>
                  </button>
                </TooltipTrigger>
                <TooltipContent>Playback speed</TooltipContent>
              </Tooltip>

              <button
                onClick={toggleFullscreen}
                aria-label="Toggle fullscreen"
                className="flex size-9 items-center justify-center rounded-full text-white outline-none transition-colors hover:bg-white/10 focus-visible:ring-2 focus-visible:ring-violet-400/70"
              >
                <Maximize className="size-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  },
);

