"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { toast } from "sonner";
import { TopNav } from "@/components/top-nav";
import { Switch } from "@/components/ui/switch";
import { loadA11y, saveA11y } from "@/lib/store";
import type { AccessibilitySettings } from "@/types";

const OPTIONS: {
  key: keyof AccessibilitySettings;
  title: string;
  description: string;
}[] = [
  {
    key: "highContrast",
    title: "High contrast",
    description: "Stronger borders and brighter text across the interface.",
  },
  {
    key: "reduceMotion",
    title: "Reduce motion",
    description: "Minimize animations and transitions throughout the app.",
  },
  {
    key: "captionsPreferred",
    title: "Prefer captions",
    description: "Turn video captions on by default when available.",
  },
  {
    key: "plainLanguage",
    title: "Plain-language explanations",
    description:
      "Keep every answer short, simple, and jargon-free — like a teacher explaining to a beginner.",
  },
];

export default function AccessibilityPage() {
  const [settings, setSettings] = useState<AccessibilitySettings | null>(null);

  useEffect(() => {
    // Hydrate from localStorage after mount — values differ between the
    // server render and the client, so this must happen post-hydration.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setSettings(loadA11y());
  }, []);

  // Apply document-level accessibility attributes live.
  useEffect(() => {
    if (!settings) return;
    document.documentElement.dataset.contrast = settings.highContrast
      ? "high"
      : "normal";
    document.documentElement.dataset.motion = settings.reduceMotion
      ? "reduced"
      : "full";
    saveA11y(settings);
  }, [settings]);

  const toggle = (key: keyof AccessibilitySettings) => {
    if (!settings) return;
    setSettings({ ...settings, [key]: !settings[key] });
    toast.success("Accessibility setting updated");
  };

  return (
    <div className="min-h-screen">
      <TopNav />
      <main className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-2xl font-semibold tracking-tight text-white">
            Accessibility
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            ContextBridge is built for every learner. These settings apply
            instantly and persist across sessions.
          </p>
        </motion.div>

        <div className="mt-8 flex flex-col gap-3">
          {settings === null
            ? OPTIONS.map((o) => (
                <div
                  key={o.key}
                  className="h-[76px] animate-pulse rounded-2xl border border-white/[0.06] bg-white/[0.02]"
                />
              ))
            : OPTIONS.map((option) => (
                <label
                  key={option.key}
                  className="flex cursor-pointer items-center justify-between gap-4 rounded-2xl border border-white/[0.08] bg-[#0D1322] p-5 outline-none transition-colors has-[button:focus-visible]:ring-2 has-[button:focus-visible]:ring-violet-400/70"
                >
                  <span className="min-w-0">
                    <span className="block text-sm font-medium text-slate-100">
                      {option.title}
                    </span>
                    <span className="mt-0.5 block text-xs leading-relaxed text-slate-500">
                      {option.description}
                    </span>
                  </span>
                  <Switch
                    checked={settings[option.key]}
                    onCheckedChange={() => toggle(option.key)}
                    aria-label={option.title}
                  />
                </label>
              ))}
        </div>

        <div className="mt-8 rounded-2xl border border-violet-400/20 bg-violet-500/[0.06] p-5">
          <h2 className="text-sm font-medium text-violet-200">
            Always on, by design
          </h2>
          <ul className="mt-2.5 list-disc space-y-1.5 pl-4 text-xs leading-relaxed text-slate-400">
            <li>Full keyboard navigation with visible focus states</li>
            <li>Screen-reader labels on every control and status message</li>
            <li>Voice input and spoken answers, including Hindi</li>
            <li>Responsive layout that works on any screen size</li>
            <li>Status is never communicated by color alone</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
