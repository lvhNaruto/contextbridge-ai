"use client";

import { motion } from "motion/react";
import { MapPin } from "lucide-react";
import { formatTime } from "@/lib/utils";

/**
 * The signature interaction: jump the video to the exact moment
 * an answer came from.
 */
export function TimestampButton({
  seconds,
  onJump,
  size = "default",
}: {
  seconds: number;
  onJump: (seconds: number) => void;
  size?: "default" | "sm";
}) {
  return (
    <motion.button
      whileTap={{ scale: 0.95 }}
      onClick={() => onJump(seconds)}
      aria-label={`Jump to ${formatTime(seconds)} in the video`}
      className={`inline-flex items-center gap-1.5 rounded-full bg-violet-600 font-medium text-white shadow-[0_4px_16px_-4px_rgba(139,92,246,0.6)] outline-none transition-colors hover:bg-violet-500 focus-visible:ring-2 focus-visible:ring-violet-400/70 ${
        size === "sm" ? "px-3 py-1 text-xs" : "px-4 py-1.5 text-sm"
      }`}
    >
      <MapPin className={size === "sm" ? "size-3" : "size-3.5"} aria-hidden="true" />
      Jump to {formatTime(seconds)}
    </motion.button>
  );
}
