"use client";

import { Globe, Languages, SignalHigh, Volume2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { AnswerLanguage, ExplanationLevel, LessonSettings } from "@/types";

const LANGUAGES: { value: AnswerLanguage; label: string }[] = [
  { value: "auto", label: "Same as question" },
  { value: "en", label: "English" },
  { value: "hi", label: "Hindi" },
];

const LEVELS: { value: ExplanationLevel; label: string }[] = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "expert", label: "Expert" },
];

/** Compact learning controls that sit directly above the conversation. */
export function LessonSettingsBar({
  settings,
  onChange,
}: {
  settings: LessonSettings;
  onChange: (next: LessonSettings) => void;
}) {
  const langLabel =
    LANGUAGES.find((l) => l.value === settings.answerLanguage)?.label ?? "";
  const levelLabel =
    LEVELS.find((l) => l.value === settings.explanationLevel)?.label ?? "";

  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Language selector */}
      <DropdownMenu>
        <DropdownMenuTrigger
          aria-label={`Answer language: ${langLabel}`}
          className="flex h-8 items-center gap-1.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] focus-visible:ring-2 focus-visible:ring-violet-400/70 data-[state=open]:border-violet-400/40"
        >
          <Languages className="size-3.5 text-violet-300" aria-hidden="true" />
          <span>{langLabel}</span>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start">
          <DropdownMenuLabel>Answer Language</DropdownMenuLabel>
          {LANGUAGES.map((l) => (
            <DropdownMenuItem
              key={l.value}
              selected={settings.answerLanguage === l.value}
              onSelect={() =>
                onChange({ ...settings, answerLanguage: l.value })
              }
            >
              {l.label}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Explanation level selector */}
      <DropdownMenu>
        <DropdownMenuTrigger
          aria-label={`Explanation level: ${levelLabel}`}
          className="flex h-8 items-center gap-1.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] focus-visible:ring-2 focus-visible:ring-violet-400/70 data-[state=open]:border-violet-400/40"
        >
          <SignalHigh className="size-3.5 text-violet-300" aria-hidden="true" />
          <span>{levelLabel}</span>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start">
          <DropdownMenuLabel>Explanation Level</DropdownMenuLabel>
          {LEVELS.map((l) => (
            <DropdownMenuItem
              key={l.value}
              selected={settings.explanationLevel === l.value}
              onSelect={() =>
                onChange({ ...settings, explanationLevel: l.value })
              }
            >
              {l.label}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Web search toggle ("Research missing context") */}
      <button
        type="button"
        role="switch"
        aria-checked={settings.researchMissingContext}
        title="Search the web only when the video doesn't answer"
        onClick={() =>
          onChange({
            ...settings,
            researchMissingContext: !settings.researchMissingContext,
          })
        }
        className={`flex h-8 cursor-pointer select-none items-center gap-2 rounded-full border px-3 text-xs font-medium outline-none transition-all focus-visible:ring-2 focus-visible:ring-violet-400/70 ${
          settings.researchMissingContext
            ? "border-violet-500/40 bg-violet-500/10 text-violet-200 hover:bg-violet-500/15"
            : "border-white/[0.08] bg-white/[0.03] text-slate-400 hover:bg-white/[0.07]"
        }`}
      >
        <Globe
          className={`size-3.5 transition-colors ${
            settings.researchMissingContext ? "text-violet-300" : "text-slate-500"
          }`}
          aria-hidden="true"
        />
        <span>Web research</span>
        <span
          aria-hidden="true"
          className={`inline-flex h-4 w-7 shrink-0 items-center rounded-full p-0.5 transition-colors ${
            settings.researchMissingContext ? "bg-violet-500" : "bg-white/20"
          }`}
        >
          <span
            className={`size-3 rounded-full bg-white shadow-sm transition-transform duration-200 ease-in-out ${
              settings.researchMissingContext ? "translate-x-3" : "translate-x-0"
            }`}
          />
        </span>
      </button>
      {/* Auto-speak toggle (Task 3.1) */}
      <button
        type="button"
        role="switch"
        aria-checked={Boolean(settings.autoSpeak)}
        title="Automatically read answers aloud in matched language"
        onClick={() =>
          onChange({
            ...settings,
            autoSpeak: !settings.autoSpeak,
          })
        }
        className={`flex h-8 cursor-pointer select-none items-center gap-1.5 rounded-full border px-3 text-xs font-medium outline-none transition-all focus-visible:ring-2 focus-visible:ring-violet-400/70 ${
          settings.autoSpeak
            ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-200 hover:bg-emerald-500/15"
            : "border-white/[0.08] bg-white/[0.03] text-slate-400 hover:bg-white/[0.07]"
        }`}
      >
        <Volume2
          className={`size-3.5 transition-colors ${
            settings.autoSpeak ? "text-emerald-300" : "text-slate-500"
          }`}
          aria-hidden="true"
        />
        <span>Auto-speak</span>
      </button>
    </div>
  );
}
